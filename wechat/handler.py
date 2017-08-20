# -*- coding: utf-8 -*-
# filename: wechathandler.py
import wechat.receive as receive
import wechat.reply as reply
import hashlib
import xml.etree.ElementTree as ET

token = "iamteddybendyourknees"
help_msg = "输入电影名称，即可看到基本信息以及基于豆瓣评论生成的关键字云图。"
accept_msg = "正在绘制云图，请稍候..."

def parse_xml(xml_str):
    if len(xml_str) == 0:
        return None
    xml_data = ET.fromstring(xml_str)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return receive.TextMsg(xml_data)
    elif msg_type == 'image':
        return receive.ImageMsg(xml_data)

def handle_msg(raw_data):
    rec_msg = parse_xml(raw_data)
    if isinstance(rec_msg, receive.Msg) and rec_msg.MsgType == 'text':
        to_user = rec_msg.FromUserName
        from_user = rec_msg.ToUserName
        if rec_msg.Content.strip() in ["help", "h", "?", "帮助"]:
            content = help_msg
        else:
            content = accept_msg
        reply_msg = reply.TextMsg(to_user, from_user, content)
        return reply_msg.send()
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
