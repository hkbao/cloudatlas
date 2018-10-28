var canvasWidth = wx.getSystemInfoSync().windowWidth - 40
var canvasHeight = 220
var animationInverval = null

var kwlist = []
var colors = ['9,187,7', '53,53,53', '136,136,136', '87,107,149', '230,67,64', '0,0,204', '0,102,51', '153,51,204', '255,153,51']
var app = getApp()

function kwdata(text, size, color, x, y, speed) {
  this.text = text;
  this.size = size;
  this.color = color;
  this.x = x
  this.y = y
  this.speed = speed
}

var getRandomColor = function () {
  return colors[Math.floor(Math.random() * colors.length)]
}

var getInitialX = function(text, size, width) {
  return Math.floor(Math.random() * (width - text.length * size))
}

var getInitialY = function (index, height) {
  return Math.floor(Math.random() * (height + 10 * index))
}

var getRandomSpeed = function() {
  return 6 + Math.floor(Math.random() * 5)
}

var drawCloud = function(keywords) {
  for (let x = 0; x < Math.min(keywords.length, 50); x++) {
    let text = keywords[x][0]
    let size = Math.min(120, Math.floor(keywords[x][1] * 200 + 18))
    kwlist.push(new kwdata(text, size, getRandomColor(),
      getInitialX(text, size, canvasWidth), getInitialY(x, canvasHeight), getRandomSpeed()))
  }
  animationInverval = setInterval(buildWordCloud, 20)
}

var buildWordCloud = function() {
  var context = wx.createCanvasContext('cloudcanvas')

  function drawText(text, size, color, x, y, y_factor) {
    if (y < -100 || y > canvasHeight + 100) {
      return
    }

    context.setFontSize(size)
    context.setFillStyle('rgba(' + color + ',' + (0.25 + 0.75 * y_factor) + ')')
    context.fillText(text, x, y)
    //context.setGlobalAlpha(0.5 + Math.abs(Math.sin((y*2/canvasHeight) * 3.14/2)))
  }

  for (let x = 0; x < kwlist.length; x++) {
    let kw = kwlist[x]
    let y_factor = Math.sin(Math.PI * kw.y / canvasHeight)
    kw.y -= (kw.speed - (3 + 2 * y_factor))
    if (kw.y < 0) {
      kw.x = getInitialX(kw.text, kw.size, canvasWidth)
      kw.y = canvasHeight + getInitialY(100, canvasHeight)
      kw.speed = getRandomSpeed()
      kw.color = getRandomColor()
    }
    drawText(kw.text, kw.size, kw.color, kw.x, kw.y, y_factor)
  }

  wx.drawCanvas({
    canvasId: 'cloudcanvas',
    actions: context.getActions()
  })
}

var stopAnimation = function() {
  clearInterval(animationInverval)
  kwlist = []
}

module.exports = { drawCloud: drawCloud, stopAnimation: stopAnimation}