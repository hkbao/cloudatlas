var kwlist = []
var displist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
var colors = ['#000000', '#FF00FF', '#FFA500', '#8A2BE2', '#DC143C', '#008B8B', '#006400', '#FF8C00', '#FF1493',
              '#1E90FF', '#FFD700', '#008000', '#808000', '#ADD8E6', '#32CD32', '#9370DB']

function kwdata(word, size, x, y, ispeed, color) {
  this.word = word;
  this.size = size;
  this.x = x;
  this.y = y;
  this.speed = ispeed;
  this.ispeed = ispeed;
  this.color = color;
}

var getRandomColor = function () {
  return colors[Math.round(Math.random() * 16)]
}

var getTopNews = function() {
  wx.request({
    url: 'https://cloudatlas.applinzi.com/app/kwdata?qtype=news',
    header: {
      'content-type': 'json'
    },
    success: function (res) {
      console.log(res.data)
      for (var kw in res.data) {
        if (res.data[kw]) {
          kwlist.push(new kwdata(kw, parseInt(res.data[kw] * 200 + 20), Math.round(Math.random() * 280), Math.round(Math.random() * 280) + 300, Math.round(Math.random() * 3) + 2, getRandomColor()))
        }
      }
      console.log(kwlist)
      setInterval(buildWordCloud, 20)
    }
  })
}

var buildWordCloud = function() {
  var context = wx.createCanvasContext('wccanvas')
  function drawText(text, x, y, size, color) {
    context.setFontSize(size)
    context.setFillStyle(color) 
    context.fillText(text, x, y)
  }

  for (var x in displist) {
    var i = displist[x]
    var kwd = kwlist[i]
    if (kwd.y <= -10) {
      displist[x] = (i + (displist.length)) % kwlist.length
      kwd.x = Math.round(Math.random() * 280)
      kwd.ispeed = Math.round(Math.random() * 3) + 2;
      kwd.y = Math.round(Math.random() * 300) + 300;
      continue
    }
    if (kwd.y >= 250 || kwd.y <= 80) {
      kwd.speed = kwd.ispeed
    } else {
      kwd.speed = kwd.ispeed / 2
    }
    kwd.y -= kwd.speed
    if (kwd.y <= 350) {
      drawText(kwd.word, kwd.x, kwd.y, kwd.size, kwd.color)
    }
  }

  wx.drawCanvas({
    canvasId: 'wccanvas',
    actions: context.getActions()
  })
}

module.exports.getTopNews = getTopNews