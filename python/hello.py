# def say_hello(name=""):
#     if name:
#         return f"Hello, {name}!"
#     return "Hello!"

# from datetime import datetime

# def say_hello(name):
#     now = datetime.now() # 現在時刻に直接依存しているため、テストしにくい
#     current_hour = now.hour

#     if 6 <= current_hour < 10:
#         return f"Good morning, {name}!"
#     if 10 <= current_hour < 18:
#         return f"Hello, {name}!"
#     return f"Good evening, {name}!"

# 改善されたコード（テストしやすい設計）
from datetime import datetime

def say_hello(name, now=None):
    if now is None:
        now = datetime.now()

    current_hour = now.hour

    if 6 <= current_hour < 10:
        return f"Good morning, {name}!"
    if 10 <= current_hour < 18:
        return f"Hello, {name}!"
    return f"Good evening, {name}!"
