from pathlib import Path
from typing import no_type_check

from jinja2 import Environment
import pytest

from enw.block import (
    InputFiles,
    Array
)


pytestmark = [
    pytest.mark.block,
    pytest.mark.block_misc
]

@pytest.fixture
def file_list() -> list[str]:
    return [
        "relative/file.txt",
        "samedir.txt",
        "/absolute/file.txt"
    ]

@pytest.fixture
def input_files_expected_block() -> str:
    return "\n".join([
        "Input Files:",
        "File Names",
        "relative/file.txt",
        "samedir.txt",
        "/absolute/file.txt"
    ])

@pytest.fixture
def input_files_expected_repr() -> str:
    return "\n".join([
        "[Input Files]",
        "\trelative/file.txt",
        "\tsamedir.txt",
        "\t/absolute/file.txt"
    ])


def test_init_input_files(
    file_list: list[str],
):
    """Does the InputFiles class initialise?"""
    tests = {}
    expected_vals = (
        Path("relative/file.txt"),
        Path("samedir.txt"),
        Path("/absolute/file.txt")
    )

    input_files = InputFiles.setup(
        files=file_list
    )

    tests["files present"] = "files" in  input_files.__dict__
    tests["files correct"] = input_files.files == expected_vals

    tests["Environment present"] = isinstance(
        input_files._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_input_files_str(
    file_list: list[str],
    input_files_expected_block: str
):
    """Does the InputFiles create the right str?"""
    tests = {}

    input_files = InputFiles.setup(
        files=file_list
    )
    block = str(input_files)

    tests["Expected str"] = block == input_files_expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_input_files_repr(
    file_list: list[str],
    input_files_expected_repr: str
):
    """Does the InputFiles create the right repr?"""
    tests = {}

    input_files = InputFiles.setup(
        files=file_list
    )
    block = repr(input_files)

    tests["Expected repr"] = block == input_files_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_input_bad_files(
):
    """Does InputFiles error with bad path?"""

    with pytest.raises(
        TypeError,
        match=r"Input Files \(Index 0\) is not a valid path: 0"
    ):
        _ = InputFiles.setup(
            files=[0]
        )



@pytest.fixture
def preset_array() -> dict[str, dict[str, object]]:
    """Preset rows for array."""
    return {
        "A": {
            "name": "A",
            "values": [0,1,2,3,4,5,6,7,8,9],
            "comments": ["0","1","2",None,"4",None,"6","7",None,None],
            "comments_name": "TestA"
        },
        "B": {
            "name": "B",
            "values": [0.1,1.1,2.1,3.1,4.1,5.1,6.1,7.1,8.1,9.1],
            "comments": ["Long Comment",None,"",None,"",None,"",None,"",None],
            "comments_name": "TestB"
        },
        "C": {
            "name": "C",
            "values": [
                "0.1",
                "1.1",
                "2.1",
                "3.1",
                "4.1",
                "5.1",
                "6.1",
                "7.1",
                "8.1",
                "9.1",
            ],
            "comments": ["1","2","3","4","5","6","7","8","9","10"],
            "comments_name": "TestC"
        },
    }

@pytest.fixture
def array_expected_str() -> dict[str, str | list[str]]:
    return {
        "Title A": "Array: A",
        "Title B": "Array: B",
        "Title C": "Array: C",
        "Header": "Array Values",
        "Header A": "Array Values, ! TestA",
        "Header B": "Array Values, ! TestB",
        "Header C": "Array Values, ! TestC",
        "A": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ],
        "B": [
            "0.1",
            "1.1",
            "2.1",
            "3.1",
            "4.1",
            "5.1",
            "6.1",
            "7.1",
            "8.1",
            "9.1"
        ],
        "C": [
            "0.1",
            "1.1",
            "2.1",
            "3.1",
            "4.1",
            "5.1",
            "6.1",
            "7.1",
            "8.1",
            "9.1"
        ],
        "Comments - A": [
            "0",
            "1",
            "2",
            "",
            "4",
            "",
            "6",
            "7",
            "",
            "",
        ],
        "Comments - B": [
            "Long Comment",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Comments - C": [
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
        ]
    }

