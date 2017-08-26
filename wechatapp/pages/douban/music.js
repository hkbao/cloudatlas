//music.js
var share = require('share.js')
var app = getApp()
Page({
  data: {
    id: '',
    imgLoading: true,
    info: {}
  },
  bindCloudImageLoad: function (e) {
    this.setData({
      imgLoading: false
    })
  },
  shareThisPage: share.sharePage,
  onLoad: function (option) {
    var that = this
    this.setData({
      id: option.id,
      imgUrl: 'http://iamted.cc/app/wordcloud?t=music&q=' + option.id
    })
    wx.showToast({
      title: '正在获取信息',
      icon: 'loading',
      duration: 10000
    })
    wx.request({
      url: 'https://api.douban.com/v2/music/' + option.id,
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          info: that.getMusicInfo(res.data)
        });
        wx.hideToast()
      }
    })
  },
  getMusicInfo: function (data) {
    var info = {
      title: data.title,
      year: data.attrs.pubdate[0],
      rating: data.rating,
      image: data.image.replace('/ipst/', '/mpst/'),
      attrs: [
        { attr_name: "又名", attr_value: data.alt_title },
        { attr_name: "表演者", attr_value: data.author[0].name },
        { attr_name: "类型", attr_value: data.attrs.version },
        { attr_name: "出版者", attr_value: data.attrs.publisher },
        { attr_name: "发行时间", attr_value: data.attrs.pubdate },
      ]
    }
    //generate tag
    var tags = []
    for (var i in data.tags) {
      tags.push(data.tags[i].name)
    }
    if (info.year) {
      info.year = info.year.split('-')[0]
    }
    info.attrs.push({ attr_name: '标签', attr_value: tags.join('/') })
    return info
  },

  /**
  * 用户点击右上角分享
  */
  onShareAppMessage: function (res) {
    if (res.from === 'button') {
      // 来自页面内转发按钮
      console.log(res.target)
    }
    return {
      title: '你的关键词 - 电影 ' + this.data.info.title,
      path: '/douban/movie?id=' + this.data.mid,
      success: function (res) {
        // 转发成功
      },
      fail: function (res) {
        // 转发失败
      }
    }
  }
})