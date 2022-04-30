SAMPLES = "10\n9 7 5 5 2 9 9 9 2 -1", "5\n4 -1 4 1 1", "5\n-1 0 0 0 0", "5\n1 -1 1 1 1", "5\n4 4 4 4 -1", "5\n-1 0 1 2 3", "5\n1 -1 0 2 3", "5\n1 2 3 4 -1"
OUTPUTS = 4, 3, 2, 2, 2, 5, 5, 5

READER = [(x for x in SAMPLES[i].split('\n')) for i in range(len(SAMPLES))]                             # список генераторов входных данных
_input = lambda i=0:  next(READER[i])                                                                   # для эмулятора input()


# put your python code here
from functools import lru_cache

def heightTD(T):
    @lru_cache(maxsize=None)
    def _height(node):
        h = 1
        for i, n in enumerate(T):
            if n == node:
                h = max(h, 1 + _height(i))
        return h
    return _height(T.index(-1))
    
    
def heightGD(T):    # O(n^2)
    h, n = 1, len(T)
    stack = []

    while True:
        core = [False] * n       
        if not stack:
            for i in range(n):
                if T[i] != -1: 
                    core[T[i]] = True
        else:
            while stack:
                i = stack.pop()
                if T[i] != -1:
                    core[T[i]] = True
        for i in range(n):
            if core[i]:
                stack.append(i)
        if len(stack) > 0:
            h = h + 1
        else:
            return h

def height(T):
    n = len(T)
    D = [0] * n             # глубина поддерева с корнем в i

    def fillDepth(i):
        if D[i] > 0:
            return          # уже посчитали...
        if T[i] == -1:
            D[i] = 1    
            return          # ...или добрались до корня
        if D[T[i]] == 0:
            fillDepth(T[i]) # вычислить у родителя...
        
        D[i] = D[T[i]] + 1  # ...добавить потомку высоту родителя + 1

    for i in range(n):
        fillDepth(i)

    h = D[0]
    for i in range(1, n):
        h = max(h, D[i])
    return h



def main():
    n = int(_input())
    T = list(map(int, _input().split()))
    print(height(T))


main()

# tests area
def test(func, i=0):
    n = int(_input(i=i))
    T = list(map(int, _input(i=i).split()))
    return func(T)

test_cases = lambda tester, func: [tester(func, i=case) == out for case, out in enumerate(OUTPUTS[1:], 1)]
test_cases(test, height)


import sys
from time import perf_counter_ns
from matplotlib import pyplot as plt

def timeit(func, *args, n_iter=10):
    t1 = float('inf')
    for _ in range(n_iter):
        t0 = perf_counter_ns()
        func(*args)
        t1 = min(t1, perf_counter_ns() - t0)
    return t1

num = 10 ** 5
import sys
print(sys.getrecursionlimit())
sys.setrecursionlimit(num)
print(sys.getrecursionlimit())
print('__file__: {}'.format(__file__))

funcs = [height]
arg1 = [i+1 for i in range(num-1)] + [-1]
arg2 = [i - 1 for i in range(num)]


for func in funcs:
    t1 = timeit(func, arg1)
    t2 = timeit(func, arg2)
    print(func.__name__, t1)
    plt.bar(func.__name__+' (last)', t1)
    plt.bar(func.__name__+' (first)', t2)
plt.grid(True)
plt.show()



