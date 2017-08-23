# -*- coding: utf-8 -*-
# filename: wechathandler.py
import wechat.receive as receive
import wechat.reply as reply
import hashlib
import xml.etree.ElementTree as ET
from douban import DoubanMovie

token = "iamteddybendyourknees"
welcome_msg = \
"""欢迎关注本微信订阅号。回消息以查看基于大数据分析生成的关键字云图。"""
help_msg = \
"""• 输入电影名称，即可看到基于豆瓣短评生成的关键字云图。例如: 战狼2
• 请注意: 服务器位于aws美国，回复及图片加载有延迟，请耐心等待。由于网站未备案，点击阅读全文时可能会被微信拦截，此时请选择访问原网页。"""

def parse_xml(xml_str):
    if len(xml_str) == 0:
        return None
    xml_data = ET.fromstring(xml_str)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return receive.TextMsg(xml_data)
    elif msg_type == 'image':
        return receive.ImageMsg(xml_data)
    elif msg_type == 'event':
        return receive.EventMsg(xml_data)

def handle_msg(raw_data):
    rec_msg = parse_xml(raw_data)
    to_user = rec_msg.FromUserName
    from_user = rec_msg.ToUserName
    if rec_msg.MsgType == "text":
        query = rec_msg.Content.strip()
        if query in ["help", "h", "?", "帮助"]:
            reply_msg = reply.TextMsg(to_user, from_user, help_msg)
        else:
            try:
                movie = DoubanMovie(name=query)
                reply_msg = reply.ImageTextMsg(to_user, from_user, movie.get_basic_info())
            except Exception as e:
                msg_content = str(e) + "\n" + help_msg
                reply_msg = reply.TextMsg(to_user, from_user, msg_content)
        return reply_msg.send()
    elif rec_msg.MsgType == "event":
        if rec_msg.Event == "subscribe":
            msg_content = "\n".join([welcome_msg, help_msg])
            reply_msg = reply.TextMsg(to_user, from_user, msg_content)
            return reply_msg.send()
        else:
            return "success"
    else:
        return "success"

def wechat_auth(request):
    try:
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce     = request.args.get("nonce", "")
        echostr   = request.args.get("echostr", "")
        digest_list = [token.encode(), timestamp.encode(), nonce.encode()]
        digest_list.sort()
        sha1 = hashlib.sha1()
        tuple(map(sha1.update, digest_list))
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            return True
    except Exception as e:
        print("wechat auth failed:" + str(e))
    return False
