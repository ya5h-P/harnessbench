from bank.account import Account


class Ledger:
    def __init__(self):
        self.accounts = {}

    def open(self, name, opening=0):
        self.accounts[name] = Account(opening)

    def transfer(self, src, dst, amt):
        self.accounts[src].withdraw(amt)
        self.accounts[dst].deposit(amt)

    def total(self):
        return sum(a.balance for a in self.accounts.values())
