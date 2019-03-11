import numpy as np
from netCDF4 import Dataset
import sys

filename=sys.argv[1]

with Dataset(filename,'r',) as root:
    P=np.array(root["PSFC"][:])
    Q=np.array(root["Q2"][:])
    T=np.array(root["T2"][:])

RH=(0.263*P*Q)/np.exp(17.67*(T-273.15)/(T-29.65))
np.clip(RH,0,100,out=RH)
print(RH.shape)
print(RH[0,0:10])
print(np.max(RH),np.min(RH))
