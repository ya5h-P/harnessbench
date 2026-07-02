class Account:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amt):
        if amt <= 0:
            raise ValueError("amount must be positive")
        self.balance += amt

    def withdraw(self, amt):
        if amt <= 0:
            raise ValueError("amount must be positive")
        if amt > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amt
        return amt
