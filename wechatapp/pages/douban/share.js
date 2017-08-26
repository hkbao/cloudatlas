var sharePage = function (e) {
  var that = this
  wx.showModal({
    content: '点击确定即可把本页面截图保存到相册，由于微信暂不支持小程序直接分享到朋友圈，如果喜欢本程序，请手动分享。',
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
          url: that.data.imgUrl + '&watermark=true',
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
              title: '截图错误',
              icon: 'loading',
              duration: 3000
            });
          }
        })
      }
    }
  });
}

module.exports.sharePage = sharePage