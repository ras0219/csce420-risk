#from scipy.stsci import convolve
import numpy as np

patch32 = {(0,2):0.3716,
          (1,1):0.3358,
          (2,0):0.2926}
patch22 = {(0,2):0.3716,
          (1,1):0.3358,
          (2,0):0.2926}
patch31 = {(0,1):0.4167,
          (1,0):0.5833}
patch21 = {(0,1):0.4167,
          (1,0):0.5833}
patch11 = {(0,1):0.4167,
          (1,0):0.5833}

patch00 = {(0,0):1.00}

def add(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def utility(a1, a2, L):
    if a1-L[0] == 0:
        # We lost, so not very util
        #return L[1]/a2 # Spite factor; how much we like killin' other people
        return 0
    return 1 #( - (L[0]*1.0/a1))


def runsim(armies1, armies2):
    rounds = min((armies1,armies2))/2 + max((armies1,armies2))
    curpatch = patch00.copy() # np.zeros((rounds*2+1, rounds*2+1))

    for x in range(rounds):
        newpatch = {}
        for k,v in curpatch.items():
            patch = patch32
            if armies2-k[1] == 1:
                patch = patch31
            if armies1-k[0] == 2:
                patch = patch22
                if armies2-k[1] == 1:
                    patch = patch21
            elif armies1-k[0] == 1:
                patch = patch11
            if armies1-k[0] == 0 or armies2-k[1] == 0:
                patch = patch00
            for k2,v2 in patch.items():
                nk = add(k,k2)
                if v > 0 and v2 > 0:
                    newpatch[nk] = newpatch.get(nk, 0.00) + v*v2
        curpatch = newpatch
    return curpatch

for m in range(1,80):
    for m2 in range(50,51):
        armies1 = m
        armies2 = m2
        curpatch = runsim(armies1, armies2)

        util = 0
        for k in curpatch:
#        print "%-10s %#02.8f %01.8f" % (k, curpatch[k]*100, utility(armies1, armies2, k))
            util += curpatch[k]*utility(armies1, armies2, k)

#    acc = 0
#    for r in curpatch:
#        acc += curpatch[r]

        print "%4d %4d %8.4f %s" % (armies1,armies2,util*100,''.join(['-']*int((util)*100)))
#    print acc
#    print util


