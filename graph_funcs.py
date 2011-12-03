import itertools

# regions :: [String] -> {String:[String]} -> [[String]]
def regions(countries, elist):
    regs = map(lambda x: [x], countries)
    rem = []
    while len(regs) > 0:
        r = regs.pop()
        expand = True
        while expand:
            expand = False
            endregs = []
            for y in regs:
                joined = False
                for c in itertools.product(r,y):
                    if c[0] in elist[c[1]]:
                        joined = True
                        break
                if joined:
                    r += y
                    expand = True
                else:
                    endregs.append(y)
            regs = endregs
        rem.append(r)
    return rem

# border :: [String] -> {String:[String]} -> [String]
def border(countries, elist):
    b = set()
    for c in countries:
        for e in elist[c]:
            b.add(e)
    return list(b - set(countries))


if __name__ == '__main__':
    elist = {0:[1,2,3,4,5],1:[0,2],2:[0,1,3,4],3:[0,2],4:[0,2,5],5:[0,4,6],6:[5]}
    countries = [1,2,3,5,6]
    print regions(countries, elist)

    print border(countries, elist)
