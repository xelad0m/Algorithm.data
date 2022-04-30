class Queue():
    def __init__(self, size, repr=0):
        self.size = size
        self.length = 0     # current len of queue
        self.cost = 0       # cost of enqueued
        self.full = False
        self.empty = True
        self._queue = [-1] * self.size
        self._back = 0      # points empty to push
        self._front = 0     # points not empty to pop
        self._repr = repr

    def front(self):
        return self._queue[self._front]

    def pushBack(self, key):
        if self.full:
            return -1
        else:
            self._queue[self._back] = key       
            self._back = (self.size + self._back - 1) % self.size
            self.length += 1
            self.cost += key
            self.full = True and (self.length == self.size)
            self.empty = False and self.empty
            return self.cost - key
            

    def popFront(self):
        if not self.empty:
            key = self._queue[self._front]
            self._queue[self._front] = -1
            self._front = (self.size + self._front - 1) % self.size
            self.length -= 1
            self.cost -= key
            self.empty = True and (self.length == 0)
            self.full = False and self.full


    def update(self, d_time):
        if d_time >= self.cost:
            self.__init__(self.size, repr=self._repr)    # release queue
        else:
            while d_time:
                if self.front() <= d_time:
                    d_time = d_time - self.front()
                    self.popFront()
                else:
                    self._queue[self._front] -= d_time
                    self.cost -= d_time     
                    d_time = 0

        if self._repr: print("\n{}".format(self), end=' ')

    
    def __repr__(self):
        l = self._repr
        pretify = lambda x: "[{}]".format(' '*(l - len(str(x))) + str(x) if x >= 0 else ' '*l)
        Q = ''
        i = self._front
        while i > self._front - self.size:
            Q += pretify(self._queue[i])
            i -= 1
        return "{} {:>3}/{:<3} ".format(Q, self.length, self.size)

import random
from matplotlib import pyplot as plt

def queue_test(size, intens, mean, d_mean, n_req=10000):                         # intens - поступление (пак/сек), mean - обработка (пак/сек), d_mean - разброс обработки (%)
    # возвращает процент дропнутых пакетов и среднюю заполненность очереди
    A = sorted([random.randint(0, n_req // intens) for _ in range(n_req)])      # времена поступления 
    dm =  mean * d_mean // 100
    D = [random.randint(n_req // (mean - dm), n_req // (mean + dm) ) for _ in range(n_req)]    # длительность обслуживания
    dropped = 0
    S = [0] * n_req

    q = Queue(size)
    
    q.update(A[0] - 0)
    Di = q.pushBack(D[0])
    Ai = A[0] + Di if Di != -1 else -1
    if Ai == -1: dropped += 1
    S[0] = q.length
    for i in range(1, n_req):
        q.update(A[i] - A[i-1])
        Di = q.pushBack(D[i])
        Ai = A[i] + Di if Di != -1 else -1
        S[i] = q.length
        if Ai == -1: dropped += 1
    
    dropped = dropped / n_req
    workload = sum(S) / len(S)
    return dropped, workload

k, j = 1, 3
size = [x for x in range(1,10)]
intens = [y for y in range(1,10) for x in size]
size = size * (len(intens)//len(size))
mean = [x for x in intens]
d_mean = [0 for x in mean]

z = [queue_test(s, i, m, dm)[0] for s, i, m, dm in zip(size, intens, mean, d_mean)]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(size, intens, z, s=10)
plt.grid(True)
plt.show()