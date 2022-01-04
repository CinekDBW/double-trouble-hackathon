alphabet = 'aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż'
LEN = len(alphabet)

def get_letter(l: str, shift: int) -> str:
    new_l = ((alphabet.index(l) + LEN) - shift) % LEN
    return alphabet[new_l]

def decode(text: str, words):
    text = text.lower()
    possible = []

    for shift in range(0,LEN):
        new_str = ''
        for l in text:
            if alphabet.find(l) == -1:
                new_str += l
            else:
                new_str += get_letter(l, shift)


        possible.append(new_str)
    return possible

def get_result(encoded, words):
    points = [0 for i in range(LEN)]

    for l in range(len(encoded)):
        for word in encoded[l]:
            if word in words:
                points[l] += 1

    for i in range(LEN):
        if points[i] == max(points):
            return encoded[i]

def cezar(text):
    lines = []
    with open('w_pustyni_i_w_puszczy.txt', encoding="utf8") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
        lines = [line.split() for line in lines]

    words = []

    for line in lines:
        for word in line:
            words.append(word)

    words = set(words)

    encrypted = decode(text, words)
    output = (get_result(encrypted, words))
    return output
