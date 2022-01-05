import multiprocessing
import pyautogui
import time

global lastCoords
lastCoords = 450
def move_left():
    #print('left')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')


def move_right():
    #print('right')
    pyautogui.keyDown('d')
    pyautogui.keyUp('d')


def shoot():
    while True:
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')


def getPlayerPosition(im):
    for x in range(0, im.size[0]):
        # print(im.getpixel((x,im.size[1]-5)))
        if ((im.getpixel((x, im.size[1] - 5)) == (255, 0, 0) or im.getpixel((x, im.size[1] - 5)) == (
                255, 255, 255)) and (
                im.getpixel((x + 8, im.size[1] - 5)) == (255, 0, 0) or im.getpixel((x + 8, im.size[1] - 5)) == (
                255, 255, 255))):
            global lastCoords
            if(lastCoords-x!=0):
                 print(abs(lastCoords-x))
            lastCoords=x
            return x


def getHairs(playerCoords, im):  # wysokosc na ktorej zaczyna sie zawodnik
    for y in range(0, 20):
        if (im.getpixel((playerCoords, im.size[1] - 5 - y)) == (20, 20, 20)):
            return im.size[1] - 5 - y + 1


def isTubeSafe(playerCoords, hairs, im, height, width):
    listOfY = [12, 42, 70]
    for y in listOfY:
        for x in range(-1, width, 8):
            pix = im.getpixel((playerCoords + x, hairs - y))
            if (pix[0] == pix[1] == pix[2]):
                pass
            else:
                return False
        pix = im.getpixel((playerCoords + width, hairs - y))
        if (pix[0] == pix[1] == pix[2]):
            pass
        else:
            return False
    return True


def move(playerCoords, hairs, im, height):
    baseWidth = 60
    if isTubeSafe(playerCoords, hairs, im, height, baseWidth):
        if(playerCoords>600):
            if ((playerCoords >= 48) and (isTubeSafe(playerCoords - 48, hairs, im, height, baseWidth + 8))):
                move_left()
        elif(playerCoords<300):
            if ((playerCoords <= (960 - baseWidth - 48)) and (isTubeSafe(playerCoords + 40, hairs, im, height, 67))):
                move_right()
    else:
        if ((playerCoords <= (960 - baseWidth - 48)) and (isTubeSafe(playerCoords + 40, hairs, im, height, 67))):
            move_right()
        elif ((playerCoords >= 48) and (isTubeSafe(playerCoords - 48, hairs, im, height, baseWidth + 8))):
            move_left()
        else:
            pass
            # print('dytnka')
            # move_left()
            # move_left()


def main():
    hairs = 0
    doOnce = True
    while True:
        while (pyautogui.locateOnScreen('canvas.png', grayscale=True, confidence=0.2) != None):
            time.sleep(2)
            pyautogui.hotkey('ctrl', 'f5')
            canvasState = pyautogui.locateOnScreen('canvas.png', confidence=0.2)
            if canvasState != None:
                while True:
                    im = pyautogui.screenshot(region=(canvasState.left, canvasState.top, canvasState.width,
                                                      canvasState.height))
                    # im.save('zrzut.png')

                    if (doOnce):
                        hairs = getHairs(getPlayerPosition(im), im)
                        doOnce = False
                    move(getPlayerPosition(im), hairs, im, 80)


if __name__ == '__main__':
    q = multiprocessing.Process(target=main, name="Main")
    q.start()

    p = multiprocessing.Process(target=shoot, name="Foo")
    p.start()
