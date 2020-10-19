import numpy as np
import matplotlib.pyplot as plt
from math import pow
import os
from scipy.stats import norm, zscore
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from scipy.spatial.distance import jensenshannon


arr1=[0,0.0224,0,0.4718,0.4793,0,0.0265,0]
fig, axs = plt.subplots(7)
#plt.figure(figsize=(10,5))
for i in range(1,8):

    probjsd = np.loadtxt("GRHL2_async_unweigh_jsd_{}.txt".format(i))
    arr2=[0]*200
    for j in range(0,200):
        arr2[j]=jensenshannon(arr1,probjsd[j,:])
    #fig.suptitle('Vertically stacked subplots')
    arr3=[t for t in range (0,200)]
    axs[i-1].plot(arr3, arr2)
plt.show()    
plt.savefig("sfsfss.jpg")
    
        