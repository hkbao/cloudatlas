# -*- coding: utf-8 -*-
from config import cache_path
import oss2
import time
import os
try:
    from urllib import quote_plus
except ImportError:
    from urllib.parse import quote_plus

class LocalCache(object):
    def __init__(self, cache_path):
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)
        self.cache_path = cache_path
    
    def put(self, file_name, file_obj, obj_type='png'):
        full_path = os.path.join(self.cache_path, file_name)
        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path))
       	with open(full_path, 'wb') as f:
            f.write(file_obj.getvalue())

    def get(self, file_name):
        full_path = os.path.join(self.cache_path, file_name)
        return open(full_path, 'rb')
    
    def exists(self, file_name, mtime=None):
        full_path = os.path.join(self.cache_path, file_name)
        if os.path.exists(full_path):
            if mtime and (time.time() - os.path.getmtime(full_path) > mtime):
                return False
            else:
                return True
        else:
            return False
    
    def get_url(self, file_name):
        return os.path.join('/', os.path.basename(self.cache_path), file_name)

class OSSCache(object):
    def __init__(self, oss_key_path):
        with open(oss_key_path) as f:
            endpoint, bucket, key_id, key_secret = f.read().splitlines()
        self.auth = oss2.Auth(key_id, key_secret)
        self.service = oss2.Service(self.auth, endpoint)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket)
        self.cache_url = 'https://%s.%s/' % (bucket, endpoint)
    
    def put(self, file_name, file_obj, obj_type='image/png'):
        self.bucket.put_object(file_name, file_obj.getvalue(), headers={'Content-Type': obj_type, 'x-oss-object-acl': 'public-read'})

    def get(self, file_name):
        return self.bucket_get_object(file_name)
    
    def exists(self, file_name, mtime=None):
        return self.bucket.object_exists(file_name)

    def get_url(self, file_name, expire_time=3600):
        return self.cache_url + quote_plus(file_name)
        #return self.bucket.sign_url('GET', file_name , expire_time)

if cache_path == 'oss':
    cache = OSSCache('oss_key.txt')
else:
    cache = LocalCache(cache_path)
