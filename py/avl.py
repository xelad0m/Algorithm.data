import sys
import random
from itertools import product

COMMANDS = ['+', '?', '-', 's']

class TestCases():
    def __init__(self, n, mode=0):
        self.n = n
        self.MOD = 10 ** 9 + 1
        self.cases = [k + (0 if random.random() > 0.5 else 1) for k in range(n)]     # одинаковых в среднем 0.5*n
        for i in range(n//20):                                              
            a, b = random.randint(0,n - 1), random.randint(0,n - 1)
            self.cases[a], self.cases[b] = self.cases[b], self.cases[a]              # неупорядочено в среднем 0.05 * n
            self.cases[random.randint(0,n - 1)] += self.MOD                          # превышают модуль в среднем 0.05 * n
        if mode == -1:
            self.cases.reverse()
        elif mode == 0:
            random.shuffle(self.cases)
        
        ws = [50, 10, 10, 35]
        ws = [round(n * x / 100) for x in ws]
        self.operations = ['+'] * ws[0] + ['?'] * ws[1] + ['-'] * ws[2] 
        self.operations = self.operations + ['s'] * (n - len(self.operations))
        random.shuffle(self.operations)
         
    def stream(self):
        def choose(k):
            l = random.randint(0,k//4)
            r = random.randint(l,k) if (l != k) else l
            return (self.cases[l], self.cases[r]) if self.cases[l] % self.MOD <=self.cases[r] % self.MOD else (self.cases[r], self.cases[l])

        yield str(self.n) + '\n'
        for i, cmd in enumerate(zip(self.operations, self.cases)):
            if cmd[0] == 's': arg = choose(i)
            elif cmd[0] == '?': arg = (choose(i)[0], )
            else: arg = (cmd[1],)
            command = (cmd[0],) + arg
            yield ' '.join(list(map(str, command))) + '\n'




from io import StringIO

def check_reference(tree, n=1000, **settings):
    for _ in range(5):
        out, out1 = StringIO(), StringIO()
        cases = [*TestCases(n, mode=0).stream()]
        test_gen, tests_gen1 = (c for c in cases), (c for c in cases)
        tref = run(BSTList, input=test_gen, output=out, **settings)
        t = run(tree, input=tests_gen1, output=out1, **settings)
        # assert out.getvalue() == out1.getvalue()
        out, out1 = out.getvalue(), out1.getvalue()
        if out != out1:
            print(repr(''.join(cases)))
            print(tref)
            t.tree.display()
            return False
    return True


class Drawer():
    def display(self, nfunc=lambda x: x.key):
        if self:
            lines, *_ = self._display_aux(nfunc)
            for line in lines:
                print(line)

    def _display_aux(self, nfunc):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.node.right.node is None and self.node.left.node is None:
            line = '%s' % nfunc(self.node)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.node.right.node is None:
            lines, n, p, x = self.node.left._display_aux(nfunc)
            s = '%s' % nfunc(self.node)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.node.left.node is None:
            lines, n, p, x = self.node.right._display_aux(nfunc)
            s = '%s' % nfunc(self.node)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.node.left._display_aux(nfunc)
        right, m, q, y = self.node.right._display_aux(nfunc)
        s = '%s' % nfunc(self.node)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

class NodeAVL:
    __slots__ = ['key', 'sum', 'size', 'left', 'right']

    def __init__(self, key):
        self.key = key
        self.sum = key
        self.size = 1
        self.left = None
        self.right = None
    
    def __repr__(self):
        return "{}({},{})".format(self.key, self.left or '', self.right or '')

class AVLTreeCore(Drawer):
    __slots__ = ['node', 'height', 'balance']

    def __init__(self):
        self.node = None
        self.height = -1
        self.balance = 0

    def __repr__(self):
        return repr(self.node)

    def fmin(self, node=None):
        if node is None: node = self.node
        while node:
            if node.left.node == None:
                return node
            node = node.left.node

    def fmax(self, node=None):
        if node is None: node = self.node
        while node:
            if node.right.node == None:
                return node
            node = node.right.node

    def add(self, key):
        node = self.node
        if node == None:
            self.node = NodeAVL(key) 
            self.node.left = AVLTreeCore() 
            self.node.right = AVLTreeCore()        
        elif key < node.key: 
            self.node.left.add(key)
        elif key > node.key: 
            self.node.right.add(key)  
        self.rebalance()                                                    # каждое поддерево при выходе из рекурсии

    def rebalance(self):
        self.update_nodes(False)
        while self.balance < -1 or self.balance > 1: 
            if self.balance > 1:
                if self.node.left.balance < 0:  
                    self.node.left.lrotate() # we're in case II
                    self.update_nodes()
                self.rrotate()
                self.update_nodes()
                
            if self.balance < -1:
                if self.node.right.balance > 0:  
                    self.node.right.rrotate() # we're in case III
                    self.update_nodes()
                self.lrotate()
                self.update_nodes()

    def update_nodes(self, recurse=True):
        if self.node: 
            if recurse: 
                if self.node.left: 
                    self.node.left.update_nodes()
                if self.node.right:
                    self.node.right.update_nodes()
            self.height = max(self.node.left.height,
                              self.node.right.height) + 1 
            self.balance = self.node.left.height - self.node.right.height
            self.node.sum = self.node.key + (self.node.left.node.sum if self.node.left.node else 0) + \
                                            (self.node.right.node.sum if self.node.right.node else 0)
            self.node.size = 1 + (self.node.left.node.size if self.node.left.node else 0) + \
                                 (self.node.right.node.size if self.node.right.node else 0)
        else: 
            self.height = -1 
            self.balance = 0

    def rrotate(self):
        # Rotate right pivoting on self 
        A = self.node 
        B = self.node.left.node 
        T = B.right.node 
        
        self.node = B 
        B.right.node = A 
        A.left.node = T 
    
    def lrotate(self):
        # Rotate left pivoting on self 
        A = self.node 
        B = self.node.right.node 
        T = B.left.node 
        
        self.node = B 
        B.left.node = A 
        A.right.node = T 

    def remove(self, key):
        if (self.node != None) and (key != None): 
            if self.node.key == key: 
                if self.node.left.node == self.node.right.node == None:     # потомков нет
                    self.node = None
                elif self.node.left.node == None:                           # один потомок: подтянуть справа
                    self.node = self.node.right.node
                elif self.node.right.node == None:                          # один потомок: подтянуть слева
                    self.node = self.node.left.node
                else:                                                       # два потомка
                    right_min = self.fmin(self.node.right.node)
                    self.node.key = right_min.key 
                    self.node.right.remove(right_min.key)                   # теперь у того уже будет 1 потомок
                self.rebalance()
                return  
            elif key < self.node.key: 
                self.node.left.remove(key)  
            elif key > self.node.key: 
                self.node.right.remove(key)
            self.rebalance()                                                # каждое поддерево при выходе из рекурсии

    def order_statistics(self, k):  # 1-based
        if not self.node or (k < 1) or (k > self.node.size):
            return
        leftsize = self.node.left.node.size if self.node.left.node else 0
        if k == leftsize + 1:
            return self.node.key
        if k < leftsize + 1:
            return self.node.left.order_statistics(k)
        else:
            return self.node.right.order_statistics(k - leftsize - 1)

class AVLTree:
    __slots__ = ['accumulator', 'bormuliator', 'tree', 'usesplit']

    def __init__(self, usesplit=False):
        self.accumulator = 0
        self.bormuliator = lambda x: (x + self.accumulator) % (10 ** 9 + 1)
        self.tree = AVLTreeCore()
        self.usesplit = usesplit

    def add(self, *args):
        self.tree.add(*args)

    def remove(self, *args):
        self.tree.remove(*args)
    
    def display(self, *args, **kwargs):
        self.tree.display(*args, **kwargs)

    def find(self, key):
        node = self.tree.node
        while node:
            if key < node.key:
                node = node.left.node
            elif key > node.key:
                node = node.right.node
            else:
                return node 

    def split(self, key):
        return self._avl_split(self.tree, key)
    
    def merge_w_root(self, t1, t2, t):
        return self._merge_w_root(t1, t2, t)

    def merge(self, t1, t2):
        if t1 == None:
            return
        if t2 == None:
            return
        else:
            node = t1.fmax()
            t = AVLTreeCore()
            t.node = node
            t1.remove(node.key)
            self.tree = self._avl_merge_w_root(t1, t2, t)

    def _merge_w_root(self, t1, t2, t):
        t.node.left = t1 if t1 != None else AVLTreeCore()
        t.node.right = t2 if t2 != None else AVLTreeCore()
        return t

    def _avl_merge_w_root(self, t1, t2, t):
        t1h = t1.height if t1 != None else -1
        t2h = t2.height if t2 != None else -1
        if (t1h - t2h) in (-1, 0, 1):
            t = self._merge_w_root(t1, t2, t)
            t.update_nodes()
            return t
        elif t1h > t2h:
            Tx = self._avl_merge_w_root(t1.node.right, t2, t)
            t1.node.right = Tx
            t1.rebalance()
            return t1
        else:
            Tx = self._avl_merge_w_root(t1, t2.node.left, t)
            t2.node.left = Tx
            t2.rebalance()
            return t2

    def _avl_split(self, t, key):
        if t.node == None:
            return None, None
        if key < t.node.key:
            t1, t2 = self._avl_split(t.node.left, key)
            t2x = self._avl_merge_w_root(t2, t.node.right, t)
            return t1, t2x
        else:
            t1, t2 = self._avl_split(t.node.right, key)
            t1x = self._avl_merge_w_root(t.node.left, t1, t)
            return t1x, t2

    def in_walk(self, tree):
        if tree:
            node = tree.node
            stack = list()
            while stack or node:
                if stack:
                    node = stack.pop()
                    yield node.key
                    node = node.right.node
                while node:
                    stack.append(node)
                    node = node.left.node

    def sum_sum(self, l, r):
        self.accumulator = sum([x for x in self.in_walk(self.tree) if l <= x <= r])
        return self.accumulator  
    
    def sum_split(self, l, r): # чувствительна к l > r
        le, gr = self.split(l-1)
        l1 = le.node.sum if le != None else 0
        self.merge(le, gr)
        le, gr = self.split(r)
        r1 = gr.node.sum if gr != None else 0
        self.merge(le, gr)

        self.accumulator = (self.tree.node.sum - l1 - r1) if self.tree.node != None else 0
        return self.accumulator  

    def summ(self, l, r):
        return self.sum_split(l, r) if self.usesplit else self.sum_sum(l, r)


def run(tree, input=sys.stdin, output=sys.stdout, trace=False, nodefunc=False, **settings):
    reader = lambda: next(input)
    find = lambda key: output.write("Found\n" if T.find(key) != None else "Not found\n")
    summ = lambda l, r: output.write(str(T.summ(l, r)) + '\n')  
    T = tree(**settings)
    n = int(reader())
    commands = {'+': T.add, '?': find, '-': T.remove, 's': summ}
    for _ in range(n):
        cmd, *args = reader().split()
        args = list(map(T.bormuliator, map(int, args)))
        commands[cmd](*args)
        if trace:
            print("acc:{} <- ({} {})".format(T.accumulator, cmd, args))
        if nodefunc:
            T.display(nodefunc)
    return T


n = 100
nodes = list(range(5,n + 5))
random.shuffle(list(range(5,n + 5)))

T1, T2 = AVLTree(), AVLTree(usesplit=True)
for k in nodes:
    T1.add(k); T2.add(k)

def speed(s):
    for (l, r) in product(range(n + 10), repeat=2):
        if l <= r:
            s(l, r)
# speed = lambda s: [s(l, r) for (l, r) in product(range(n + 10), repeat=2) if l <= r]


import cProfile
cProfile.run('speed(T1.summ)', sort=2)
cProfile.run('speed(T2.summ)', sort=2)
