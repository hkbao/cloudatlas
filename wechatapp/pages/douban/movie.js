//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    mid: '',
    imgLoading: true,
    movieInfo: {}
  },
  bindCloudImageLoad: function(e) {
    console.log('bindCloudImageLoad is called')
    this.setData({
      imgLoading: false
    })
  },
  onLoad: function (option) {
    console.log('onLoad')
    var that = this
    this.setData({
      mid: option.id
    })
    this.getMovieInfo = function(res) {
      var info = {
        title: res.data.title,
        rating: res.data.rating,
        image: res.data.image.replace('/ipst/', '/mpst/'),
        attrs: res.data.attrs,
      }
      for (var key in info.attrs) {
        for (var i in info.attrs[key]) {
          info.attrs[key][i] = info.attrs[key][i].split(' ')[0]
        }
        info.attrs[key] = info.attrs[key].slice(0,5).join('/')
      }
      return info
    }
    wx.showToast({
      title: '正在获取信息',
      icon: 'loading',
      duration: 10000
    })
    wx.request({
      url: 'https://api.douban.com/v2/movie/' + option.id,
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          movieInfo: that.getMovieInfo(res)
        });
        wx.hideToast()
      }
    })
  }
})