from django.core.files.storage import Storage
from django.conf import settings
from .utils import get_key
import uuid
import qiniu


class QNStorage(Storage):
    secrete_key = get_key('QINIU_SECRET_KEY')
    access_key = get_key('QINIU_ACCESS_KEY')

    def __init__(self, bucket_name=None):
        self.bucket_name = get_key('QINIU_BUCKET_NAME', bucket_name)
        self.q = qiniu.Auth(self.access_key, self.secrete_key)
    
    def _save(self, name, content):
        name = unicode(uuid.uuid4())
        token = self.q.upload_token(self.bucket_name)
        ret, info = qiniu.put_data(token, name, content)
        if ret:
            print('upload success')
            return name
        else:
            raise Exception('upload fail. detail: {}'.format(info))

    def _open(self, name, mode='rb'):
        pass

    def exists(self, name):
        ''' always false for file '''
        return False

    def url(self, name):
        name = name + '?imageView2/1/w/200/h/200'
        base_url = 'http://{}/{}'.format(self.bucket_name+'.qiniudn.com', name)
        return self.q.private_download_url(base_url, expires=3600)
