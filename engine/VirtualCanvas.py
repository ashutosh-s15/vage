import cv2
import numpy as np
import os
import HandTrackingModule as htm

class virtualCanvas:
    def __init__(self):
        self.drawThickness = 15
        self.eraserThickness = 50
        self.currTool = 'pen'
        self.shape = 'rectangle'
        self.fillShape = True
        self.n = 0
        self.temp = False

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

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        self.detector = htm.handDetector(detectionCon=0.85)
        self.xp, self.yp = 0, 0
        self.imgCanvas = np.zeros((720, 1280, 3), np.uint8)

    def run(self):
        while True:
            success, img = self.cap.read()
            img = cv2.flip(img, 1)

            # Find Hand landmarks
            img = self.detector.findHands(img)
            lmList = self.detector.findPosition(img, draw=False)

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

                    if x1 > 1188:
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

                    if self.xp == 0 and self.yp == 0:
                        self.xp, self.yp = x1, y1

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
                          ## update eraser thickness
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

            # Adding header/toolbar to canvas
            img[0:125, 0:1280] = self.header

            # Adding stroke-width panel to canvas
            img[206:514, 1188:1280] = self.strokeWidthPanel

            # Adding clear button to canvas
            img[544:636, 1188:1280] = self.clearButton

            # Adding logo to canvas
            img[650:710, 10:70] = self.logo

            cv2.imshow("Image", img)
            # cv2.imshow("Canvas", imgCanvas)
            cv2.waitKey(1)

def main():
    # Initiating virtual canvas instance
    canvas = virtualCanvas()
    canvas.run()

main()