@pytest.fixture
def array_expected_repr() -> str:
    return {
        "A": "\n".join([
            "[Array - A]",
            "\tvalues",
            "\t\t0",
            "\t\t1",
            "\t\t2",
            "\t\t3",
            "\t\t4",
            "\t\t5",
            "\t\t6",
            "\t\t7",
            "\t\t8",
            "\t\t9",
            "\tcomments_name                   : TestA",
            "\tcomments",
            "\t\t0",
            "\t\t1",
            "\t\t2",
            "\t\t",
            "\t\t4",
            "\t\t",
            "\t\t6",
            "\t\t7",
            "\t\t",
            "\t\t"
        ]),
        "B": "\n".join([
            "[Array - B]",
            "\tvalues",
            "\t\t0.1",
            "\t\t1.1",
            "\t\t2.1",
            "\t\t3.1",
            "\t\t4.1",
            "\t\t5.1",
            "\t\t6.1",
            "\t\t7.1",
            "\t\t8.1",
            "\t\t9.1",
            "\tcomments_name                   : TestB",
            "\tcomments",
            "\t\tLong Comment",
            "\t\t",
            "\t\t",
            "\t\t",
            "\t\t",
            "\t\t",
            "\t\t",
            "\t\t",
            "\t\t",
            "\t\t"
        ]),
        "C": "\n".join([
            "[Array - C]",
            "\tvalues",
            "\t\t0.1",
            "\t\t1.1",
            "\t\t2.1",
            "\t\t3.1",
            "\t\t4.1",
            "\t\t5.1",
            "\t\t6.1",
            "\t\t7.1",
            "\t\t8.1",
            "\t\t9.1",
            "\tcomments_name                   : TestC",
            "\tcomments",
            "\t\t1",
            "\t\t2",
            "\t\t3",
            "\t\t4",
            "\t\t5",
            "\t\t6",
            "\t\t7",
            "\t\t8",
            "\t\t9",
            "\t\t10"
        ])
    }

