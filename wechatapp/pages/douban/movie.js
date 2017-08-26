//movie.js
var share = require('share.js')
var app = getApp()
Page({
  data: {
    id: '',
    imgLoading: true,
    info: {}
  },
  bindCloudImageLoad: function(e) {
    this.setData({
      imgLoading: false
    })
  },
  shareThisPage: share.sharePage,
  onLoad: function (option) {
    var that = this
    this.setData({
      id: option.id,
      imgUrl: 'http://iamted.cc/app/wordcloud?t=movie&q=' + option.id
    })
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
          info: that.getMovieInfo(res.data)
        });
        wx.hideToast()
      }
    })
  },
  getMovieInfo: function (data) {
    var info = {
      title: data.title,
      year: data.attrs.year[0],
      rating: data.rating,
      image: data.image.replace('/ipst/', '/mpst/'),
      attrs: [
        {attr_name: "导演", attr_value: data.attrs.director},
        {attr_name: "主演", attr_value: data.attrs.cast},
        {attr_name: "类型", attr_value: data.attrs.movie_type},
        {attr_name: "国家/地区", attr_value: data.attrs.country},
        {attr_name: "上映日期", attr_value: data.attrs.pubdate},
        { attr_name: "片长", attr_value: data.attrs.movie_duration}
      ]
    }
    //Remove english names
    for (var i in info.attrs) {
      for (var j in info.attrs[i].attr_value) {
        info.attrs[i].attr_value[j] = info.attrs[i].attr_value[j].split(' ')[0]
      }
      if (info.attrs[i].attr_value) {
        info.attrs[i].attr_value = info.attrs[i].attr_value.slice(0, 5).join('/')
      }
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