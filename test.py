import copy

class B:
    id : int
    def __init__(self, id):
        self.id = id

class A:
    b : B
    def __init__(self, b):
        self.b = b

b = B(10)
a = A(b)

b.id = 5

print(a.b.id)

copy_a = copy.deepcopy(a)

print(copy_a.b.id)

b.id = 42

print(copy_a.b.id)
print(a.b.id)