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
      imgUrl: 'http://101.132.46.130/app/wordcloud?t=music&q=' + option.id
    })
    wx.showToast({
      title: '正在获取信息',
      icon: 'loading',
      duration: 10000
    })
    wx.request({
      url: app.globalData.apiRoot + 'music/' + option.id,
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
      rating: data.rating,
      image: data.image.replace('/ipst/', '/mpst/'),
      banner: data.image.replace('/ipst/', '/mpst/'),
      attrs: [
        data.author[0].name + '/' + data.attrs.pubdate,
        data.attrs.version + '/' + data.attrs.publisher
      ]
    }
    //generate tag
    var tags = []
    for (var i in data.tags) {
      tags.push(data.tags[i].name)
    }
    info.attrs.push(tags.join('/'))
    return info
  },

  /**
  * 用户点击右上角分享
  */
  onShareAppMessage: share.shareApp
})