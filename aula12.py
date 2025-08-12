import cv2 as cv
import numpy as np

path = "caminho da pasta"
img = cv.imgread(path+'GTR.jpg', 0)

blur = cv.blur(img, (5,5))

sx = cv.Sobel(blur, cv.CV_32F, 1, 0, ksize = 3)
sy = cv.Sobel(blur, cv.CV_32F, 0, 1, ksize = 3)
mag = cv.magnitude(sx, sy)
mag = cv.convertScaleAbs(mag)

_, th = cv.threshold(mag, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

kernel = cv.getStructuringElement(cv.MORPH_CLOSE, (3,3))
closed = cv.morphologyEx(th, cv.MORPH_CLOSE, kernel, interations=2)

conts, _ = cv.findCountours(closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

mask = np.zeros(img.shape, dtype = np.uint8)  #cria matriz com mesmo tamanho da imagem para usar de máscara.
cv.drawCountours(mask, conts, -1, 255, cv.FILLED)
seg = cv.bitwise_and(img, img, mask=mask)

res = np.hstack([th, mag])

cv.imshow('res', res)
cv.waitKey(0)
cv.destroyAllWindows()
