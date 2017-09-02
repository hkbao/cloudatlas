//movie.js
var share = require('share.js')
var app = getApp()
Page({
  data: {
    id: '',
    screenCap: false,
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
      imgUrl: 'http://101.132.46.130/app/wordcloud?t=movie&q=' + option.id
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
      star: parseInt(parseFloat(data.rating.average) + 0.5),
      image: data.image.replace('/ipst/', '/mpst/'),
      banner: data.image.replace('/ipst/', '/lpst/'),
      attrs: [
        '',
        data.attrs.movie_duration + ' ' + data.attrs.movie_type.join('/'),
        data.attrs.pubdate.pop() + ' ' + data.attrs.country.join('/')
      ]
    }

    //Remove english names
    var casts = data.attrs.cast.slice(0,3)
    if (data.attrs.director) {
      casts.splice(0, 0, data.attrs.director.join(' '))
    }
    for (var i in casts) {
      casts[i] = casts[i].split(' ')[0]
      if (i == 0) { casts[i] += '(导演)' }
    }
    info.attrs[0] = casts.join('/')
    if (!this.hasChineseChar(info.title)) {
      info.title = data.alt_title.split('/')[0]
    }
    return info
  },

  hasChineseChar: function(str) {
    var reg = new RegExp('[\\u4E00-\\u9FFF]+', 'g');
    return reg.test(str);
  },

  /**
  * 用户点击右上角分享
  */
  onShareAppMessage: share.shareApp
})