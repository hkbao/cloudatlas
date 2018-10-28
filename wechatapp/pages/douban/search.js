// search.js
var app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    qstr: '',
    qtype: '',
    searchResults: []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    this.setData({
      qstr: options.q,
      qtype: options.type
    })
    wx.showToast({
      title: '正在获取信息',
      icon: 'loading',
      duration: 10000
    })
    wx.request({
      url: app.globalData.apiRoot + '/douban/api/' + options.type + '/search?q=' + options.q,
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          searchResults: that.getSearchResults(res.data)
        });
        wx.hideToast()
      }
    })
  },
  getSearchResults: function(data) {
    var info = []
    if (this.data.qtype == 'movie') {
      for (var i in data.subjects) {
        if (data.subjects[i].directors.length > 0) {
          var author = data.subjects[i].directors[0].name
        } else {
          var author = 'unknown'
        }
        info.push({
          id: data.subjects[i].id,
          title: data.subjects[i].title,
          alt_title: data.subjects[i].original_title,
          year: data.subjects[i].year,
          image: data.subjects[i].images.medium,
          author: author,
          rating: data.subjects[i].rating
        })
      }
    } else if (this.data.qtype == 'book') {
      for (var i in data.books) {
        info.push({
          id: data.books[i].id,
          title: data.books[i].title,
          alt_title: data.books[i].subtitle,
          year: data.books[i].pubdate,
          image: data.books[i].image,
          author: data.books[i].author[0],
          rating: data.books[i].rating
        })
      }
    } else if (this.data.qtype == 'music') {
      for (var i in data.musics) {
        info.push({
          id: data.musics[i].id,
          title: data.musics[i].title,
          alt_title: data.musics[i].alt_title,
          year: data.musics[i].attrs.pubdate,
          image: data.musics[i].image,
          author: data.musics[i].author[0].name,
          rating: data.musics[i].rating
        })
      }
    }
    return info
  }
})