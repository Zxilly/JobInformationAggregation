authURL = 'https://passport2.chaoxing.com/getauthstatus'


class loginAuth(object):
    def __init__(self, enc, uuid):
        self.enc = enc
        self.uuid = uuid

    def loginAuth(self, session):
        req = session.post(url=authURL, data={
            'enc': self.enc,
            'uuid': self.uuid
        }).json()
        return req['status']
