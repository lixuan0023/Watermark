import cv2
import numpy as np

imgName = "Lena.png"
img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)

imf = np.float32(img)

Trans = cv2.dct(imf) #dct forward
iTrans = cv2.dct(Trans,flags=cv2.DCT_INVERSE) #dct inverse

dst =  np.uint8(iTrans)

cv2.imshow('dct',dst)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
