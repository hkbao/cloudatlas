//index.js
//获取应用实例
var app = getApp()
Page({
  dataSourceNames: ['电影', '书籍', '音乐'],
  suggestUrls: ['https://movie.douban.com/j/subject_suggest', 'https://book.douban.com/j/subject_suggest', 'https://music.douban.com/j/subject_suggest'],
  placeHolders: ['电影,电视剧,综艺...', '书名,作者名', '歌曲名,专辑名'],
  data: {
    dataSources: ['douban/movie', 'douban/book', 'douban/music'],
    dataSourceNames: ['电影', '书籍', '音乐'],
    placeHolders: ['电影,电视剧,综艺...', '书名,作者名', '歌曲名,专辑名'],
    searchSuggestions: [],
    dataSourceIndex: 0,
    qstr: ''
  },
  //事件处理函数
  bindDataSourceChange: function(e) {
    this.setData({
      dataSourceIndex: parseInt(e.detail.value),
      searchSuggestions: []
    })
    this.searchSuggest(this.data.qstr)
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
  shareApp: function() {
    wx.showShareMenu({
      withShareTicket: true
    })
  },
  onLoad: function() {
    console.log('onLoad')
  }
})