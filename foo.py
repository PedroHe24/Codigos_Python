def foo (n):
    if n> 1:
        return n * foo(n-1)
    return n

print (foo(4))