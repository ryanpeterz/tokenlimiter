import time
from threading import Lock

# written by ChatGPT with minimal intervention
class TokenLimiter:
    def __init__(self, max_tokens: int, period: float, callback: callable):
        self.max_tokens = max_tokens
        self.period = period
        self.callback = callback
        self.tokens = 0
        self.last_refill = time.monotonic()
        self.lock = Lock()

    def __enter__(self):
        return self.burn

    def __exit__(self, type, value, traceback):
        pass

    def burn(self, tokens: int):
        with self.lock:
            now = time.monotonic()
            self.tokens += (now - self.last_refill) * (self.max_tokens / self.period)
            self.tokens = min(self.max_tokens, self.tokens)
            self.last_refill = now

            if self.tokens < tokens:
                if self.callback:
                    self.callback(tokens)
                while self.tokens < tokens:
                    time.sleep((tokens - self.tokens) * self.period / self.max_tokens)
                    now = time.monotonic()
                    self.tokens += (now - self.last_refill) * (self.max_tokens / self.period)
                    self.last_refill = now
                    self.tokens = min(self.max_tokens, self.tokens)

            self.tokens -= tokens
