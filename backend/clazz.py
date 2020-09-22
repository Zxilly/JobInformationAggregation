authURL = 'https://passport2.chaoxing.com/getauthstatus'


class Auth(object):
    def __init__(self, enc, uuid):
        self.enc = enc
        self.uuid = uuid

    def auth(self, session):
        req = session.post(url=authURL, data={
            'enc': self.enc,
            'uuid': self.uuid
        }).json()
        return req['status']
