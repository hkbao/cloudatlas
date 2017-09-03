//book.js
var share = require('share.js')
var app = getApp()
Page({
  data: {
    id: '',
    imgLoading: true,
    imgUrl: '',
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
      imgUrl: 'http://101.132.46.130/app/wordcloud?t=book&q=' + option.id
    })
    wx.showToast({
      title: '正在获取信息',
      icon: 'loading',
      duration: 10000
    })
    wx.request({
      url: 'https://api.douban.com/v2/book/' + option.id,
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          info: that.getBookInfo(res.data)
        });
        wx.hideToast()
      }
    })
  },
  getBookInfo: function (data) {
    var info = {
      title: data.title,
      rating: data.rating,
      image: data.image,
      banner: data.image,
      attrs: [
        (data.author? data.author.join('/'): '未知') + '(作者)/' + data.pubdate,
        data.publisher,
        data.pages + '页/￥' + data.price + ''
      ]
    }
    return info
  },

  /**
  * 用户点击右上角分享
  */
  onShareAppMessage: share.shareApp
})