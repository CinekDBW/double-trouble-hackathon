from PIL import Image
import pytesseract
import time
import multiprocessing
import os
import shutil

from cezar import cezar
from findPiece import findPiece


def zadanie2(path):
    filename = path.split('/')[-1]

    im = Image.open(path)
    pix = im.load()
    size = im.size

    dict = {}

    for j in range(size[1]):
        for i in range(size[0]):
            if pix[i, j] not in dict:
                dict[pix[i, j]] = (255, 255, 255)

    for key in dict.keys():
        foo = (key[0] - 1, key[1] - 1, key[2] - 1)
        if foo in dict.keys():
            dict[key] = (0, 0, 0)

    for j in range(size[1]):
        for i in range(size[0]):
            pix[i, j] = dict[pix[i, j]]

    im.save(f'temp/{filename.split(".")[0]}Decoded.{filename.split(".")[1]}')

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    output = pytesseract.image_to_string(f'temp/{filename.split(".")[0]}Decoded.{filename.split(".")[1]}', lang='pol')
    output = output.replace('\n', ' ').replace('\r', '')
    outputPostCezar = cezar(output)
    indexes = findPiece(outputPostCezar)
    if (indexes[1] == -1):
        print("decoding failed successfully")

    if not os.path.exists("./output"):
        os.mkdir('./output')

    with open(f'output/{filename.split(".")[0]}.txt', 'w') as f:
        f.write(f'{indexes[0]} {indexes[1]}')


def main(path):
    start = time.time()
    if not os.path.exists("temp"):
        os.mkdir('temp')

    p = multiprocessing.Process(target=zadanie2, name="Foo", args=(path,))
    p.start()
    p.join(30)

    if p.is_alive():
        print("program is running too long, let's kill it...")

        p.terminate()
        p.join()

    if os.path.exists("temp"):
        shutil.rmtree('temp', ignore_errors=True)

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    path = 'input/szyfr_2.png'
    main(path)
