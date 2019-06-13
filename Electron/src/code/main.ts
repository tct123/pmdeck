import { app, BrowserWindow } from "electron";
import * as path from "path";

let mainWindow: Electron.BrowserWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    height: 600,
    width: 800,
    frame: false,
  });

  mainWindow.loadFile(path.join(__dirname, "../src/html/index.html"));

  //mainWindow.webContents.openDevTools();

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  const { ipcMain } = require('electron')
    ipcMain.on('ondragstart', (event:any, filePath:any) => {
        event.sender.startDrag({
            file: filePath,
            icon: ''
        })
    })
}

app.on("ready", createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (mainWindow === null) {
    createWindow();
  }
});

import "./server-communication";