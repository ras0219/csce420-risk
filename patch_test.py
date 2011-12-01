#from scipy.stsci import convolve
import numpy as np

rounds = 120
patch1 = [[0, 0, 0.30],
         [0, 0.50, 0],
         [0.20, 0, 0]]

patch2 = [[0, 0.50],
         [0.50, 0]]

patch3 = [[1]]

curpatch = [[1]] # np.zeros((rounds*2+1, rounds*2+1))

armies1 = 50
armies2 = 20

# curpatch[0][0] = 1

# print curpatch

# out = convolve.convolve2d(curpatch, patch)

#print out

for x in range(rounds):
    size = len(patch1)+len(curpatch)-1
    newpatch = [[0 for x in range(size)] for y in range(size)]
    for r in range(len(curpatch)):
        for c in range(len(curpatch[r])):
            patch = patch1
            if armies1-r <= 0 or armies2-c <= 0:
                patch = patch3
            elif armies1-r == 1 or armies2-c == 1:
                patch = patch2

            for r2 in range(len(patch)):
                for c2 in range(len(patch[r2])):
                    newpatch[r+r2][c+c2] += patch[r2][c2] * curpatch[r][c]
    curpatch = newpatch

for r in range(min([len(curpatch),armies1+1])):
    for c in range(min([len(curpatch[r]),armies2+1])):
        print "%#02.2f " % (curpatch[r][c]*100),
    print ""

acc = 0
for r in curpatch:
    for c in r:
       acc += c

print acc
