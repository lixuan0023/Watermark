import gmpy2
from gmpy2 import mpz
import numpy as np
import cv2

random_SIZE = 99
alpha = 0.001
amplifier = 10**12
half_amp = 10**6

class EncWatermark(object):
    """docstring for EncWatermark"""
    def __init__(self, seed):
        super(EncWatermark, self).__init__()

        state = gmpy2.random_state(seed)
        self.random_state = state

    def Setup(self,b=1024):
        state = self.random_state

        #generate the random integer between 0~2^b, b=1024,2048,...
        tmp1 = gmpy2.mpz_urandomb(state,b)
        tmp2 = gmpy2.mpz_urandomb(state,b)
        p = gmpy2.next_prime(tmp1)  #generate random prime number
        q = gmpy2.next_prime(tmp2)

        N = p*q
        k = gmpy2.mpz_random(state,random_SIZE)
        g = gmpy2.mpz_random(state,random_SIZE)
        g_k = g**k

        ####private parameters
        self.N = N
        self.k = k
        ###public parameters
        self.PP = {'p':p,'g':g,'g_k':g_k}

        return self.PP

    def KeyGen(self,PP):
        p = PP['p']
        g = PP['g']
        state = self.random_state
        x = gmpy2.mpz_random(state,random_SIZE)
        g_x = g**x

        return {'pk':g_x,'sk':x}

    def ReKeyGen(self,PP,sk_s,pk_b):
        g_k = PP['g_k']
        k = self.k
        g_tk = pk_b**k
        g_sk = g_k**sk_s
        rk_sb = gmpy2.mpq(g_tk,g_sk)

        return rk_sb

    def Enc(self,PP,pk,m):
        state = self.random_state
        p = self.PP['p']
        r = gmpy2.mpz_random(state,random_SIZE)
        N = self.N
        k = self.k
        g_k = self.PP['g_k']
        m_mod = 1
        if m<0:
            m_mod = -m
            b = -g_k
        else:
            m_mod = m
            b = g_k
        enc_m = (m_mod + r * p) % N
        g_xk = pk**k
        a = g_xk * enc_m

        return {'a':a,'b':b}

    def ReEnc(self,rk,c):
        enc_m1 = c['a']
        enc_m2 = enc_m1*rk

        return {'a':enc_m2.numerator,'b':c['b']}

    def Dec(self,PP,sk,c):
        p = self.PP['p']
        a = c['a']
        b = c['b']
        m = 0
        if b<0:
            b_mod = -b
            m_mod = gmpy2.div(a,b_mod**sk)%p
            m = -m_mod
        else:
            b_mod = b
            m_mod = gmpy2.div(a,b_mod**sk)%p
            m = m_mod
        return m

    def Mul(self,c1,c2):
        a = c1['a']*c2['a']
        b = c1['b']*c2['b']

        return {'a':a,'b':b}

    def ImgEnc(self,PP,pk,img_dct,pos_wtm):
        idx = pos_wtm
        size = len(pos_wtm)
        dct = img_dct*amplifier #10**6

        for k in range(size):
            i,j = idx[k]
            dct[i][j] = dct[i][j]/half_amp #10**3

        height, width = dct.shape

        C = []
        for i in range(height):
            row = []
            for j in range(width):
                m = mpz(int(dct[i][j]))
                c = self.Enc(PP,pk,m)
                row.append(c)
            C.append(row)
        return C

    def ImgReEnc(self,PP,rk,dct_enc):
        C = []
        for rows in dct_enc:
            row = []
            for element in rows:
                c = self.ReEnc(rk,element)
                row.append(c)
            C.append(row)
        return C

    def ImgDec(self,PP,sk,dct_enc):
        row = len(dct_enc)
        col = len(dct_enc[0])
        dct = np.zeros((row,col))
        i = 0
        for rows in dct_enc:
            j=0
            for element in rows:
                plaintext = self.Dec(PP,sk,element)
                m = plaintext/amplifier #10**6
                dct[i,j] = m
                j=j+1
            i=i+1
        return np.float32(dct)

    def WatermarkGen(self,size):
        mu,sigma = 0,1
        watermark = np.random.normal(mu,sigma,size)

        return np.float32(watermark)

    def WatermarkPos(self,img_dct,size):
        dct = img_dct.copy()
        dct_ls = np.reshape(dct,-1)
        dct_ls[0] = float('-inf')  #set the DC coefficients
        dct_AC = dct_ls

        idx = np.argsort(dct_AC)[-size:] # the index of the 'size' largest DCT AC coefficients
        idx_2d = [np.unravel_index(idx[x],img_dct.shape) for x in range(idx.size)]

        return idx_2d


    def WatermarkEnc(self,PP,pk,watermark):
        # alpha = 0.001
        w_a_1 = watermark*alpha+1 #(1+alpha*w)*10^6
        wtm = w_a_1*half_amp #10**3
        size_wm = np.size(watermark)
        W = []
        for i in range(size_wm):
            m = mpz(int(wtm[i]))
            c = self.Enc(PP,pk,m)
            W.append(c)
        return W


    def WatermarkEmb(self,dct_enc,watermark,pos):
        dct_copy = dct_enc.copy()
        size = len(pos)

        for i in range(size):
            idx_r,idx_c = pos[i]
            x_i = dct_enc[idx_r][idx_c]
            w_i = watermark[i]
            dct_copy[idx_r][idx_c] = self.Mul(x_i,w_i)
        return dct_copy

    def watermarkExt(self,dct,dct_wtm,size):
        wtmed = dct_wtm.copy()
        dct_ls = np.reshape(wtmed,-1)
        dct_ls[0] = float('-inf')  #set the DC coefficients
        dct_AC = dct_ls

        idx = np.argsort(dct_AC)[-size:] # the index of the 'size' largest DCT AC coefficients
        idx_2d = [np.unravel_index(idx[x],dct_wtm.shape) for x in range(idx.size)]

        # alpha = 0.001
        watermark = np.zeros(size)

        for i in range(size):
            idx = idx_2d[i]
            x_i = dct[idx]
            y_i = dct_wtm[idx]
            delta = y_i - x_i
            alpha_wi = delta/x_i
            w_i = alpha_wi / alpha
            watermark[i] = w_i
        return np.float32(watermark)

