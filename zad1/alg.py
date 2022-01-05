import cv2
import time
import os

METHOD = cv2.TM_SQDIFF_NORMED

results = []

PATH = 'C:/PG/hack/zad1/f1'

FRAGMENT = cv2.imread(PATH + '.png', cv2.IMREAD_GRAYSCALE)

ans = {}

def templateMatchScore(matching):
    return cv2.minMaxLoc(matching)

def templateMatchPhoto(small_img, big_img):
    matching = cv2.matchTemplate(small_img, big_img, METHOD)
    return matching


def calcPosition(name: str, depth: int, re_min: float, im_min: float, re_max: float, im_max: float, my_name):
    # print(f'{name}->{depth} => {my_name}')

    if depth == 5:
        return

    ans[name] = (re_min, im_min, re_max, im_max)

    fourth = (re_max - re_min) / 4
    new_depth = depth + 1

    calcPosition(name + "0", new_depth, re_min + fourth, im_min, re_max, im_max - fourth, my_name)

    calcPosition(name + "1", new_depth, re_min, im_min, re_max - fourth, im_max - fourth, my_name)

    calcPosition(name + "2", new_depth, re_min, im_min + fourth, re_max - fourth, im_max, my_name)

    calcPosition(name + "3", new_depth, re_min + fourth, im_min + fourth, re_max, im_max, my_name)


def findRecursively(n, filename):
    if n > 4:
        return
    image = cv2.imread(f'C:/PG/hack/zad1/img/{filename}.png', cv2.IMREAD_GRAYSCALE)

    if not os.path.exists(f'C:/PG/hack/zad1/img/{filename}.png'):
         return

    # blackout(image, 224)
    matching = templateMatchPhoto(FRAGMENT, image)
    score = templateMatchScore(matching)
    results.append((score[0], score[3], filename))



    for i in range(4):
        findRecursively(n + 1, filename + str(i))


def resizeImg(src, ratio=0.5):
    dsize = (int(src.shape[0]*ratio), int(src.shape[1]*ratio))
    resized = cv2.resize(src, dsize)
    return resized


def mark_pattern(img, big_img, score):
    w = img.shape[1]
    h = img.shape[0]
    # minMax cos tam gowno

    return [score[3][0], score[3][1], w, h]

    # return cv2.rectangle(big_img, score[3], (score[3][0] + w, score[3][1] + h), (0, 255, 255), 2)

# def second_try(img):
#
#     #
#     # for po wielkosciach:
#     #
#     #
#     # threshold = .60
#     # yloc, xloc = np.where(result >= threshold)
#     #
#     # # for (x, y) in zip(xloc, yloc):
#     # #     cv2.rectangle(farm_img, (x, y), (x + w, y + h), (0, 255, 255), 2)
#     #
#     #
#     # for (x, y) in zip(xloc, yloc):
#     #     rectangles.append([int(x), int(y), int(w), int(h)])
#     #     rectangles.append([int(x), int(y), int(w), int(h)])
#
#     half = len(rectangles)
#     rectangles, weights = cv2.groupRectangles(rectangles, half , 0.2)


def maciek():
    start = time.time()

    big_image = cv2.imread(f'C:/PG/hack/zad1/img/0.png', cv2.IMREAD_GRAYSCALE)
    small_image = cv2.imread(f'C:/PG/hack/zad1/f1.png', cv2.IMREAD_GRAYSCALE)

    rectangles = []


    tmp = small_image
    for i in range(5):


        result = templateMatchPhoto(tmp, big_image)
        score = templateMatchScore(result)
        rectangles.append(mark_pattern(tmp, big_image, score))
        tmp = resizeImg(tmp)


        print(score)

    half = len(rectangles) // 2

    print(rectangles)

    color = (0,255,0)

    for r in rectangles:
        print(r[0], r[1], r[2], r[3])
        cv2.rectangle(big_image, (r[0], r[1]), (r[2], r[3]), color, 1)

    cv2.imshow("skdfjsl",big_image)
    cv2.waitKey(0)

    rectangles, weights = cv2.groupRectangles(rectangles, half, 0.2)

    print(rectangles)



    print(time.time() - start)


def main():

     start = time.time()
     findRecursively(0, '0')
     results.sort()

     calcPosition('0', 0, -1, -1, 1, 1, results[0][2])

     # print(ans[results[0][2]])
     # print(ans['02322'])
     # print(results)

     selected = ''

     for k in results:
         if len(k[2]) == 5:
             selected = ans[k[2]]
             break

     print(selected)
     print(time.time() - start)

     precission = 5

     with open(PATH + ".txt", 'w') as f:
        f.write(str("%.5f"%round(selected[0], precission)))
        f.write("\n")
        f.write(str("%.5f"%round(selected[2], precission)))
        f.write("\n")
        f.write(str("%.5f"%round(selected[1], precission)))
        f.write("\n")
        f.write(str("%.5f"%round(selected[3], precission)))
        f.write("\n")
        f.write(str(int((time.time() - start) * 1000.)))





if __name__ == '__main__':
    main()


