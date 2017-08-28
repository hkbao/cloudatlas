import time

class Msg(object):
    def __init__(self):
        pass
    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)

class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId
    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[image]]></MsgType>
        <Image>
        <MediaId><![CDATA[{MediaId}]]></MediaId>
        </Image>
        </xml>
        """
        return XmlForm.format(**self.__dict)

class ImageTextMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaInfo):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.set_movie_info(mediaInfo)

    def set_movie_info(self, info):
        self.__dict['MovieTitle'] = "%s (%s)" % (info['title'], info['attrs']['year'])
        self.__dict['MovieDescription'] = "导演:%s|主演:%s|类型:%s|豆瓣评分:%s" % \
            (info['attrs'].get('director'), info['attrs'].get('cast',''), info['attrs'].get('movie_type'), info['rating'].get('average'))
        self.__dict['MoviePic'] = "https://cloudatlas.applinzi.com/app/wordcloud?q=%s&t=movie" % info['mid']
        self.__dict['url'] = "http://cloudatlas.applinzi.com/app/movie/" + info['mid']

    def send(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[{MovieTitle}]]></Title>
        <Description><![CDATA[{MovieDescription}]]></Description>
        <PicUrl><![CDATA[{MoviePic}]]></PicUrl>
        <Url><![CDATA[{url}]]></Url>
        </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)
