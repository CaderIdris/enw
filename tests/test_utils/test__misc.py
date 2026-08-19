import pytest

from enw.utils._misc import get_hash

pytestmark = [
    pytest.mark.utils,
    pytest.mark.utils_misc
]

def test_get_hash():
    """Does get_hash work?"""
    tests = {}
    result = get_hash("TEST")
    tests["Is string"] = isinstance(result, str)
    tests["Is 64 characters"] = len(result) == 64

    for test, outcome in tests.items():
        if not outcome:
            print(test)

    assert all(tests.values())
