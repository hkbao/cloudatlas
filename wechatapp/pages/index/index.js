//index.js
var app = getApp()
Page({
  suggestUrls: ['https://movie.douban.com/j/subject_suggest', 'https://book.douban.com/j/subject_suggest', 'https://music.douban.com/j/subject_suggest'],
  data: {
    dataSources: ['douban/movie', 'douban/book', 'douban/music'],
    dataSourceNames: ['电影'],
    placeHolders: ['电影,电视剧,综艺', '书名,作者名', '歌曲名,专辑名'],
    searchSuggestions: [],
    movieInTheaters: [],
    tvShow: [],
    dataSourceIndex: 0,
    qstr: ''
  },
  //事件处理函数
  bindDataSourceChange: function(e) {
    this.setData({
      dataSourceIndex: parseInt(e.detail.value),
      searchSuggestions: []
    })
    if (this.data.qstr != '') {
      this.searchSuggest(this.data.qstr)
    }
  },
  bindQueryStringInput: function(e) {
    this.setData({
      qstr: e.detail.value
    })
    this.searchSuggest(e.detail.value)
  },
  bindSearch: function(e) {
    if (this.data.qstr) {
      var searchUrl = this.data.dataSources[this.data.dataSourceIndex].split('/')[0]
      var searchType = this.data.dataSources[this.data.dataSourceIndex].split('/')[1]
      wx.navigateTo({
        url: '../' + searchUrl + '/search?q=' + this.data.qstr + '&type=' + searchType
      })
    }
  },
  getSuggestData: function(data) {
    var info = data
    switch (this.data.dataSourceIndex) {
      case 0:
        break;
      case 1:
        for (var i in info) {
          info[i].img = info[i].pic
          info[i].sub_title = info[i].author_name
        }
        break;
      case 2:
        for (var i in info) {
          info[i].img = info[i].pic
          if (info[i].type == 's') {
            info[i].year = '专辑'
          }
          if (info[i].performer) {
            info[i].sub_title = info[i].performer.join('/')
          }
        }
        break;
      default:
        break;
    }
    console.log(info)
    return info
  },
  searchSuggest: function(query) {
    var that = this
    var suggestUrl = this.suggestUrls[this.data.dataSourceIndex] + '?q=' + query
    wx.request({
      url: suggestUrl,
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          searchSuggestions: that.getSuggestData(res.data)
        });
      }
    })
  },
  getMovieInTheaters: function() {
    var that = this
    wx.request({
      url: app.globalData.apiRoot + '/douban/api/movie/in_theaters?count=10',
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          movieInTheaters: res.data.subjects.slice(0,10)
        });
      }
    })
  },
  getTVShow: function () {
    var that = this
    wx.request({
      url: 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=0',
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        
        that.setData({
          tvShow: res.data.subjects.slice(0, 10)
        });
      }
    })
  },
  shareApp: function() {
    wx.showShareMenu({
      withShareTicket: true
    })
  },
  onLoad: function() {
    this.getMovieInTheaters()
    this.getTVShow()
  }
})
