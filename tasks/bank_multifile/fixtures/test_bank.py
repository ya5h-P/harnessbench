from bank.account import Account
from bank.ledger import Ledger


def expect(exc, fn):
    try:
        fn()
    except exc:
        return
    raise AssertionError("expected " + exc.__name__)


def run():
    a = Account(100)
    a.withdraw(40)
    assert a.balance == 60
    expect(ValueError, lambda: a.withdraw(1000))
    assert a.balance == 60
    L = Ledger()
    L.open("x", 50)
    L.open("y", 0)
    L.transfer("x", "y", 30)
    assert L.accounts["x"].balance == 20
    assert L.accounts["y"].balance == 30
    print("ALL TESTS PASSED")


if __name__ == "__main__":
    run()
