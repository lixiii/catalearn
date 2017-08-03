

def login(key):
    r = requests.post('http://{}/api/admin/verifyKey'.format(self.CATALEARN_URL))