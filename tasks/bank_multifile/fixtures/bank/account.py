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
        # BUG: no overdraft protection
        self.balance -= amt
        return amt
