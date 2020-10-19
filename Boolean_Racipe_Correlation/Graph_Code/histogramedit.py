import matplotlib.pyplot as plt
import numpy as np
import numpy as numpy
from scipy import stats
def polyfit(x, y, degree):
    results = {}

    coeffs = numpy.polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = numpy.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = numpy.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = numpy.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = numpy.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results
    
network='OCT4'
dir1='Contv2'
dict={
  "GRHL2": 35,
  "GRHL2wa": 358,
  "OVOL2": 15,
  "OVOLsi": 35,
  "NRF2": 16,
  "OCT4": 356
}

boolean = open("{}_boolean_jsd.txt".format(network), "r").read().split("\n")[1:]
racipe = open("{}_racipe_jsd.txt".format(network), "r").read().split("\n")[1:]

bool_lis = []
boolavg_lis=[]
final_lis = []
avgbool=0
avgrac=0
rac_lis = []
racavg_lis = []
color=[]
coloravg=[]
if "" in boolean:
    boolean.remove("")
# if "" in racipe:
#     racipe.remove("")

# print(boolean)
# print(racipe)
q=0
for i in boolean:
    if(q%3!=0):
        q=(q+1)%3    
        continue
    q=(q+1)%3    
    temp = i.split(" ")[1:]
    temp1 = i.split(" ")[0:]
    temp2=int(temp1[0])
    
    for j in range(len(temp)):
        temp[j] = float(temp[j])
        bool_lis.append(temp[j])
        
        if(temp2==dict[network]):
            color.append('r')
        else:
            color.append('b')
    boolavg_lis.append(sum(temp)/len(temp))      
    if(temp2 == dict[network]):
        avgbool+=sum(temp)/len(temp)    
    if(temp2==dict[network]):
        coloravg.append('r')
    else:
        coloravg.append('b')

# final_lis /= final_lis[13]
if "" in racipe:
    racipe.remove("")
for i in racipe:
     temp = i.split(" ")[1:]
     temp1 = i.split(" ")[0:]
     temp2=int(temp1[0])
     for j in range(len(temp)):
         temp[j] = float(temp[j])
         rac_lis.append(temp[j])
     racavg_lis.append(sum(temp)/len(temp))        
     if(temp2 == dict[network]):
        avgrac+=sum(temp)/len(temp)    
         
#print(len(bool_lis))
#color = ['b']*len(bool_lis)
#color[12] = 'r'
#color = []

#for i in range(len(bool_lis)//7):
 #   if i != dict[network]:
  #      for j in range(7):
   #         color.append('b')
   # else:
    #    for j in range(7):
     #       color.append('r')



x=[0.01* i for i in range(1,40)]
bool_lis=np.array(bool_lis)
rac_lis=np.array(rac_lis)
gradient, intercept, r_value, p_value, std_err = stats.linregress(bool_lis,rac_lis)

plt.scatter(bool_lis,rac_lis,c=color,s=8)

mn=np.min(bool_lis)
mx=np.max(bool_lis)
x1=np.linspace(mn,mx,500)
y1=gradient*x1+intercept
plt.plot(x1,y1,'-r')

print(polyfit(bool_lis,rac_lis,1),r_value**2)

plt.title(r_value**2, loc='center')

plt.savefig("{}/{}_check2.jpg".format(dir1,network))

plt.clf()
x=[0.01* i for i in range(1,40)]
plt.plot(x,x)
plt.scatter(boolavg_lis,racavg_lis,c=coloravg,s=8)
plt.savefig("{}/{}_checkavg2.jpg".format(dir1,network))
plt.clf()

plt.hist(np.array(boolavg_lis)/avgbool, bins = 40)
# plt.plot(x,x)
plt.savefig("{}/{}_boolhist2.jpg".format(dir1,network))
plt.clf()

plt.hist(np.array(racavg_lis)/avgrac, bins = 40)
# plt.plot(x,x)
plt.savefig("{}/{}_rachist.jpg".format(dir1,network))
plt.clf()

