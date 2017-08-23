//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    dataSources: ['douban/movie'],
    dataSourceNames: ['电影'],
    suggestUrls: ['https://movie.douban.com/j/subject_suggest'],
    placeHolders: ['电影,电视剧,综艺...'],
    currentPlaceHolder: '电影,电视剧,综艺...',
    searchSuggestions: [],
    dataSourceIndex: 0,
    qstr: ''
  },
  //事件处理函数
  bindDataSourceChange: function(e) {
    this.setData({
      dataSourceIndex: e.detail.value,
      currentPlaceHolder: this.data.placeHolders[e.detail.value]
    })
  },
  bindQueryStringInput: function(e) {
    this.setData({
      qstr: e.detail.value
    })
    this.searchSuggest(e.detail.value)
  },
  bindSearch: function(e) {
    if (this.data.searchSuggestions.length > 0) {
      var mid = this.data.searchSuggestions[0].id
      var dataSource = this.data.dataSources[this.data.dataSourceIndex]
      wx.navigateTo({
        url: '../' + dataSource + '?id=' + mid
      })
    }
  },
  searchSuggest: function(query) {
    var that = this
    if (this.data.dataSourceIndex == 0) {
      var suggestUrl = this.data.suggestUrls[0] + '?q=' + query
    }
    wx.request({
      url: suggestUrl,
      header: {
        'content-type': 'json'
      },
      success: function (res) {
        that.setData({
          searchSuggestions: res.data
        });
      }
    })
  },
  onLoad: function() {
    console.log('onLoad')
  }
})
