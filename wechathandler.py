# -*- coding: utf-8 -*-
# filename: wechathandler.py
import hashlib

def wechat_echo(signature, timestamp, nonce, echostr):
    try:
        token = "iamteddybendyourknees"
        digest_list = [token, timestamp, nonce]
        digest_list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, digest_list)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return echostr
        else:
            return "auth failed"
    except Exception, Argument:
        return Argument
