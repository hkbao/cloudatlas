var sharePage = function (e) {
  captureImage(this.data.imgUrl.replace('http://101.132.46.130', 'https://cloudatlas.applinzi.com'), this.data.info)
}

var captureImage = function(imgUrl, info) {
  wx.showModal({
    content: '点击确定把云图保存到相册，由于微信暂不支持小程序直接分享到朋友圈，如果喜欢本程序，请手动分享。',
    showCancel: true,
    success: function (res) {
      if (res.confirm) {
        console.log('用户点击确定')
        wx.showToast({
          title: '正在处理...',
          icon: 'loading',
          duration: 10000
        });
        wx.downloadFile({
          url: imgUrl + '&watermark=' + JSON.stringify(info),
          success: function (res) {
            wx.saveImageToPhotosAlbum({
              filePath: res.tempFilePath,
              success: function (res) {
                wx.hideToast();
                wx.showToast({
                  title: '截图成功',
                  icon: 'success',
                  duration: 3000
                });
              },
              fail: function (res) {
                console.log(res)
              }
            })
          },
          fail: function (res) {
            wx.showToast({
              title: res.data,
              icon: 'loading',
              duration: 3000
            });
          }
        })
      }
    }
  });
}

var shareApp = function (res) {
  if (res.from === 'button') {
    // 来自页面内转发按钮
    console.log(res.target)
  }
  return {
    title: '你的关键词 - ' + this.data.info.title,
    path: '/douban/movie?id=' + this.data.id,
    success: function (res) {
      // 转发成功
    },
    fail: function (res) {
      // 转发失败
    }
  }
}

module.exports.sharePage = sharePage