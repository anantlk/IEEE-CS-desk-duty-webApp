
from data.bitmaps import bitmap

CHARACTERS = "abcdefghijklmnpqrstuvwxyz123456789"

def solve_captcha(img):
    captcha = ""
    img = img.convert('L')
    pix = img.load()
    for y in range(1, 44):
        for x in range(1, 179):
            if pix[x, y - 1] == 255 and pix[x, y] == 0 and pix[x, y + 1] == 255:
                pix[x, y] = 255
            if pix[x - 1, y] == 255 and pix[x, y] == 0 and pix[x + 1, y] == 255:
                pix[x, y] = 255
            if pix[x, y] != 255 and pix[x, y] != 0:
                pix[x, y] = 255
    for j in range(30, 181, 30):
        cropped_img = img.crop((j - 30, 12, j, 44))
        pix1 = cropped_img.load()
        matches = {}
        for char in CHARACTERS:
            match = 0
            black = 0
            pix2 = bitmap[char]
            for y in range(0, 32):
                for x in range(0, 30):
                    if pix1[x, y] == pix2[y][x] and pix2[y][x] == 0:
                        match += 1
                    if pix2[y][x] == 0:
                        black += 1
            perc = float(match) / float(black)
            matches.update({perc: char[0].upper()})
        try:
            captcha += matches[max(matches.keys())]
        except ValueError:
            captcha += "0"
    return captcha
