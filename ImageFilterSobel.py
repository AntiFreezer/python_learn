from PIL import Image

def image_filter(pixels, i, j, maxx, maxy):
    """оконтуривание с помощью оператора собеля"""
    z = [[0 for j in range(3)] for i in range(3)]
    for k in range(3):
        for m in range(3):
            p = i - 1 + k
            q = j - 1 + m
            if p < 0 or p > maxx - 1 or q < 0 or q > maxy - 1:
                continue
            z[k][m] = int(0.3 * pixels[p, q][0] + 0.59 * pixels[p, q][1] + 0.11 * pixels[p, q][2])

    gx = (z[0][0] + 2 * z[0][1] + z[0][2]) - (z[2][0] + 2 * z[2][1] + z[2][2])
    gy = (z[0][0] + 2 * z[1][0] + z[2][0]) - (z[0][2] + 2 * z[1][2] + z[2][2])
    gr = abs(gx) + abs(gy)

    return gr, int(gr / 1.186), 0


im = Image.open("C://rianna.jpg")
pixels = im.load()  # список с пикселями
maxx, maxy = im.size  # ширина (x) и высота (y) изображения


im1 = Image.new("RGB", (maxx, maxy))
pixels1 = im1.load()

for i in range(maxx):
    for j in range(maxy):
        pixels1[i, j] = image_filter(pixels, i, j, maxx, maxy)

im1.save("C://rianna2.jpg")
