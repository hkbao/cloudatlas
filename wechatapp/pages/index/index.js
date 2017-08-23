//index.js
//获取应用实例
var app = getApp()
Page({
  data: {
    mid: '',
    movieInfo: {}
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function (option) {
    console.log('onLoad')
    var that = this
    that.setData({
      mid: option.id
    })
    //调用应用实例的方法获取全局数据
    app.getUserInfo(function(userInfo){
      //更新数据
      that.setData({
        userInfo:userInfo
      })
    });
    wx.request({
      url: 'https://api.douban.com/v2/movie/subject/' + option.id,
      header: {
        'content-type': 'json'
      },
      referrer: null,
      success: function (res) {
        that.setData({
          movieInfo: res.data
        })
      }
    })
  }
})
