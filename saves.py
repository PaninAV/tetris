import music


def set_saves(accepts):
    file = open("save.txt", "r")
    for i in range(0, 4):
        s = file.readline()
        k = 0
        for j in s:
            if j == '0':
                accepts[i][k] = False
            elif j == '1':
                accepts[i][k] = True
            k += 1
    file.close()
    return accepts


def set_new_save(difficult, level):
    file = open("save.txt", "r")
    data = file.readlines()
    file.close()
    file = open("save.txt", "w+")
    k = 0
    for line in data:
        i = 0
        difficult_line_saves = ""
        for value in line:
            if value == "1" or value == "0":
                if k == difficult and i == level:
                    difficult_line_saves += '1'
                else:
                    difficult_line_saves += value
            i += 1
        k += 1
        file.write(difficult_line_saves + '\n')
    file.close()


def set_zero_saves():
    file = open("save.txt", "w+")
    for i in range(4):
        file.write("0000\n")
    file.close()
    music.new_sound.play()
