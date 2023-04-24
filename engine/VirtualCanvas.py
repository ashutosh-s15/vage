import os
import time
from tkinter import filedialog
import cv2
import numpy as np
import HandTrackingModule as htm
from StateManager import stateManager

class imageImport:
    def __init__(self, filePath):
        self.filePath = filePath
        self.imageArray = cv2.imread(filePath)
        print(self.imageArray)
        self.pos = [300, 200]
        self.shape = self.imageArray.shape

    def resize(self, canvasSize):
        """Resize image import if larger than the canvas"""
        if self.shape[0] >= canvasSize[1] or self.shape[1] >= canvasSize[0]:
          aspectRatio = float(self.shape[1]) / float(self.shape[0])
          newWidth = int(canvasSize[0] * 1/4)
          newHeight = int(newWidth / aspectRatio)

          self.imageArray = cv2.resize(self.imageArray, (newWidth, newHeight))
          self.shape = self.imageArray.shape

    def printInfo(self):
        """Print instance information"""
        print("File Path:", self.filePath)
        print("Image Array Shape:", self.imageArray.shape)
        print("Current position:", self.pos)
        print("Shape Member Variable:", self.shape) 

class virtualCanvas:
    def __init__(self):
        self.canvasSize = (1280, 595) # (canvasWidth, canvasHeight)
        self.drawThickness = 15
        self.eraserThickness = 50
        self.currTool = 'pen'
        self.shape = 'rectangle'
        self.fillShape = True
        self.n = 0
        self.temp = False

        self.time_limit = 5
        # Get the current time
        self.start_time = time.time()

        currDirPath = os.getcwdb().decode()

        assetsPath = currDirPath + "\engine\Images\Assets"
        myAssets = os.listdir(assetsPath)
        logoImage = cv2.imread(f'{assetsPath}/{myAssets[1]}')
        self.logo = logoImage
        clearButtonImage = cv2.imread(f'{assetsPath}/{myAssets[0]}')
        self.clearButton = clearButtonImage

        headerPath = currDirPath + "\engine\Images\Header"
        myList = os.listdir(headerPath)
        self.overlayList = []
        for imgPath in myList:
            image = cv2.imread(f'{headerPath}/{imgPath}')
            self.overlayList.append(image)
        self.header = self.overlayList[0]
        self.drawColor = (255, 255, 255)

        strokeWidthPanelPath = currDirPath + "\engine\Images\StrokeWidthPanel"
        myList = os.listdir(strokeWidthPanelPath)
        self.panelList = []
        for imgPath in myList:
            image = cv2.imread(f'{strokeWidthPanelPath}/{imgPath}')
            self.panelList.append(image)
        self.strokeWidthPanel = self.panelList[1]

        sidebarPath = currDirPath + "\engine\Images\Sidebar"
        myList = os.listdir(sidebarPath)
        self.sidebarList = []
        for imgPath in myList:
            image = cv2.imread(f'{sidebarPath}/{imgPath}')
            self.sidebarList.append(image)
        self.sidebar = self.sidebarList[0]

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        self.canvasState = stateManager() # Initiating canvas state instance

        self.detector = htm.handDetector(detectionCon=0.85)
        self.xp, self.yp = 0, 0
        self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        self.importsState = stateManager() # Initiating imports state instance
    def createImageImport(self):
        filePath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")])
        image = imageImport(filePath)
        image.resize(self.canvasSize)
        self.importsState.addState(image)

    def selectImageImport(self, imports, img, x1, y1):
        currentIndex = self.importsState.current_state
        currentImport = imports[currentIndex]

        # Update selected or current image import's position values
        currentImport.pos[0] = x1
        currentImport.pos[1] = y1

        # currentImport.imageArray = cv2.resize(currentImport.imageArray, (x1-x0, y0-y1))
        # currentImport.shape = currentImport.imageArray.shape
        
        # Highlight the selected image import
        cv2.rectangle(
            img,
            (currentImport.pos[0], currentImport.pos[1]),
            (currentImport.pos[0] + currentImport.shape[1], currentImport.pos[1] + currentImport.shape[0]),
            (233, 140, 12), 4
        )


    def run(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)

            # Find Hand landmarks
            img = self.detector.findHands(img)
            lmList = self.detector.findPosition(img, draw=False)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('u') or key == ord('U'):
                self.imgCanvas = self.canvasState.prevState()
            if key == ord('r') or key == ord('R'):
                self.imgCanvas = self.canvasState.nextState()

            if key == ord('a') or key == ord('A'):
                self.importsState.prevState()
            if key == ord('s') or key == ord('S'):
                self.importsState.nextState()
            if key == ord('d') or key == ord('D'):
                self.importsState.deleteCurrentState()

            if key == ord('q') or key == ord('Q'):
                break

            # Update image imports' position on canvas
            imports = self.importsState.history
            for imp in imports:
              if imp.pos[1]+imp.shape[0] < 720 and imp.pos[0]+imp.shape[1] < 1280: # Check if the new position is outside the canvas bounds
                img[imp.pos[1]:imp.pos[1]+imp.shape[0], imp.pos[0]:imp.pos[0]+imp.shape[1]] = imp.imageArray

            if len(lmList) != 0:
                # Tip of index and middle fingers
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                x0, y0 = lmList[4][1:]

                # Check which fingers are up
                fingers = self.detector.fingersUp()

                # If selection mode - Two fingers are up
                if fingers[1] and fingers[2]:
                    self.xp, self.yp = 0, 0
                    print(self.currTool)
                    print(self.shape)
                    if y1 < 125:
                        self.sidebar = self.sidebarList[0]
                        if 622 < x1 < 699:
                            if self.currTool == 'pen':
                                self.header = self.overlayList[0]
                            elif self.currTool == 'shape' and self.shape == 'rectangle':
                                self.header = self.overlayList[4]
                            elif self.currTool == 'shape' and self.shape == 'ellipse':
                                self.header = self.overlayList[8]
                            elif self.currTool == 'shape' and self.shape == 'circle':
                                self.header = self.overlayList[12]
                            self.drawColor = (255, 255, 255)
                        elif 723 < x1 < 800:
                            if self.currTool == 'pen':
                                self.header = self.overlayList[1]
                            elif self.currTool == 'shape' and self.shape == 'rectangle':
                                self.header = self.overlayList[5]
                            elif self.currTool == 'shape' and self.shape == 'ellipse':
                                self.header = self.overlayList[9]
                            elif self.currTool == 'shape' and self.shape == 'circle':
                                self.header = self.overlayList[13]
                            self.drawColor = (154, 154, 154)
                        elif 822 < x1 < 899:
                            if self.currTool == 'pen':
                              self.header = self.overlayList[2]
                            elif self.currTool == 'shape' and self.shape == 'rectangle':
                                self.header = self.overlayList[6]
                            elif self.currTool == 'shape' and self.shape == 'ellipse':
                                self.header = self.overlayList[10]
                            elif self.currTool == 'shape' and self.shape == 'circle':
                                self.header = self.overlayList[14]
                            self.drawColor = (0, 0, 255)
                        elif 924 < x1 < 1001:
                            if self.currTool == 'pen':
                                self.header = self.overlayList[3]
                            elif self.currTool == 'shape' and self.shape == 'rectangle':
                                self.header = self.overlayList[7]
                            elif self.currTool == 'shape' and self.shape == 'ellipse':
                                self.header = self.overlayList[11]
                            elif self.currTool == 'shape' and self.shape == 'circle':
                                self.header = self.overlayList[15]
                            self.drawColor = (0, 255, 0)

                        elif 1062 < x1 < 1135:
                            self.header = self.overlayList[0]
                            self.currTool = 'pen'
                            self.drawColor = (255, 255, 255)
                        elif 1165 < x1 < 1252:
                            self.header = self.overlayList[16]
                            self.currTool = 'eraser'
                            self.drawColor = (0, 0, 0)

                        elif 491 < x1 < 556 and self.currTool == 'shape':
                            self.fillShape ^= True

                        elif 393 < x1 < 458:
                            self.header = self.overlayList[4]
                            self.currTool = 'shape'
                            self.shape = 'rectangle'
                            self.drawColor = (255, 255, 255)
                        elif 265 < x1 < 340:
                            self.header = self.overlayList[8]
                            self.currTool = 'shape'
                            self.shape = 'ellipse'
                            self.drawColor = (255, 255, 255)
                        elif 150 < x1 < 215:
                            self.header = self.overlayList[12]
                            self.currTool = 'shape'
                            self.shape = 'circle'
                            self.drawColor = (255, 255, 255)

                        elif 27 < x1 < 92:
                            # Saving sketch as image
                            if not self.cap.isOpened():
                                break

                            os.makedirs('data/temp', exist_ok=True)
                            base_path = os.path.join('data/temp', 'camera_capture')
                            print("saving...")

                            cv2.imwrite('{}_{}.{}'.format(base_path, self.n, 'jpg'), img)
                            self.n += 1

                    if 30 < x1 < 90:
                        if 164 < y1 < 224:
                            self.sidebar = self.sidebarList[1]
                            self.currTool = 'addImage'
                            if time.time() - self.start_time > self.time_limit:
                              self.createImageImport()
                              self.start_time = time.time()
                        if 260 < y1 < 320:
                            self.sidebar = self.sidebarList[2]
                            self.currTool = 'selectImport'
                        if 360 < y1 < 420:
                            self.sidebar = self.sidebarList[3]
                            self.currTool = 'addCanvas'

                    if x1 > 1188:
                        self.sidebar = self.sidebarList[0]
                        if 209 < y1 < 280:
                            self.strokeWidthPanel = self.panelList[0]
                            self.drawThickness = 8
                        elif 286 < y1 < 357:
                            self.strokeWidthPanel = self.panelList[1]
                            self.drawThickness = 16
                        elif 363 < y1 < 434:
                            self.strokeWidthPanel = self.panelList[2]
                            self.drawThickness = 24
                        elif 440 < y1 < 511:
                            self.strokeWidthPanel = self.panelList[3]
                            self.drawThickness = 36

                        elif 544 < y1 < 636:
                            # Clear canvas
                            self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)

                    cv2.rectangle(img, (x1, y1-25), (x2, y2+25), self.drawColor, cv2.FILLED)

                # If drawing mode - Index finger is up
                if fingers[1] and fingers[2] == False:
                    cv2.circle(img, (x1, y1), 15, self.drawColor, cv2.FILLED)

                    # Capture current state of canvas in history
                    self.canvasState.addState(np.copy(self.imgCanvas))

                    if self.xp == 0 and self.yp == 0:
                        self.xp, self.yp = x1, y1

                    if self.currTool == 'selectImport' and len(imports) > 0:
                        self.selectImageImport(imports, img, x1, y1)

                    if self.currTool == 'shape' and self.shape == 'circle':
                        z1, z2 = lmList[4][1:]
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        if result < 0:
                            result = -1 * result
                        u = result
                        cv2.circle(img, (x0, y0), u, self.drawColor)
                        if fingers[4] and self.temp:
                            if self.fillShape:
                                cv2.circle(self.imgCanvas, (x0, y0), u, self.drawColor, cv2.FILLED)
                            else:
                                cv2.circle(self.imgCanvas, (x0, y0), u, self.drawColor)

                            self.temp = False
                        elif fingers[4] == 0:
                            self.temp = True

                    if self.currTool == 'shape' and self.shape == 'ellipse':
                        z1, z2 = lmList[4][1:]
                        a = z1 - x1
                        b = (z2 - x2)
                        if x1 > 250:
                            b = int(b / 2)
                        if a < 0:
                            a = -1 * a
                        if b < 0:
                            b = -1 * b
                        cv2.ellipse(img, (x1, y1), (a, b), 0, 0, 360, 255, 0)

                        if fingers[4] and self.temp:
                            if self.fillShape:
                                cv2.ellipse(self.imgCanvas, (x1, y1), (a, b), 0, 0, 360, self.drawColor, cv2.FILLED)
                            else:
                                cv2.ellipse(self.imgCanvas, (x1, y1), (a, b), 0, 0, 360, self.drawColor, self.drawThickness)

                            self.temp = False
                        elif fingers[4] == 0:
                            self.temp = True

                    if self.currTool == 'shape' and self.shape == 'rectangle':
                        z1, z2 = lmList[4][1:]
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        if result < 0:
                            result = -1 * result
                        u = result
                        cv2.rectangle(img, (x0, y0), (x1, y1), self.drawColor)

                        if fingers[4] and self.temp:
                            if self.fillShape:
                                cv2.rectangle(self.imgCanvas, (x0, y0), (x1, y1), self.drawColor, cv2.FILLED)
                            else:
                                cv2.rectangle(self.imgCanvas, (x0, y0), (x1, y1), self.drawColor)

                            self.temp = False
                        elif fingers[4] == 0:
                            self.temp = True

                    elif self.currTool == 'eraser' and self.drawColor == (0, 0, 0):
                        self.eraserThickness = 50
                        z1, z2 = lmList[4][1:]
                        result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                        if result < 0:
                          result = -1 * result
                        u = result
                        if fingers[1] and fingers[4]:
                          ## Update eraser thickness
                          self.eraserThickness = u

                        cv2.line(img, (self.xp, self.yp), (x1, y1), self.drawColor, self.eraserThickness)
                        cv2.line(self.imgCanvas, (self.xp,self. yp), (x1, y1), self.drawColor, self.eraserThickness)
                    elif self.currTool == 'pen':
                        cv2.line(img, (self.xp, self.yp), (x1, y1), self.drawColor, self.drawThickness)
                        cv2.line(self.imgCanvas, (self.xp, self.yp), (x1, y1), self.drawColor, self.drawThickness)

                    self.xp, self.yp = x1, y1

                # if not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and fingers[4]:
                #     cv2.destroyAllWindows()

            imgGray = cv2.cvtColor(self.imgCanvas, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img, imgInv)
            img = cv2.bitwise_or(img, self.imgCanvas)

            # Add header/toolbar to canvas
            img[0:125, 0:1280] = self.header

            # Add Sidebar to canvas
            img[125:720, 0:120] = self.sidebar

            # Add stroke-width panel to canvas
            img[206:514, 1188:1280] = self.strokeWidthPanel

            # Add clear button to canvas
            img[544:636, 1188:1280] = self.clearButton

            # Adding logo to canvas
            # img[650:710, 10:70] = self.logo

            cv2.imshow("Image", img)
            # cv2.imshow("Canvas", imgCanvas)
            cv2.waitKey(1)

def main():
    # Initiating virtual canvas instance
    canvas = virtualCanvas()
    canvas.run()

main()

