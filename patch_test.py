#from scipy.stsci import convolve
import numpy as np

rounds = 450
patch1 = {(0,2):0.30,
          (1,1):0.50,
          (2,0):0.20}

patch2 = {(0,1):0.50,
          (1,0):0.50}

patch3 = {(0,0):1.00}

curpatch = patch3.copy() # np.zeros((rounds*2+1, rounds*2+1))

armies1 = 300
armies2 = 300

# curpatch[0][0] = 1

# print curpatch

# out = convolve.convolve2d(curpatch, patch)

#print out

def add(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

for x in range(rounds):
    newpatch = {}
    for k,v in curpatch.items():
        patch = patch1
        if armies1-k[0] <= 0 or armies2-k[1] <= 0:
            patch = patch3
        elif armies1-k[0] == 1 or armies2-k[1] == 1:
            patch = patch2
        for k2,v2 in patch.items():
            nk = add(k,k2)
            if v > 0 and v2 > 0:
                newpatch[nk] = newpatch.get(nk, 0.00) + v*v2
    curpatch = newpatch

for k in curpatch:
    print "%-10s %#02.8f " % (k, curpatch[k]*100)

acc = 0
for r in curpatch:
    acc += curpatch[r]

print acc
