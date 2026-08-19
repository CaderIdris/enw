from jinja2 import Environment
import pytest

from enw.block import NAMEIIIHeaderInputBlock

pytestmark = [
    pytest.mark.block,
    pytest.mark.block_base
]

def test_init_n3hib():
    """Does the NAMEIIIHeaderInputBlock class initialise?"""
    base = NAMEIIIHeaderInputBlock()
    assert isinstance(
        base._environment,  #noqa: SLF001
        Environment
    )

def test_n3hib_str_err():
    """Does the NAMEIIIHeaderInputBlock __str__ func raise expected error?"""
    with pytest.raises(
        NotImplementedError,
        match=r"This functionality has not been implemented for BaseConfig."
    ):
        str(NAMEIIIHeaderInputBlock())

def test_n3hib_repr_err():
    """Does the NAMEIIIHeaderInputBlock __repr__ func raise expected error?"""
    with pytest.raises(
        NotImplementedError,
        match=r"This functionality has not been implemented for BaseConfig."
    ):
        repr(NAMEIIIHeaderInputBlock())
