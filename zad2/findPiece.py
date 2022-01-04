def findIndex(text, lines):
    wordIndex = -1
    bestScore = 0
    bestIndex = 0
    for index in range(len(lines)):
        if (index == 0 or lines[index - 1] == ' '):
            wordIndex += 1
            currentScore = 0
            for subindex in range(len(lines) - index):
                if (subindex == len(text)):
                    break
                if (text[subindex] == lines[index + subindex]):
                    currentScore += 1
                elif (subindex + 1 < len(text) and text[subindex + 1] == lines[
                    index + subindex]):
                    subindex += 1
                    currentScore += 1
                elif (subindex + 2 < len(text) and text[subindex + 2] == lines[
                    index + subindex]):
                    subindex += 2
                    currentScore += 1

            if (currentScore > bestScore):
                bestScore = currentScore
                bestIndex = wordIndex
    return bestIndex, bestScore


def listToString(l):
    output = ''
    for item in l:
        output += item
        output += ' '
    return output[0:-1]


def findPiece(text):
    with open('w_pustyni_i_w_puszczy.txt', encoding="utf8") as file:
        lines = file.read()

    bestIndex, bestScore = findIndex(text, lines)
    words = lines.split()
    goodPiece = words[bestIndex:bestIndex + len(text.split())]
    wynik = bestIndex, bestIndex + len(text.split()) - findIndex(text[::-1], listToString(goodPiece)[::-1])[0] - 1

    return wynik