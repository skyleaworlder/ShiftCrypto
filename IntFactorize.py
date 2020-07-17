'''
1. Quadratic Sieve
python IntFactorize.py --QuadSieve/-qs [<number>] [<base-num>]
eg. python IntFactorize.py --QuadSieve 110 100
    python IntFactorize.py -qs 11004 100

2. Pollard Rho
python IntFactorize.py --Rho/-r [<mode>] [<number>]
eg. python IntFactorize.py --Rho --origin 110
    python IntFactorize.py -r --nowadays 110

'''
import sys
from QuadResidue import legendre
from PrimeTest import Fermat
from ConMod import CMVerify, DIVVerify
from Calcu import GCD
from math import sqrt, ceil
import numpy as np
from functools import reduce

'''
draft of quadratic sieve.
cannot work and perform well for several reasons.
'''
solve = []
class QuadSieve:

    def __init__(self, n):
        self.n = n
        self.p = []
        self.q = []

    def _Y_calcu(self, x, n):
        return (x + ceil(sqrt(n)))**2 - n

    def _DIV_total(self, base, v):
        ret = v
        cnt = 0
        while DIVVerify(base, ret):
            ret = ret // base
            cnt += 1
        return {
            "ret": ret,
            "cnt": cnt
        }

    def _solve_backTrack(self, coef, ans, layer):
        '''
        back track method
        to find a vector can solve cong_equ
        '''
        global solve
        if layer == ans.shape[1]:
            return
        for i in range(1, -1, -1):
            ans[0][layer] = i
            if (np.mod(np.dot(ans, coef), 2) == np.zeros([ans.shape[0], coef.shape[1]], dtype=int)).all() \
                and (np.array(ans, dtype=int) != np.zeros(ans.shape, dtype=int)).any():
                solve.append(ans[0].tolist())
                #print(ans[0].tolist(), solve)
            #print(layer, "?", ans)
            self._solve_backTrack(coef, ans, layer+1)

    def _solve(self, coef):
        ans = np.zeros([1, coef.shape[0]], dtype=int)
        self._solve_backTrack(coef, ans, layer=0)
        return solve

    def QuadSieve(self, baseNum):
        '''
        V:      vector of Y(x)
        B:      prime bases arr
        Coef:   a matrix(B.len*B.len) of decomped result,
                the same as Coef Matrix in Dixon ALG
        Y:      res
        '''
        global solve
        assert not Fermat(self.n)
        self.V = [self._Y_calcu(x, self.n) for x in range(0, 100)]
        V_tmp = self.V
        self.B = [x for x in range(2, baseNum) if legendre(self.n, x) == 1 and Fermat(x)]

        for base in self.B:
            V_tmp = [self._DIV_total(base, v)["ret"] for v in V_tmp]

        Y_index_arr = [index for index, v in enumerate(V_tmp) if v == 1]
        self.Y = [self.V[index] for index in Y_index_arr]

        ''' div y by base^k if base^k | y '''
        self.Coef = np.zeros([self.Y.__len__(), self.B.__len__()], dtype=int)
        for jndex,y in enumerate(self.Y):
            for index,base in enumerate(self.B):
                self.Coef[jndex][index] = self._DIV_total(base, y)["cnt"]
        self.Coef = np.mod(self.Coef, 2)

        ''' del all 0 rows '''
        res_row = [index for index,val in enumerate(self.Coef.any(axis=1)) if val]
        Y_index_arr = [val for index,val in enumerate(Y_index_arr) if index in res_row]
        self.Coef = self.Coef[res_row, :]

        ''' solve cong_equ(mod 2) '''
        self.R = self._solve(self.Coef)
        #print(self.V, '\n', V_tmp, self.R, solve, Y_index_arr, "???")

        ''' resolve and calcu p_arr, q_arr '''
        for r in self.R:
            Y_index_arr_turn = [val for index,val in enumerate(Y_index_arr) if r[index] != 0]
            square = reduce(lambda x,y : x*self.V[y], Y_index_arr_turn, 1)
            V_2 = [self._Y_calcu(x, self.n)+self.n for x in Y_index_arr_turn]
            square2 = reduce(lambda x,y : x*y, V_2, 1)
            self.p.append(GCD(sqrt(square) + sqrt(square2), self.n))
            self.q.append(GCD(abs(sqrt(square2) - sqrt(square)), self.n))
        print(self.p, '\n', self.q)

'''
Pollard-Rho ALG to decompose a composite number.
n:      the num to decomped
mode:   1. --origin, use f(x) = x^2 - 1 (mod n)
        2. --nowadays, use f(x) = x^2 - 1 (mod n) (default)
        (the second one is recommended)
        (the firset cannot work well in some situations)
'''
class PollardRho:

    def __init__(self, n):
        self.n = n

    def _fx_origin(self, x):
        return (x*x - 1) % self.n

    def _fx_nowadays(self, x):
        return (x*x + 1) % self.n

    '''
    x_0 = 1
    y_0 = f(x_0)
    d = gcd(x, y)

    x <- f(x)
    y <- f(f(y))
    d <- gcd(|x-y|, n)
    '''
    def factoring(self, mode):
        x = 1
        y = self._fx_origin(x) if mode == "--origin" else self._fx_nowadays(x)
        d = GCD(x, y)

        while d == 1:
            x = self._fx_origin(x) if mode == "--origin" else self._fx_nowadays(x)
            y = self._fx_origin(self._fx_origin(y)) if mode == "--origin" else self._fx_nowadays(self._fx_nowadays(y))
            d = GCD(abs(x-y), self.n)

        if d == self.n:
            return -1
        else:
            return d

def main(argv):
    choice = argv[0]
    if choice == "--QuadSieve" or choice == "-qs":
        n = int(argv[1])
        baseNum = int(argv[2])
        qs = QuadSieve(n)
        qs.QuadSieve(baseNum)
    elif choice == "--Rho" or choice == "-r":
        mode = argv[1]
        n = int(argv[2])
        rho = PollardRho(n)
        ans = rho.factoring(mode)
        if ans == -1:
            print("Failure.", n, "might be a prime.")
        else:
            print("Success:", n, "can be decomped to", ans, "and", n // ans)

if __name__ == "__main__":
    main(sys.argv[1:])