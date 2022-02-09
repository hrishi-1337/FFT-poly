import time
import random
from math import sin,cos,pi


def generator(n):
    a, b = [], []
    for i in range(0,n):
        n1 = random.randint(-50,50)
        n2 = random.randint(-50,50)
        a.append(n1)
        b.append(n2)
    return a, b
 
def  naive(a, b, n):
    ans = [0] * (2 * n - 1);
    for i in range(n):
        for j in range(n):
            ans[i + j] += a[i] * b[j]; 
    return ans;

def dft(a):

    n = len(a)
    if n == 1:
        return [a[0]]
    theta = 2*pi/n
    w = list( complex(cos(theta*i), sin(theta*i)) for i in range(n) )
    Aeven = a[0::2]
    Aodd  = a[1::2]
    Yeven = dft(Aeven)
    Yodd = dft(Aodd) 
    Y = [0]*n    
    middle = n//2
    for k in range(n//2):
        w_yodd_k  = w[k] * Yodd[k]
        yeven_k   =  Yeven[k]         
        Y[k]          =  yeven_k  +  w_yodd_k
        Y[k + middle] =  yeven_k  -  w_yodd_k     
    return Y


def idft(a):

    n = len(a)
    if n == 1:
        return [a[0]]
    theta = 2*pi/n
    w = list( complex(cos(theta*i), sin(theta*i)) for i in range(n))
    Aeven = a[0::2]
    Aodd  = a[1::2]
    Yeven = idft(Aeven)
    Yodd = idft(Aodd) 
    Y = [0]*n    
    middle = n//2
    for k in range(n//2):
        w_yodd_k  = Yodd[k]/w[k]
        yeven_k   =  Yeven[k]         
        Y[k]          =  yeven_k  +  w_yodd_k
        Y[k + middle] =  yeven_k  -  w_yodd_k  
    return Y


def main():
    n = 10
    t = 10
    norm_time = {}
    fft_time = {}
    while n > 1:
        a, b = generator(n)
        print("Polynomial 1: "+str(a))
        print("Polynomial 2: "+str(b))


        start_time1 = time.time()
        ans1 = naive(a, b, n)
        end_time1 = time.time()     
        print("Naive polynomial multiplication result: "+str(ans1));
        n_time = round(end_time1 - start_time1, 6);
        print("Time elapsed: %f seconds" %n_time)
        if norm_time.has_key(n):
            norm_time[n] = norm_time[n] + n_time
        else:
            norm_time[n] = n_time


        ans_dft = [0]*(n*2)
        for i in range(n):
            a.append(0)
            b.append(0)
        start_time2 = time.time()
        a_dft = dft(a)
        b_dft = dft(b)
        for i in range(n*2):
            ans_dft[i] = a_dft[i] * b_dft[i]
        ans2 =  idft(ans_dft)    
        ans2 = [(x//(n*2)).real for x in ans2] 
        end_time2 = time.time()     
        print("Naive polynomial multiplication result: "+str(ans2));
        f_time = round(end_time2 - start_time2, 6);
        print("Time elapsed: %f seconds" %f_time)
        if fft_time.has_key(n):
            fft_time[n] = fft_time[n] + f_time
        else:
            fft_time[n] = f_time   

        t-=1
        if t == 0:
            n-=1
            t=10


def test():
    a = [1, 3, 5, 11]
    b = [2, 4, 6 ,9]
    n = len(a);    
    ans_dft = [0]*(n*2)

    ans1 = naive(a, b, n)  
    print("Naive polynomial multiplication result: "+str(ans1));

    for i in range(n):
        a.append(0)
        b.append(0)

    print("Polynomial 1: "+str(a))
    print("Polynomial 2: "+str(b))
    a_dft = dft(a)
    b_dft = dft(b)
    print("A DFT: "+str(a_dft))
    print("B DFT: "+str(b_dft))  
    for i in range(n*2):
        ans_dft[i] = a_dft[i] * b_dft[i]
    print("Ans DFT: "+str(ans_dft))
    ans2 =  idft(ans_dft)    
    ans2 = [(x//(n*2)).real for x in ans2] 
    print("Ans DFT: "+str(ans2))

if __name__ == "__main__":
    main()


