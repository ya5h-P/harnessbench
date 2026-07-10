from stack import Stack


def run():
    s = Stack()
    s.push(1)
    s.push(2)
    s.push(3)
    assert s.pop() == 3, "LIFO: first pop should be 3"
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    run()
