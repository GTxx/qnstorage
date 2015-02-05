import uuid
import qiniu

from django.core.files.base import File
from django.core.files.storage import Storage
from django.conf import settings


class QNFile(File):
    pass


class QNStorage(Storage):
    file_class = QNFile

    def __init__(self, bucket_name=None):
        self.secrete_key = getattr(settings, 'QINIU_SECRET_KEY')
        self.access_key = getattr(settings, 'QINIU_ACCESS_KEY')
        self.bucket_name = getattr(settings, 'QINIU_BUCKET_NAME', bucket_name)
        self.q = qiniu.Auth(self.access_key, self.secrete_key)
        self.bucket = qiniu.BucketManager(self.q)
    
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

    def delete(self, name):
        bucket = qiniu.BucketManager(self.q)
        ret, info = bucket.delete(self.bucket_name, name)
        if ret:
            return True
        else:
            raise Exception('delete qiniu file error, detail: {}'.format(info))

    def listdir(self, path):
        ''' list contents of specify path '''
        pass

    def size(self):
        pass

    def exists(self, name):
        ''' always false for file '''
        return False

    def url(self, name):
        name = name + '?imageView2/1/w/400/h/200'
        base_url = 'http://{}/{}'.format(self.bucket_name+'.qiniudn.com', name)
        return self.q.private_download_url(base_url, expires=3600)