#########general function
def DCT(imgName):
    img = cv2.imread(imgName,cv2.IMREAD_GRAYSCALE)
    imf = np.float32(img)
    Trans = cv2.dct(imf) #dct forward
    return Trans

def IDCT(dct):
    iTrans = cv2.dct(dct,flags=cv2.DCT_INVERSE) #dct inverse
    dst =  np.uint8(iTrans)
    return dst

if __name__ == '__main__':
    ew = EncWatermark(99)
    PP = ew.Setup(512)
    S_key = ew.KeyGen(PP)
    B_key = ew.KeyGen(PP)

    img_dct = DCT("Lena.png")
    print(img_dct[0][1])

    size = 10
    watermark = ew.WatermarkGen(size)
    pos = ew.WatermarkPos(img_dct,size)


    wtm_enc = ew.WatermarkEnc(PP,B_key['pk'],watermark)
    img_enc = ew.ImgEnc(PP,B_key['pk'],img_dct,pos)



    img_wtm = ew.WatermarkEmb(img_enc,wtm_enc,pos)
    imgw_enc = ew.ImgDec(PP,B_key['sk'],img_enc)

    print('dct[2,5]',img_dct[2][5])
    print('imgw[2,5]',imgw_enc[2][5])

    w_e = ew.watermarkExt(img_dct,imgw_enc,size)
    print('watermark[0]',watermark[0])
    print('waterExtract[0]',w_e[0])



    # imgw = IDCT(imgw_enc)

    # cv2.imshow('dct',imgw)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()















