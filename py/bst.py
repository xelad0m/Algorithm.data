SAMPLES = ["15\n? 1\n+ 1\n? 1\n+ 2\ns 1 2\n+ 1000000000\n? 1000000000\n- 1000000000\n? 1000000000\ns 999999999 1000000000\n- 2\n? 2\n- 0\n+ 9\ns 0 9", 
           "5\n+ 10\n+ 5\n+ 14\n+ 3\n+ 11"]           
OUTPUTS = ...
READER = (x for x in SAMPLES[1].split('\n')); input = lambda: next(READER)
# штош, пишем сначала просто бинарное дерево поиска

class Node():
    def __init__(self, *args):
        self.num = 1
        self.key, self.left, self.right = args
    
    def inorder(self):
        stack, current = [], self
        while stack or current:
            if stack:
                current = stack.pop()
                yield current        
                current = current.right   # перейти в правое п.д.
            while current:
                stack.append(current)
                current = left.left    # идти налево до конца

    def __repr__(self):
        return "{}({},{})".format(self.key, self.left, self.right)

    def __bool__(self):
        return True if self.key else False


class Tree(Node):
    def __init__(self):
        self.root = None
    def __call__(self):
        return self.root

root = Node(None, None, None)


def find(key, node=root):
    while node:
        if key < node.key:
            node = node.left
        elif key > node.key:
            node = node.right
        else:
            return node
    return None


def add(key, node=root):
    if not node:
        if node is root:
            node.key = key
        else:
            node = Node(key, None, None)
    else:
        if key < node.key:
            add(key, node.left)
        elif key > node.key:
            add(key, node.right)
        else:
            return

def remove(key):
    ...

def inorder(node=0):
    if tree:
        stack = []
        while stack or node != -1:
            if stack:
                node = stack.pop()
                yield tree[node].key         
                node = tree[node].right   # перейти в правое п.д.
            while node != -1:
                stack.append(node)
                node = tree[node].left    # идти налево до конца

def summ(l, r):
    global s
    f = lambda x: (x + s) % (10 ** 9 + 1)
    s = sum([x for x in inorder() if f(l) <= x <= f(r)])
    return s

def run():
    commands = {'+': add, '?': find, '-': remove, 's': summ}
    n = int(input())
    for _ in range(n):
        cmd, *args = input().split()
        args = list(map(int, args))
        commands[cmd](*args)

s = 0
run()
print(root.key)