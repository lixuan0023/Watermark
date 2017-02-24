import cv2
import numpy as np

imgName = "Lena.png"
img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)

imf = np.float32(img)

Trans = cv2.dct(imf) #dct forward

dct = Trans*(10**6)
dct_int = np.int32(dct)

print(Trans[88][88])
print(dct_int[88][88])
