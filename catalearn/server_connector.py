
import requests
from websocket import create_connection
import time
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import json
import dill
import os
from tqdm import tqdm
import sys
from .dummies import import_all, unimport_all


def status_check(res):
    if res.status_code != 200:
        print(res.text)
        sys.exit()


class ServerConnector():

    def __init__(self, username, instanceType):
        self.GPU_SERVER_PORT = '8000'
        self.username = username
        self.type = instanceType
        if instanceType == 'local':
            self.CATALEARN_URL = 'localhost:8080'
        else:
            self.CATALEARN_URL = 'catalearn.com'

    def verify_key(self, key):
        r = requests.post(
            'http://{}/api/admin/verifyKey'.format(self.CATALEARN_URL))
        status_check(r)
        res = r.json()
        if 'err' in res:
            print(res['err'])
            return False
        else:
            return True

    def contact_server(self):

        print("Starting server, this will take about 3 minutes")

        r = requests.post('http://{}/api/gpu/checkAvailability'.format(self.CATALEARN_URL),
                              data={'username': self.username,
                                    'type': self.type})
        status_check(r)
        res = r.json()

        if 'err' in res:
            print(res['err'])
            sys.exit()

        self.jobHash = res['jobHash']
        instanceId = res['instanceId']
        while True:
            r = requests.post('http://{}/api/gpu/checkStatus'.format(self.CATALEARN_URL),
                                  data={'instanceId': instanceId})
            status_check(r)
            res = r.json()
            if 'err' in res:
                print(res['err'])
                return
            if res['started']:
                break
            time.sleep(3)
            print('-', end='')

        print()

        r = requests.post('http://{}/api/gpu/runJob'.format(self.CATALEARN_URL),
                              data={'hash': self.jobHash})
        status_check(r)
        res = r.json()
        if 'err' in res:
            print(res['err'])
            return None
        else:
            gpu_hash = res['hash']
            gpu_ip = res['ip']
            ws_port = res['ws_port']
            return (gpu_hash, gpu_ip, ws_port)

    def upload_params_decorator(self, gpu_ip, job_hash):
        url = 'http://{}:{}/runJobDecorator'.format(
            gpu_ip, self.GPU_SERVER_PORT, job_hash)
        self.upload_params(url, job_hash)

    def upload_params_magic(self, gpu_ip, job_hash):
        url = 'http://{}:{}/runJobMagic'.format(
            gpu_ip, self.GPU_SERVER_PORT, job_hash)
        self.upload_params(url, job_hash)

    def upload_params(self, url, job_hash):
        print("Uploading data")
        time.sleep(0.5)
        file_size = os.path.getsize('uploads.pkl')

        pbar = tqdm(total=file_size, unit='B', unit_scale=True)

        def callback(monitor):

            progress = monitor.bytes_read - callback.last_bytes_read
            pbar.update(progress)
            callback.last_bytes_read = monitor.bytes_read
        callback.last_bytes_read = 0

        with open('uploads.pkl', 'rb') as pickle_file:
            data = {
                    'file': ('uploads.pkl', pickle_file, 'application/octet-stream'),
                    'hash': job_hash
                }
            encoder = MultipartEncoder(
                fields=data
            )
            monitor = MultipartEncoderMonitor(encoder, callback)
            r = requests.post(url, data=monitor, headers={
                                  'Content-Type': monitor.content_type})
            pbar.close()
            status_check(r)

    def stream_output(self, gpu_ip, gpu_hash, ws_port):

        gpuUrl = 'ws://{}:{}'.format(gpu_ip, ws_port)

        ws = create_connection(gpuUrl)

        outUrl = None
        ws.send(gpu_hash)
        try:
            while True:
                message = ws.recv()
                msgJson = json.loads(message)
                if 'end' in msgJson:
                    if 'downloadUrl' in msgJson:
                        outUrl = msgJson['downloadUrl'] 
                    else:
                        outUrl = None
                    ws.close()
                    break
                else:
                    sys.stdout.write(msgJson['message'])
                    sys.stdout.flush()
            return outUrl
        except KeyboardInterrupt:
            print('\nJob interrupted')
            ws.close()

    def get_return_object(self, outUrl):

        print("Downloading result")

        r = requests.post(outUrl, data={'hash' : self.jobHash}, stream=True)
        status_check(r)
        total_size = int(r.headers.get('content-length', 0))
        with open('return.pkl', 'wb') as f:
            pbar = tqdm(total=total_size, unit='B', unit_scale=True)
            chunck_size = 32768
            for data in r.iter_content(chunck_size):
                f.write(data)
                pbar.update(chunck_size)
            pbar.close()

        with open('return.pkl', "rb") as f:

            # import_all()  # Hack: a workaround for dill's pickling problem
            result = dill.load(f)
            # unimport_all()
            if result is None:
                print('Computation failed')
            print("Done!")
            return result
