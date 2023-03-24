import cv2
import numpy as np
import os
import HandTrackingModule as htm

###########################
drawThickness = 15
eraserThickness = 50
currTool = 'pen'
shape = 'rectangle'
fillShape = True
n = 0
temp = False
###########################

currDirPath = os.getcwdb().decode()

assetsPath = currDirPath + "\engine\Images\Assets"
myAssets = os.listdir(assetsPath)
logoImage = cv2.imread(f'{assetsPath}/{myAssets[1]}')
logo = logoImage
clearButtonImage = cv2.imread(f'{assetsPath}/{myAssets[0]}')
clearButton = clearButtonImage


headerPath = currDirPath + "\engine\Images\Header"
myList = os.listdir(headerPath)
overlayList = []
for imgPath in myList:
    image = cv2.imread(f'{headerPath}/{imgPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (255, 255, 255)

strokeWidthPanelPath = currDirPath + "\engine\Images\StrokeWidthPanel"
myList = os.listdir(strokeWidthPanelPath)
panelList = []
for imgPath in myList:
    image = cv2.imread(f'{strokeWidthPanelPath}/{imgPath}')
    panelList.append(image)

strokeWidthPanel = panelList[1]

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find Hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Tip of index and middle fingers
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        x0, y0 = lmList[4][1:]

        # Check which fingers are up
        fingers = detector.fingersUp()

        # If selection mode - Two fingers are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print(currTool)
            print(shape)
            if y1 < 125:
                if 622 < x1 < 699:
                    if currTool == 'pen':
                        header = overlayList[0]
                    elif currTool == 'shape' and shape == 'rectangle':
                        header = overlayList[4]
                    elif currTool == 'shape' and shape == 'ellipse':
                        header = overlayList[8]
                    elif currTool == 'shape' and shape == 'circle':
                        header = overlayList[12]
                    drawColor = (255, 255, 255)
                elif 723 < x1 < 800:
                    if currTool == 'pen':
                        header = overlayList[1]
                    elif currTool == 'shape' and shape == 'rectangle':
                        header = overlayList[5]
                    elif currTool == 'shape' and shape == 'ellipse':
                        header = overlayList[9]
                    elif currTool == 'shape' and shape == 'circle':
                        header = overlayList[13]
                    drawColor = (154, 154, 154)
                elif 822 < x1 < 899:
                    if currTool == 'pen':
                        header = overlayList[2]
                    elif currTool == 'shape' and shape == 'rectangle':
                        header = overlayList[6]
                    elif currTool == 'shape' and shape == 'ellipse':
                        header = overlayList[10]
                    elif currTool == 'shape' and shape == 'circle':
                        header = overlayList[14]
                    drawColor = (0, 0, 255)
                elif 924 < x1 < 1001:
                    if currTool == 'pen':
                        header = overlayList[3]
                    elif currTool == 'shape' and shape == 'rectangle':
                        header = overlayList[7]
                    elif currTool == 'shape' and shape == 'ellipse':
                        header = overlayList[11]
                    elif currTool == 'shape' and shape == 'circle':
                        header = overlayList[15]
                    drawColor = (0, 255, 0)

                elif 1062 < x1 < 1135:
                    header = overlayList[0]
                    currTool = 'pen'
                    drawColor = (255, 255, 255)
                elif 1165 < x1 < 1252:
                    header = overlayList[16]
                    currTool = 'eraser'
                    drawColor = (0, 0, 0)

                elif 491 < x1 < 556 and currTool == 'shape':
                    fillShape ^= True
                elif 393 < x1 < 458:
                    header = overlayList[4]
                    currTool = 'shape'
                    shape = 'rectangle'
                    drawColor = (255, 255, 255)
                elif 265 < x1 < 340:
                    header = overlayList[8]
                    currTool = 'shape'
                    shape = 'ellipse'
                    drawColor = (255, 255, 255)
                elif 150 < x1 < 215:
                    header = overlayList[12]
                    currTool = 'shape'
                    shape = 'circle'
                    drawColor = (255, 255, 255)

                elif 27 < x1 < 92:
                    # Saving sketch as image
                    if not cap.isOpened():
                        break;

                    os.makedirs('data/temp', exist_ok=True)
                    base_path = os.path.join('data/temp', 'camera_capture')
                    print("saving...")

                    cv2.imwrite('{}_{}.{}'.format(base_path, n, 'jpg'), img)
                    n += 1

            if x1 > 1188:
                if 209 < y1 < 280:
                    strokeWidthPanel = panelList[0]
                    drawThickness = 8
                elif 286 < y1 < 357:
                    strokeWidthPanel = panelList[1]
                    drawThickness = 16
                elif 363 < y1 < 434:
                    strokeWidthPanel = panelList[2]
                    drawThickness = 24
                elif 440 < y1 < 511:
                    strokeWidthPanel = panelList[3]
                    drawThickness = 36

                elif 544 < y1 < 636:
                    # Clear canvas
                    imgCanvas = np.zeros((720, 1280, 3), np.uint8)

            cv2.rectangle(img, (x1, y1-25), (x2, y2+25), drawColor, cv2.FILLED)

        # If drawing mode - Index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if currTool == 'shape' and shape == 'circle':
                z1, z2 = lmList[4][1:]
                result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                if result < 0:
                    result = -1 * result
                u = result
                cv2.circle(img, (x0, y0), u, drawColor)
                if fingers[4] and temp:
                    if fillShape:
                        cv2.circle(imgCanvas, (x0, y0), u, drawColor, cv2.FILLED)
                    else:
                        cv2.circle(imgCanvas, (x0, y0), u, drawColor)

                    temp = False
                elif fingers[4] == 0:
                    temp = True

            if currTool == 'shape' and shape == 'ellipse':
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

                if fingers[4] and temp:
                    if fillShape:
                        cv2.ellipse(imgCanvas, (x1, y1), (a, b), 0, 0, 360, drawColor, cv2.FILLED)
                    else:
                        cv2.ellipse(imgCanvas, (x1, y1), (a, b), 0, 0, 360, drawColor, drawThickness)

                    temp = False
                elif fingers[4] == 0:
                    temp = True

            if currTool == 'shape' and shape == 'rectangle':
                z1, z2 = lmList[4][1:]
                result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                if result < 0:
                    result = -1 * result
                u = result
                cv2.rectangle(img, (x0, y0), (x1, y1), drawColor)

                if fingers[4] and temp:
                    if fillShape:
                        cv2.rectangle(imgCanvas, (x0, y0), (x1, y1), drawColor, cv2.FILLED)
                    else:
                        cv2.rectangle(imgCanvas, (x0, y0), (x1, y1), drawColor)

                    temp = False
                elif fingers[4] == 0:
                    temp = True

            elif currTool == 'eraser' and drawColor == (0, 0, 0):
                eraserThickness = 50
                z1, z2 = lmList[4][1:]
                result = int(((((z1 - x1) ** 2) + ((z2 - y1) ** 2)) ** 0.5))
                if result < 0:
                  result = -1 * result
                u = result
                if fingers[1] and fingers[4]:
                  ## update eraser thickness
                  eraserThickness = u

                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            elif currTool == 'pen':
                cv2.line(img, (xp, yp), (x1, y1), drawColor, drawThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, drawThickness)

            xp, yp = x1, y1

        # if not fingers[0] and not fingers[1] and not fingers[2] and not fingers[3] and fingers[4]:
        #     cv2.destroyAllWindows()

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Adding header/toolbar to canvas
    img[0:125, 0:1280] = header

    # Adding stroke-width panel to canvas
    img[206:514, 1188:1280] = strokeWidthPanel

    # Adding clear button to canvas
    img[544:636, 1188:1280] = clearButton

    # Adding logo to canvas
    img[650:710, 10:70] = logo

    cv2.imshow("Image", img)
    # cv2.imshow("Canvas", imgCanvas)
    cv2.waitKey(1)