# import pytest
# from hello import say_hello

# @pytest.mark.parametrize("name, expected",[
#     ("Alice", "Hello, Alice!"),
#     ("", "Hello!"),
# ]
# )
# def test_say_hello(name, expected):
#     got = say_hello(name)

#     # 期待する返り値と実際に得た値が同じか確認した上で, 期待する返り値と実際に得た値が異なる場合は、エラーを表示
#     assert got == expected, f"unexpected result of say_hello: want={expected}, got={got}"


import pytest
from datetime import datetime
from hello import say_hello

@pytest.mark.parametrize("name, now, expected", [
    ("Alice", datetime(2024, 1, 1, 9, 0, 0), "Good morning, Alice!"),
    ("Bob", datetime(2024, 1, 1, 12, 0, 0), "Hello, Bob!"),
    ("Charlie", datetime(2024, 1, 1, 20, 0, 0), "Good evening, Charlie!"),
])
def test_say_hello_simple(name, now, expected):
    got = say_hello(name, now)
    assert got == expected, f"unexpected result of say_hello: want={expected}, got={got}"
