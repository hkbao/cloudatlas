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
      imgUrl: 'http://iamted.cc/app/wordcloud?t=book&q=' + option.id
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
      year: data.pubdate,
      rating: data.rating,
      image: data.image,
      attrs: [
        { attr_name: "作者", attr_value: data.author.join('/') },
        { attr_name: "出版社", attr_value: data.publisher },
        { attr_name: "出版时间", attr_value: data.pubdate },
        { attr_name: "页数", attr_value: data.pages },
        { attr_name: "定价", attr_value: data.price }
      ]
    }
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
      title: '你的阅读关键词: ' + this.data.info.title,
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