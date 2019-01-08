const { app, BrowserWindow } = require('electron')

let win

app.on('ready', () => {
    win = new BrowserWindow({ width: 1600, height: 900 })

    win.loadFile('index.html')
})