@pytest.mark.parametrize("row", ["A", "B", "C"])
@pytest.mark.parametrize("use_comments", [True, False])
def test_init_array_preset(
    row: str,
    preset_array: dict[str, dict[str, object]],
    *,
    use_comments: bool
):
    """Does the Species class initialise?"""
    tests = {}

    array = Array.setup(
        name=row,
        values=preset_array[row]["values"],
        comments=preset_array[row]["comments"] if use_comments else None,
        comments_name=(
            preset_array[row]["comments_name"] if use_comments else None
        )
    )
    expected_vals = {
        "A": {
            "name": "A",
            "values": ["0","1","2","3","4","5","6","7","8","9"],
            "comments": ["0","1","2","","4","","6","7","",""],
            "comments_name": "TestA"
        },
        "B": {
            "name": "B",
            "values": [
                "0.1",
                "1.1",
                "2.1",
                "3.1",
                "4.1",
                "5.1",
                "6.1",
                "7.1",
                "8.1",
                "9.1",
            ],
            "comments": [
                "Long Comment",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            "comments_name": "TestB"
        },
        "C": {
            "name": "C",
            "values": [
                "0.1",
                "1.1",
                "2.1",
                "3.1",
                "4.1",
                "5.1",
                "6.1",
                "7.1",
                "8.1",
                "9.1",
            ],
            "comments": [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
            ],
            "comments_name": "TestC"
        },
    }
    vals = array.__dict__
    tests["Correct Values"] = (
        tuple(vals["values"]) == tuple(expected_vals[row]["values"])
    )
    if use_comments:
        tests["Correct Comments"] = (
            tuple(vals["comments"]) == tuple(expected_vals[row]["comments"])
        )
        tests["Correct Comments Name"] = (
            vals["comments_name"] == expected_vals[row]["comments_name"]
        )
    else:
        tests["Correct Comments"] = vals["comments"] is None
        tests["Correct Comments Name"] = vals["comments_name"] is None
    tests["Environment present"] = isinstance(
        array._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B", "C"])
def test_init_array_all_cols_none(
    row: str,
    preset_array: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    tests = {}
    row = "A"
    array = Array.setup(
        name=row,
        values=preset_array[row]["values"],
        comments=[None for _ in preset_array[row]["comments"]],
        comments_name=(
            preset_array[row]["comments_name"]
        )
    )
    expected_vals = {
        "A": {
            "name": "A",
            "values": ["0","1","2","3","4","5","6","7","8","9"],
            "comments": ["0","1","2","","4","","6","7","",""],
            "comments_name": "TestA"
        },
        "B": {
            "name": "B",
            "values": [
                "0.1",
                "1.1",
                "2.1",
                "3.1",
                "4.1",
                "5.1",
                "6.1",
                "7.1",
                "8.1",
                "9.1",
            ],
            "comments": [
                "Long Comment",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
            ],
            "comments_name": "TestB"
        },
        "C": {
            "name": "C",
            "values": [
                "0.1",
                "1.1",
                "2.1",
                "3.1",
                "4.1",
                "5.1",
                "6.1",
                "7.1",
                "8.1",
                "9.1",
            ],
            "comments": [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
            ],
            "comments_name": "TestC"
        },
    }
    vals = array.__dict__
    tests["Correct Values"] = (
        tuple(vals["values"]) == tuple(expected_vals[row]["values"])
    )
    tests["Correct Comments"] = vals["comments"] is None
    tests["Correct Comments Name"] = vals["comments_name"] is None
    tests["Environment present"] = isinstance(
        array._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

@pytest.mark.parametrize("row", ["A", "B", "C"])
@pytest.mark.parametrize("use_comments", [True, False])
def test_init_array_str(
    row: str,
    preset_array: dict[str, dict[str, object]],
    array_expected_str: dict[str, str],
    *,
    use_comments: bool
):
    """Does the Species class initialise?"""
    tests = {}

    array = Array.setup(
        name=row,
        values=preset_array[row]["values"],
        comments=preset_array[row]["comments"] if use_comments else None,
        comments_name=(
            preset_array[row]["comments_name"] if use_comments else None
        )
    )
    if use_comments:
        expected = "\n".join([
            array_expected_str[f"Title {row}"],
            array_expected_str[f"Header {row}"],
            *[",".join([v,c]) for v,c in zip(
                array_expected_str[row],
                array_expected_str[f"Comments - {row}"],
                strict=True
            )]
        ])
    else:
        expected = "\n".join([
            array_expected_str[f"Title {row}"],
            array_expected_str["Header"],
            *array_expected_str[row],
        ])

    actual = str(array)
    print(expected)
    print(actual)

    tests["Expected str"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("row", ["A", "B", "C"])
@pytest.mark.parametrize("use_comments", [True, False])
def test_init_array_repr(
    row: str,
    preset_array: dict[str, dict[str, object]],
    array_expected_repr: dict[str, str],
    *,
    use_comments: bool
):
    """Does the Species class initialise?"""
    tests = {}

    array = Array.setup(
        name=row,
        values=preset_array[row]["values"],
        comments=preset_array[row]["comments"] if use_comments else None,
        comments_name=(
            preset_array[row]["comments_name"] if use_comments else None
        )
    )

    actual = repr(array)

    if not use_comments:
        expected = "\n".join([
            *array_expected_repr[row].split("\n")[:-12],
            f"\t{'comments_name':<32}: None",
            f"\t{'comments':<32}: None"
        ])
    else:
        expected = array_expected_repr[row]
    print(expected)
    print(actual)
    tests["Expected repr"] = actual == expected

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_arg", [
        ("name", 0),
        ("comments_name", 0),
])
def test_init_array_bad_base_type(
    bad_arg: tuple[str, str | int],
    preset_array: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_array["A"]
    vals[bad_arg[0]] = bad_arg[1]
    with pytest.raises(
        TypeError,
        match=r"is not.*str.*Is.*int|is not.*int.*Is.*str"
    ):
        _ = Array.setup(
            **vals
        )


@pytest.mark.parametrize("bad_arg", [
        ("values", 0),
        ("comments", 0),
])
def test_init_array_bad_array(
    bad_arg: tuple[str, str | int],
    preset_array: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_array["A"]
    vals[bad_arg[0]] = bad_arg[1]
    with pytest.raises(
        TypeError,
        match=r"should be an iterable object"
    ):
        _ = Array.setup(
            **vals
        )


def test_init_array_bad_mismatched_arrays(
    preset_array: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_array["A"]
    vals["comments"] = ["1","2","3"]
    with pytest.raises(
        ValueError,
        match=r"values and comments are different lengths"
    ):
        _ = Array.setup(
            **vals
        )


def test_init_array_bad_no_name(
    preset_array: dict[str, dict[str, object]],
):
    """Does the Species class initialise?"""
    vals = preset_array["A"]
    vals["comments_name"] = None
    with pytest.raises(
        ValueError,
        match=r"comments set while comments_name is not\."
    ):
        _ = Array.setup(
            **vals
        )
