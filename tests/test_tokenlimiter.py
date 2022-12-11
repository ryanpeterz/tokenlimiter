import time
from tokenlimiter import TokenLimiter

# tested by ryanpeterz
def _run_tests(quota: int = 300, period: float = 1):
    tokenlimiter = TokenLimiter(quota, period,
                                callback=lambda t: print(f"Block@{time.monotonic()}"))

    start = time.monotonic()
    gas_spent = [0]

    def ex(n: int):
        print(f"Op costs {n} gas.")
        gas_spent[0] = gas_spent[0] + n
        gpm = gas_spent[0] / (time.monotonic() - start)
        assert gpm < (quota / period)
        print(f"Current gpm: {gpm}")

    with tokenlimiter as burn:
        for _ in range(10):
            burn(40)
            ex(40)

if __name__ == "__main__": _run_tests()
