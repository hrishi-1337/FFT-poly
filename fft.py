import time
import random
import pandas as pd

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
    n = 1000
    t = 10
    norm_time = {}
    fft_time = {}
    while n > 10:
        a, b = generator(n)
        padding = 0

        print("N: "+str(n))
        start_time1 = time.time()
        ans1 = naive(a, b, n)
        end_time1 = time.time()     
        # print("Naive polynomial multiplication result: "+str(ans1));
        n_time = round(end_time1 - start_time1, 6);
        # print("Naive time elapsed: %f seconds" %n_time)
        if n in norm_time:
            norm_time[n] = norm_time[n] + n_time/n
        else:
            norm_time[n] = n_time/n

        for i in range (0,13):
            if n == pow(2,i):
                padding = n
                break;
            elif n < pow(2,i):
                padding = pow(2,i+1) - n
                break;

        ans_dft = [0]*(n+padding)
        for i in range(padding):
            a.append(0)
            b.append(0)
        start_time2 = time.time()
        a_dft = dft(a)
        b_dft = dft(b)
        for i in range(n+padding):
            ans_dft[i] = a_dft[i] * b_dft[i]
        ans2 =  idft(ans_dft)    
        ans2 = [round((x/(n+padding)).real) for x in ans2] 
        end_time2 = time.time()     
        # print("FFT polynomial multiplication result: "+str(ans2));
        f_time = round(end_time2 - start_time2, 6);
        # print("FFT time elapsed: %f seconds" %f_time)
        if n in fft_time:
            fft_time[n] = fft_time[n] + f_time/n
        else:
            fft_time[n] = f_time/n   

        t-=1
        if t == 0:
            n-=1
            t=10

    df_1 = pd.DataFrame(norm_time.items()) 
    df_2 = pd.DataFrame(fft_time.items()) 
    writer = pd.ExcelWriter('output.xlsx')
    df_1.to_excel(writer, 'NormTime')
    df_2.to_excel(writer, 'FFTTime')
    writer.save()

if __name__ == "__main__":
    main()


