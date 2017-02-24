import cv2
import numpy as np

class WatermarkEmbed(object):
    """docstring for WatermarkEmbed"""
    def __init__(self, imgName):
        super(WatermarkEmbed, self).__init__()

        self.img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)
        self.watermark_size = 10
        # self.Trans = None


    def dct(self):
        imf = np.float32(self.img)
        self.Trans = cv2.dct(imf)

    def idct(self,dct):
        iTrans = cv2.dct(dct,flags=cv2.DCT_INVERSE)
        self.dst =  np.uint8(iTrans)
        return self.dst

    def watermarkGen(self):
        mu,sigma,size = 0,1,self.watermark_size
        watermark = np.random.normal(mu,sigma,size)
        self.watermark = np.float32(watermark)
        return self.watermark

    def watermarkEmd(self):
        dct_coefficients = np.copy(self.Trans)
        dct_copy = np.copy(self.Trans)
        dct_ls = np.reshape(dct_copy,-1)
        dct_ls[0] = float('-inf')  #set the DC coefficients
        dct_AC = dct_ls

        watermark = self.watermark
        size = self.watermark_size
        idx = np.argsort(dct_AC)[-size:] # the index of the 'size' largest DCT AC coefficients
        idx_2d = [np.unravel_index(idx[x],dct_copy.shape) for x in range(idx.size)]
        alpha = 0.001

        for i in range(size):
            idx = idx_2d[i]
            x_i = dct_coefficients[idx]
            w_i = watermark[i]

            xw_i = x_i*(1+alpha*w_i)
            dct_coefficients[idx] = xw_i
        return dct_coefficients , idx_2d

    def watermarkExt(self,testImg ,idx_2d):
        dct_coefficients = np.copy(self.Trans)
        # delta  = dct_coefficients - testImg
        alpha = 0.001
        size = self.watermark_size
        watermark = np.zeros(size)
        for i in range(size):
            idx = idx_2d[i]
            x_i = dct_coefficients[idx]
            y_i = testImg[idx]
            delta = y_i - x_i
            alpha_wi = delta/x_i
            w_i = alpha_wi / alpha
            watermark[i] = w_i
        return watermark


if __name__ == '__main__':
    wm = WatermarkEmbed('Lena.png')
    wm.dct()

    waterG = wm.watermarkGen()
    dct,idx_2d = wm.watermarkEmd()
    wE = wm.watermarkExt(dct,idx_2d)
    print(waterG)
    print(wE)

    # imgName = "Lena.png"
    # img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)
    # dst = wm.idct(dct)
    # cv2.imshow('dct',dst)
    # cv2.imshow('image',img)
    # cv2.imshow('diff',img-dst)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()









