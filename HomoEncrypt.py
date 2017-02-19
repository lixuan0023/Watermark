import gmpy2
from gmpy2 import mpz

class HomoEnc(object):
    """docstring for HomoEnc"""
    def __init__(self, seed):
        super(HomoEnc, self).__init__()

        # seed = 99999
        state = gmpy2.random_state(1)
        tmp1 = gmpy2.mpz_random(state,mpz('999999999999999'))
        tmp2 = gmpy2.mpz_random(state,mpz('999999999999999'))
        p = gmpy2.next_prime(tmp1)  #generate random prime number
        q = gmpy2.next_prime(tmp2)

        N = p*q

        k = gmpy2.mpz_random(state,mpz('99'))
        g = gmpy2.mpz_random(state,mpz('99'))
        g_k = g**k

        ####private parameters
        self.N = N
        self.k = k
        ###public parameters
        self.random_state = state
        self.PP = {'p':p,'g':g,'g_k':g_k}


    def KeyGen(self):
        p = self.PP['p']
        g = self.PP['g']
        state = self.random_state
        x = gmpy2.mpz_random(state,mpz('99'))
        g_x = g**x

        return {'pk':g_x,'sk':x}

    def ReKeyGen(self,sk_s,pk_b):
        g_k = self.PP['g_k']
        k = self.k
        g_tk = pk_b**k
        g_sk = g_k**sk_s
        rk_sb = g_tk/g_sk

        return rk_sb

    def Enc(self,pk,m):
        state = self.random_state
        p = self.PP['p']
        r = gmpy2.mpz_random(state,mpz('99'))
        N = self.N
        k = self.k
        print(m)
        enc_m = (m + r * p) % N
        b = g_k = self.PP['g_k']
        g_xk = pk**k
        a = g_xk * enc_m

        return {'a':a,'b':b}

    def ReEnc(self,rk,c):
        enc_m = c['a']
        enc_m2 = enc_m*rk

        return {'a':enc_m2,'b':c['b']}

    def Dec(self,sk,c):
        p = self.PP['p']
        a = c['a']
        b = c['b']
        m = a/(b**sk)%p


        return m

    def Mul(self,c1,c2):
        a = c1['a']*c2['a']
        b = c1['b']*c2['b']

        return {'a':a,'b':b}

if __name__ == '__main__':
    hm = HomoEnc(1)
    S_key = hm.KeyGen()
    B_key = hm.KeyGen()
    m = mpz(2009)
    c = hm.Enc(S_key['pk'],m)
    mes = hm.Dec(S_key['sk'],c)
    print(mes,type(mes))

