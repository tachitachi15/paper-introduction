import numpy as np
import matplotlib.pyplot as plt

N = 512
L = 512
K = 5

R = 50
v = np.array([1,1,2,2,3])
phi = [np.pi,np.pi/2,np.pi/3,np.pi/4,np.pi/5]

f0 = 24.0 * 10 **9

fsweep = 1.0 * 10**6
Tchirp = 1.0 * 10**-3
c = 3.0 * 10**8

fB = - fsweep/Tchirp/c*R*2
fD = -2 * v * f0/c

sig = np.zeros((N*L,),dtype=complex)
for l in range(L):
    for k in range(K):
        for n in range(l*N,(l+1)*N):
            sig[n] += np.exp(2*1j*np.pi*(fB*float(n/N*0.001)-fD[k]*l*Tchirp+phi[k]))

sig = np.reshape(sig,(N,L))
S_f = np.abs(np.fft.fft2(sig))

def draw(data,cb_min,cb_max):
    X,Y=np.meshgrid(np.arange(data.shape[1]),np.arange(data.shape[0]))
    plt.figure() 
    div=20.0       
    delta=(cb_max-cb_min)/div
    interval=np.arange(cb_min,abs(cb_max)*2+delta,delta)[0:int(div)+1]
    plt.contourf(X,Y,data,interval)
    plt.show()

draw(S_f,-2,32)

