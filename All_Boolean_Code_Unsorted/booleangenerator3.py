# import numpy as np
import os

dirname = "OCT4"
topo = """Source Target Type
miR200 ZEB {}
ZEB miR200 {}
ZEB ZEB {}
SNAIL miR200 {}
SNAIL ZEB {}
OCT4 miR200 {}
miR145 OCT4 {}
OCT4 miR145 {}
miR145 ZEB {}
ZEB miR145 {}"""
idsfile = """node id
SNAIL 0
ZEB 1
OCT4 2
miR200 3
miR145 4
"""


dict={
  "GRHL2": 7,
  "GRHL2wa": 8,
  "OVOL2": 9,
  "OVOLsi": 8,
  "NRF2": 16,
  "OCT4": 10,
  "GRHL2f": 7
}


num_edges = dict[dirname]

try:
    os.mkdir(dirname)
except:
    pass

for i in range(num_edges):
    for j in range(i+1, num_edges):
        for pew in range(j+1, num_edges):
            temp = [2]*num_edges
            temp[i] = 1
            temp[j] = 1
            temp[pew] = 1
            tempstr = topo.format(*temp).split("\n")
            finstr = ""
            # print(tempstr)
            # exit(0)
            p = open("{}/{}{}{}_{}.topo".format(dirname, i+1, j+1, pew+1, 0), "w")
            p.write(topo.format(*temp))
            p.close()
            q = open("{}/{}{}{}_{}.ids".format(dirname, i+1, j+1, pew+1, 0), 'w')
            q.write(idsfile)
            q.close()
            for k in range(1,num_edges + 1):
                finstr = ""
                for l in tempstr:
                    if l != tempstr[k]:
                        finstr += l + "\n"
                # print(finstr)
                p = open("{}/{}{}{}_{}.topo".format(dirname, i+1, j+1, pew + 1, k), 'w')
                p.write(finstr)
                p.close()
                q = open("{}/{}{}{}_{}.ids".format(dirname, i+1, j+1, pew + 1, k), 'w')
                q.write(idsfile)
                q.close()
                # exit(0)


#TEMPLATE LIST:
# in order: GRHL2, OVOL2, OVOLsi, GRHL2wa, OCT4, NRF2

str='''
GRHL2
dirname = "GRHL2"
topo = """Source Target Type
miR200 ZEB {}
ZEB miR200 {}
ZEB ZEB {}
SNAIL miR200 {}
SNAIL ZEB {}
ZEB GRHL2 {}
GRHL2 ZEB {}"""
idsfile = """node id
SNAIL 0
ZEB 1
GRHL2 2
miR200 3
"""


OVOL
dirname = "OVOL2"
topo = """Source Target Type
miR200 ZEB {}
ZEB miR200 {}
ZEB ZEB {}
SNAIL miR200 {}
SNAIL ZEB {}
ZEB OVOL2 {}
OVOL2 ZEB {}
OVOL2 OVOL2 {}
OVOL2 miR200 {}"""
idsfile = """node id
SNAIL 0
ZEB 1
OVOL2 2
miR200 3
"""

OVOLsi
dirname = "OVOLsi"
topo = """Source Target Type
miR200 ZEB {}
ZEB miR200 {}
ZEB ZEB {}
SNAIL miR200 {}
SNAIL ZEB {}
ZEB OVOL2 {}
OVOL2 ZEB {}
OVOL2 miR200 {}"""
idsfile = """node id
SNAIL 0
ZEB 1
OVOL2 2
miR200 3
"""

GRHL2wa
dirname = "GRHL2wa"
topo = """Source Target Type
miR200 ZEB {}
ZEB miR200 {}
ZEB ZEB {}
SNAIL miR200 {}
SNAIL ZEB {}
ZEB GRHL2 {}
GRHL2 ZEB {}
GRHL2 GRHL2 {}"""
idsfile = """node id
SNAIL 0
ZEB 1
GRHL2 2
miR200 3
"""

OCT4
dirname = "OCT4"
topo = """Source Target Type
miR200 ZEB {}
ZEB miR200 {}
ZEB ZEB {}
SNAIL miR200 {}
SNAIL ZEB {}
OCT4 miR200 {}
miR145 OCT4 {}
OCT4 miR145 {}
miR145 ZEB {}
ZEB miR145 {}"""
idsfile = """node id
SNAIL 0
ZEB 1
OCT4 2
miR200 3
miR145 4
"""

NRF2
dirname = "NRF2"
topo = """Source Target Type
X SNAIL {}
miR34 SNAIL {}
SNAIL SNAIL {}
SNAIL miR34 {}
SNAIL miR200 {}
SNAIL ZEB {}
miR200 ZEB {}
miR200 KEAP1 {}
ZEB ZEB {}
ZEB miR34 {}
ZEB miR200 {}
ZEB Ecadherin {}
Ecadherin ZEB {}
Ecadherin NRF2 {}
KEAP1 NRF2 {}
NRF2 SNAIL {}"""
idsfile = """node id
X 0
SNAIL 1
ZEB 2
Ecadherin 3
miR200 4
miR34 5
KEAP1 6
NRF2 7
"""

'''
