import sys

class CharNode:
    def  __init__(self, char):
        self.char = char
        self.size = 1
        self.parent = None
        self.left = None
        self.right = None

class RopeSplay:
    def __init__(self, root=None):
        if root:
            root.parent = None
        self.root = root
    
    def __repr(self):
        return " ".join(self.walk(func=lambda x: x.char))
    
    def __str__(self):
        return "".join(self.walk())

    # print the tree structure on the screen
    def pprint(self):
        if self.root:
            self.__print_helper(self.root, "", True)
        else:
            print("Empty rope")
    
    def __print_helper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R---")
                indent += "     "
            else:
                sys.stdout.write("L---")
                indent += "|   "
            print(currPtr.char, currPtr.size)
            self.__print_helper(currPtr.left, indent, False)
            self.__print_helper(currPtr.right, indent, True)

    def add(self, char):
        node =  CharNode(char)
        y = None
        x = self.root
        while x:
            y = x
            x = x.right
        # y is parent of x
        node.parent = y
        if not y:
            self.root = node
        else:
            y.right = node
        # splay the node
        self.__splay(node)

    def update(self, x=None):
        x = x if x else self.root
        x.size = 1 + (x.right.size if x.right else 0) + \
                     (x.left.size if x.left else 0)
    
    # удалить самый правый, его значение вернуть
    def pop(self) -> CharNode:
        x = self.root
        t = None 
        s = None
        if x:
            #find rightest
            x = self.right(x)
            # make top & split
            self.__splay(x)
            t = None
            s = x.left
            # del x
            char = x.char
            x = None
            # join
            if s:
                s.parent = None
            self.root = self.__join(s, t)
            return char

    # joins two trees s and t
    def __join(self, s, t):
        if s == None:
            return t
        if t == None:
            return s
        x = self.right(s)
        self.__splay(x)
        x.right = t
        t.parent = x
        self.update(x)
        return x

    # rotate left at node x
    def __left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y
        self.update(x)                      # х ниже поэтому первый
        self.update(y)                      
        

    # rotate right at node x
    def __right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != None:
            y.right.parent = x
        
        y.parent = x.parent;
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y 
        y.right = x
        x.parent = y
        self.update(x)                      # х ниже поэтому первый
        self.update(y) 
        

    # Splaying operation. It moves x to the root of the tree
    def __splay(self, x):
        while x.parent != None:
            if x.parent.parent == None:
                if x == x.parent.left:
                    # zig rotation
                    self.__right_rotate(x.parent)
                else:
                    # zag rotation
                    self.__left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # zig-zig rotation
                self.__right_rotate(x.parent.parent)
                self.__right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # zag-zag rotation
                self.__left_rotate(x.parent.parent)
                self.__left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # zig-zag rotation
                self.__left_rotate(x.parent)
                self.__right_rotate(x.parent)
            else:
                # zag-zig rotation
                self.__right_rotate(x.parent)
                self.__left_rotate(x.parent)

    # find the left node
    def left(self, x):
        while x.left:
            x = x.left
        return x

    # find the right node
    def right(self, x):
        while x.right:
            x = x.right
        return x

    def walk(self, func=lambda x: str(x.char)):
        x = self.root
        stack = list()
        while stack or x:
            if stack:
                x = stack.pop()
                yield func(x)
                x = x.right
            while x:
                stack.append(x)
                x = x.left
    
    def __merge_w_root(self, x, y, t):
        if x: x.parent = t
        if y: y.parent = t
        t.left = x
        t.right = y
        self.update(t)
        return t
    
    def __order_stat(self, k):  # 1-based
        x = self.root
        k_order = 1 + (x.left.size if x.left else 0)
        while x:
            if k < k_order:
                x = x.left
                k_order = k_order - 1 - (x.right.size if x.right else 0)
            elif k > k_order:
                x = x.right
                k_order = k_order + 1 + (x.left.size if x.left else 0)
            else:
                return x

    def split(self, k): # 1-based
        if k < 1:
            return RopeSplay(), RopeSplay(self.root)
        elif k > self.root.size - 1:
            return RopeSplay(self.root), RopeSplay()
        else:
            x = self.__order_stat(k)
            self.__splay(x)
            x, y = x, x.right 
            x.right = None
            self.update(x)
            if y: y.parent = None
            if y: self.update(y)
            return RopeSplay(x), RopeSplay(y)


class Splitter:
    def __init__(self):
        self.rope = RopeSplay()

    def add(self, char):
        self.rope.add(char)

    def __merge(t1: RopeSplay, t2: RopeSplay) -> RopeSplay:
        if t1.root == None:
            return t2
        elif t2.root == None:
            return t1
        else:
            t = RopeSplay()
            t.root = CharNode(t1.pop())
            if t1.root: t1.root.parent = t.root
            if t2.root: t2.root.parent = t.root
            t.root.left = t1.root
            t.root.right = t2.root
            t.update()
            return t

    def rearrange(self, i, j, k):
        l, r = self.rope.split(i)
        c, r = r.split(j - i + 1)
        nl, nr = merge(l, r).split(k)
        self.rope = merge(merge(nl, c), nr)
        return self.rope

SAMPLES = "hlelowrold\n2\n1 1 2\n6 6 7", "abcdef\n2\n0 1 1\n4 5 0", "abcdef\n3\n0 0 5\n4 4 5\n5 5 0"
READER = (x for x in SAMPLES[0].split('\n')); input = lambda: next(READER)

# def splitter(i, j, k, rope: RopeSplay) -> RopeSplay:
#     # global rope 
#     l, r = rope.split(i)
#     c, r = r.split(j - i + 1)
#     nl, nr = merge(l, r).split(k)
#     rope = merge(merge(nl, c), nr)
    
def main() -> RopeSplay:
    rope = Splitter()   

    string = input()
    n = int(input())

    for ch in string:
        Splitter.add(Splitter, ch)

    for _ in range(n):
        [i, j, k] = list(map(int, input().split()))
        # Splitter(i, j, k)
    return Splitter(i, j, k)

print(main())