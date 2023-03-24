const path = require('path');
const { app, BrowserWindow } = require('electron');

const isDev = process.env.NODE_ENV !== 'production';
const isMac = process.platform === 'darwin';

// create the main window
function createMainWindow() {
  const mainWindow = new BrowserWindow({
    title: 'Vage',
    width: 1200,
    height: 720,
    minWidth: 940,
    minHeight: 560,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#852d91',
      symbolColor: '#f4f4f4',
      height: 30,
    },
    autoHideMenuBar: true,
    icon: __dirname + '/renderer/images/logo.png',
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      // preload: path.join(__dirname, 'preload.js'),
    }
  });

  // Open devtools if in dev env
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.loadFile(path.join(__dirname, './renderer/index.html'));
}

app.whenReady().then(() => {
  createMainWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== isMac) {
    app.quit()
  }
})