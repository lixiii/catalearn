
import dill
import requests
from websocket import create_connection
import time
import sys
import re
from inspect import signature


CATALEARN_URL = 'catalearn.com'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def color_print(msg):
	print(bcolors.OKBLUE + msg	+ bcolors.ENDC)

class DummyModule(object):
    def dummy():
        return None

sys.modules["gpu"] = DummyModule

def run(func, *args, local = False):

	if not callable(func):
		color_print('please pass in a function')
		return

	n_vars = len(signature(func).parameters)
	if len(args) != n_vars:
		color_print('Oops, the function arguments don\'t seem to match')
		color_print('Do you have ' + str(signature(func)) + '?')

	gpu_ip = ''
	gpu_hash = ''

	color_print("starting GPU server, this will take about 10 seconds")
	r = requests.post('http://{}/api/computeRequest'.format(CATALEARN_URL), 
		data={'user_name' : 'user1'})
	res = r.json()
	color_print("server started, sending data to server")
	gpu_hash = res['hash']
	gpu_ip = res['ip']

	user = 'user1'

	SERVER_PORT = '8000'
	WS_PORT = '8001'

	dill.dump({
		'function' : func,
		'variables' : args
	}, open( user, "wb" ) )

	url = 'http://{}:{}/upload/{}'.format(gpu_ip, SERVER_PORT, gpu_hash)
	files = {'file': open(user, 'rb')}
	r = requests.post(url, files=files)

	color_print("data sent, computation about to begin")

	ws = create_connection('ws://{}:{}'.format(gpu_ip, WS_PORT))
	ws.send(gpu_hash)

	try:
		while True:
			msg = ws.recv()
			if msg == gpu_hash:
				break
			print(msg, end='')
		url = ws.recv()
		ws.close()
	except Exception as e:
		color_print(e)

	
	if url == 'FAILED':
		color_print('computation failed')
	else:
		color_print("computation successful, downloading return object")
		response = requests.get(url)
		with open('test.p', 'wb') as f:
			f.write(response.content)

		r = requests.post(url = 'http://{}:{}/stop/{}'.format(gpu_ip, SERVER_PORT, gpu_hash))
		result = dill.load(open('test.p', "rb" ))['result']
		return result