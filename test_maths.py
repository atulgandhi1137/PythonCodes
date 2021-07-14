from maths import fib, next_element

def test_fib_initial():
    assert(fib(0)) == 0
    assert(fib(1)) == 1

def test_fib2():
    assert fib(2) == 1

def test_fib3():
    assert fib(3) == 2
    
def test_next_element():
    assert next_element(1) == 4

def test_next_element1():
    assert next_element(4) == 15