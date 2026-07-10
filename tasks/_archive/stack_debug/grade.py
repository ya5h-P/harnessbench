import sys, os, importlib.util


def load(workdir, name):
    path = os.path.join(workdir, name + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    workdir = sys.argv[1]
    try:
        Stack = load(workdir, "stack").Stack
    except Exception as e:
        print("FAIL: cannot import stack.py: %r" % e); sys.exit(1)

    try:
        # hidden superset: mixed interleaving, peek, size, empty, LIFO ordering
        s = Stack()
        assert s.is_empty() and s.size() == 0
        for i in range(5):
            s.push(i)
        assert s.size() == 5
        assert s.peek() == 4
        assert s.peek() == 4, "peek must not mutate"
        assert s.pop() == 4
        s.push(99)
        assert s.peek() == 99
        assert s.pop() == 99
        assert [s.pop() for _ in range(4)] == [3, 2, 1, 0], "strict LIFO order"
        assert s.is_empty()
        # interleaved
        seq = []
        s.push("a"); s.push("b"); seq.append(s.pop()); s.push("c")
        seq.append(s.pop()); seq.append(s.pop())
        assert seq == ["b", "c", "a"], "interleaved LIFO wrong: %r" % seq
    except AssertionError as e:
        print("FAIL: %s" % e); sys.exit(1)
    except Exception as e:
        print("FAIL: error %r" % e); sys.exit(1)
    print("STACK OK")


if __name__ == "__main__":
    main()
