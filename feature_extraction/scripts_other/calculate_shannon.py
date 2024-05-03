from math import log as ln

def p(n, N):
    """ Relative abundance """
    if n == 0:
        return 0
    else:
        return (float(n)/N)**2
    # * ln(float(n)/N)     

wordFormDict = {'bergf': 23, "bergf+n": 3, "bergf+s": 1}
N = sum(wordFormDict.values()) 

# print(-sum(p(n, N) for n in wordFormDict.values() if n != 0))
print(sum(p(n, N)  for n in wordFormDict.values() if n != 0))