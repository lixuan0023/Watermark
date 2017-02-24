from EncWatermark import EncWatermark
import cv2
import numpy as np

def DCT(imgName):
    img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)
    imf = np.float32(img)
    Trans = cv2.dct(imf) #dct forward
    return Trans

def IDCT(dct):
    iTrans = cv2.dct(dct,flags=cv2.DCT_INVERSE) #dct inverse
    dst =  np.uint8(iTrans)
    return dst

ew = EncWatermark(99)
PP = ew.Setup(512)
S_key = ew.KeyGen(PP)
B_key = ew.KeyGen(PP)

img_dct = DCT("Lena.png")
# print(img_dct[0][1])

rk = ew.ReKeyGen(PP,S_key['sk'],B_key['pk'])

c1 = ew.ImgEnc(PP,S_key['pk'],img_dct,[])

c2 = ew.ImgReEnc(PP,rk,c1)

m = ew.ImgDec(PP,B_key['sk'],c2)

img = IDCT(m)

cv2.imshow('dct',img)

cv2.waitKey(0)
cv2.destroyAllWindows()



