from enw.block._run import DispersionOptions
from jinja2 import Environment
import pytest

from enw.block import (
    Main,
    Output,
    Restart,
    MultipleCase,
    OpenMP
)
from typing import cast, TYPE_CHECKING, no_type_check

if TYPE_CHECKING:
    from enw.types import (
        MainConfig,
        OutputConfig,
        RestartConfig,
        MultipleCaseConfig,
        OpenMPConfig
    )

pytestmark = [
    pytest.mark.block,
    pytest.mark.block_run
]

@pytest.fixture
def main_config() -> MainConfig:
    return {
        "name": "Test",
        "backwards": True,
        "max_num_sources": 1000,
        "max_num_field_reqs": 1000,
        "max_num_field_output_groups": 1000,
        "absolute_or_relative": "Absolute",
        "fixed_met": True,
        "flat_earth": False,
        "random_seed": "Fixed (Parallel)"
    }

@pytest.fixture
def main_expected_block() -> str:
    return "\n".join([
        "Main Options:",
        (
            "Run Name,Absolute or Relative Time?,Fixed Met?,Flat Earth?,"
            "Random Seed,Max # Sources,Max # Field Reqs,"
            "Max # Field Output Groups,Backwards?"
        ),
        "Test,Absolute,Yes,No,Fixed (Parallel),1000,1000,1000,Yes"
    ])

@pytest.fixture
def main_expected_repr() -> str:
    return "\n".join([
        "[Main Options]",
        "\tname                          : Test",
        "\tbackwards                     : Yes",
        "\tmax_num_sources               : 1000",
        "\tmax_num_field_reqs            : 1000",
        "\tmax_num_field_output_groups   : 1000",
        "\tabsolute_or_relative          : Absolute",
        "\tfixed_met                     : Yes",
        "\tflat_earth                    : No",
        "\trandom_seed                   : Fixed (Parallel)"
    ])


def test_init_main(main_config: MainConfig):
    """Does the Main class initialise?"""
    tests = {}
    expected_vals = {
        "name": "Test",
        "backwards": "Yes",
        "max_num_sources": 1000,
        "max_num_field_reqs": 1000,
        "max_num_field_output_groups": 1000,
        "absolute_or_relative": "Absolute",
        "fixed_met": "Yes",
        "flat_earth": "No",
        "random_seed": "Fixed (Parallel)"
    }

    main = Main.setup(
        **main_config
    )
    vals = main.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        main._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("bad_entry", [
    {"max_num_sources": -1},
    {"max_num_field_reqs": -1},
    {"max_num_field_output_groups": -1},
    {"absolute_or_relative": "Bad Value"},
    {"random_seed": "Bad Value"}
])
def test_main_init_bad_val(
    main_config: MainConfig,
    bad_entry: dict[str, str | int],
):
    """Does the Main class error properly?"""
    bad_config = main_config | bad_entry

    bad_key = next(iter(bad_entry.keys()))
    bad_val = next(iter(bad_entry.values()))

    with pytest.raises(TypeError, match=f"{bad_key}.*{bad_val}"):
        _ = Main.setup(
            **cast("MainConfig", bad_config)
        )


def test_main_str(main_config: MainConfig, main_expected_block: str):
    """Does the Main class have the right output?"""
    tests = {}

    main = Main.setup(
        **main_config
    )

    block = str(main)
    tests["Expected str"] = block == main_expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_main_repr(main_config: MainConfig, main_expected_repr: str):
    """Does the Main class have the right repr?"""
    tests = {}

    main = Main.setup(
        **main_config
    )

    result = repr(main)
    tests["Expected repr"] = result == main_expected_repr


    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.fixture
def output_config() -> OutputConfig:
    return {
        "folder": "/any/valid/path",
        "seconds": True
    }

@pytest.fixture
def output_expected_block() -> str:
    return "\n".join([
        "Output Options:",
        "Folder,Seconds?",
        "/any/valid/path,Yes"
    ])

@pytest.fixture
def output_expected_repr() -> str:
    return "\n".join([
        "[Output Options]",
        "\tfolder                        : /any/valid/path",
        "\tseconds                       : Yes"
    ])


def test_output_init(output_config: OutputConfig):
    """Does the Output class initialise?"""
    tests = {}
    expected_vals = {
        "folder": "/any/valid/path",
        "seconds": "Yes"
    }

    output = Output.setup(
        **output_config
    )
    vals = output.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        output._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_output_init_bad_path(output_config: OutputConfig):
    """Does the Output class error with bad path?"""
    bad_config = output_config | {"folder": 222}

    with pytest.raises(TypeError, match="folder is not a valid path"):
        _ = Output.setup(
            **bad_config
        )


def test_output_str(output_config: OutputConfig, output_expected_block: str):
    """Does the Output class output the right string?"""
    tests = {}

    output = Output.setup(
        **output_config
    )

    block = str(output)
    tests["Expected str"] = block == output_expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_output_repr(output_config: OutputConfig, output_expected_repr: str):
    """Does the Output class output the right repr?"""
    tests = {}

    output = Output.setup(
        **output_config
    )

    result = repr(output)
    tests["Expected repr"] = result == output_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.fixture
def restart_configs() -> list[RestartConfig]:
    return [
        {
            "cases_between_writes": 100,
            "delete_old_files": True,
            "write_on_suspend": False
        },
        {
            "time_between_writes": "2d 01:30",
            "delete_old_files": False,
            "write_on_suspend": True
        },
        {
            "time_between_writes": "- 2 day 4 hr 3 min ",
            "delete_old_files": False,
            "write_on_suspend": True
        },
    ]

@pytest.fixture
def restart_expected_blocks() -> list[str]:
    return [
        "\n".join(i) for i in [
            (
                "Restart Options:",
                (
                "Cases Between Writes,Time Between Writes,Delete Old Files?,"
                "Write On Suspend?"
                ),
                "100,,Yes,No"
            ),
            (
                "Restart Options:",
                (
                "Cases Between Writes,Time Between Writes,Delete Old Files?,"
                "Write On Suspend?"
                ),
                ",2d 01:30,No,Yes"
            ),
            (
                "Restart Options:",
                (
                "Cases Between Writes,Time Between Writes,Delete Old Files?,"
                "Write On Suspend?"
                ),
                ",- 2 day 4 hr 3 min ,No,Yes"
            ),
        ]
    ]

@pytest.fixture
def restart_expected_reprs() -> list[str]:
    return [
        "\n".join(i) for i in [
            (
                "[Restart Options]",
                "\tcases_between_writes          : 100",
                "\ttime_between_writes           : None",
                "\tdelete_old_files              : Yes",
                "\twrite_on_suspend              : No"
            ),
            (
                "[Restart Options]",
                "\tcases_between_writes          : None",
                "\ttime_between_writes           : 2d 01:30",
                "\tdelete_old_files              : No",
                "\twrite_on_suspend              : Yes"
            ),
            (
                "[Restart Options]",
                "\tcases_between_writes          : None",
                "\ttime_between_writes           : - 2 day 4 hr 3 min ",
                "\tdelete_old_files              : No",
                "\twrite_on_suspend              : Yes"
            ),
        ]
    ]


@pytest.mark.parametrize("index", range(3))
def test_restart_init(restart_configs: list[RestartConfig], index: int):
    """Does the Restart class initialise?"""
    tests = {}
    expected_vals = (
        {
            "cases_between_writes": 100,
            "time_between_writes": None,
            "delete_old_files": "Yes",
            "write_on_suspend": "No"
        },
        {
            "cases_between_writes": None,
            "time_between_writes": "2d 01:30",
            "delete_old_files": "No",
            "write_on_suspend": "Yes"
        },
        {
            "cases_between_writes": None,
            "time_between_writes": "- 2 day 4 hr 3 min ",
            "delete_old_files": "No",
            "write_on_suspend": "Yes"
        },
    )

    restart = Restart.setup(
        **restart_configs[index]
    )
    vals = restart.__dict__

    for k, v in expected_vals[index].items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        restart._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
def test_restart_init_both_option():
    """Does the Output class error with bad path?"""
    bad_config = {
        "cases_between_writes": 100,
        "time_between_writes": "- 2 day 4 hr 3 min ",
        "delete_old_files": False,
        "write_on_suspend": True
    }

    with pytest.raises(
        ValueError,
        match="Both cases_between_writes and time_between_writes are set"
    ):
        _ = Restart.setup(
            **bad_config
        )


@no_type_check
def test_restart_init_blank():
    """Does the Output class error with bad path?"""
    tests = {}

    blank_config = {
        "cases_between_writes": None,
        "time_between_writes": None,
        "delete_old_files": False,
        "write_on_suspend": True
    }

    expected_vals = {
        "cases_between_writes": None,
        "time_between_writes": None,
        "delete_old_files": None,
        "write_on_suspend": None
    }

    restart = Restart.setup(
        **blank_config
    )
    vals = restart.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        restart._environment,  #noqa: SLF001
        Environment
    )

    tests ["Blank str"] = str(restart) == ""

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("index", range(3))
def test_restart_str(
    restart_configs: list[RestartConfig],
    restart_expected_blocks: list[str],
    index: int
):
    """Does the Restart class output the right string?"""
    tests = {}

    restart = Restart.setup(
        **restart_configs[index]
    )

    block = str(restart)
    tests["Expected str"] = block == restart_expected_blocks[index]

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("index", range(3))
def test_restart_repr(
    restart_configs: list[RestartConfig],
    restart_expected_reprs: list[str],
    index: int
):
    """Does the Output class output the right repr?"""
    tests = {}

    restart = Restart.setup(
        **restart_configs[index]
    )

    result = repr(restart)
    tests["Expected repr"] = result == restart_expected_reprs[index]

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.fixture
def multiple_case_config() -> MultipleCaseConfig:
    return {
        "name": "Test",
        "dispersion_options_ensemble_size": 1,
        "met_ensemble_size": 1
    }

@pytest.fixture
def multiple_case_expected_block() -> str:
    return "\n".join([
        "Multiple Case Options: Test",
        "Dispersion Options Ensemble Size,Met Ensemble Size",
        "1,1"
    ])

@pytest.fixture
def multiple_case_expected_repr() -> str:
    return "\n".join([
        "[Multiple Case Options]",
        "\tname                               : Test",
        "\tdispersion_options_ensemble_size   : 1",
        "\tmet_ensemble_size                  : 1"
    ])


def test_multiple_case_init(
    multiple_case_config: MultipleCaseConfig,
):
    """Does the MultipleCase class initialise?"""
    tests = {}
    expected_vals = {
        "name": "Test",
        "dispersion_options_ensemble_size": 1,
        "met_ensemble_size": 1
    }

    multiple_case = MultipleCase.setup(
        **multiple_case_config
    )
    vals = multiple_case.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        multiple_case._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_multiple_case_str(
    multiple_case_config: MultipleCaseConfig,
    multiple_case_expected_block: str,
):
    """Does the MultipleCase class output the right string?"""
    tests = {}

    multiple_case = MultipleCase.setup(
        **multiple_case_config
    )

    block = str(multiple_case)
    tests["Expected str"] = block == multiple_case_expected_block

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_multiple_case_repr(
    multiple_case_config: MultipleCaseConfig,
    multiple_case_expected_repr: str,
):
    """Does the MultipleCase class output the right repr?"""
    tests = {}

    multiple_case = MultipleCase.setup(
        **multiple_case_config
    )

    result = repr(multiple_case)
    tests["Expected repr"] = result == multiple_case_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_type",
    [
        ("name", 1),
        ("dispersion_options_ensemble_size", "1"),
        ("met_ensemble_size", "1")
    ]
)
@no_type_check
def test_multiple_case_bad_type(
    multiple_case_config: MultipleCaseConfig,
    bad_type: tuple[str, str | int]
):
    """Does the MultipleCase class error with a bad type?"""
    config = multiple_case_config | {bad_type[0]: bad_type[1]}

    with pytest.raises(TypeError, match=f"{bad_type[0]} is not "):
        _ = MultipleCase.setup(**config)


@no_type_check
def test_multiple_case_name_blank(
    multiple_case_config: MultipleCaseConfig
):
    """Does the MultipleCase class error with a bad type?"""
    tests = {}
    config = multiple_case_config | {"name": None}

    multiple_cases = MultipleCase.setup(**config)
    tests["name is string"] = isinstance(multiple_cases.name, str)
    tests["name is blank string"] = multiple_cases.name == ""

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@no_type_check
@pytest.fixture
def openmp_config() -> OpenMPConfig:
    return {
        "threads": 1,
        "particle_threads": 2,
        "particle_update_threads": 3,
        "chemistry_threads": 4,
        "output_group_threads": 5,
        "output_process_threads": 6,
        "parallel_metread": True,
        "parallel_metprocess": False
    }


@pytest.mark.parametrize("threads", [True, False])
@pytest.mark.parametrize("particle_threads", [True, False])
@pytest.mark.parametrize("particle_update_threads", [True, False])
@pytest.mark.parametrize("chemistry_threads", [True, False])
@pytest.mark.parametrize("output_group_threads", [True, False])
@pytest.mark.parametrize("output_process_threads", [True, False])
@pytest.mark.parametrize("parallel_metread", [True, False])
@pytest.mark.parametrize("parallel_metprocess", [True, False])
@no_type_check
def test_openmp_init(
    openmp_config: OpenMPConfig,
    threads: bool,  # noqa: FBT001
    particle_threads: bool,  # noqa: FBT001
    particle_update_threads: bool,  # noqa: FBT001
    chemistry_threads: bool,  # noqa: FBT001
    output_group_threads: bool,  # noqa: FBT001
    output_process_threads: bool,  # noqa: FBT001
    parallel_metread: bool,  # noqa: FBT001
    parallel_metprocess: bool  # noqa: FBT001
):
    """Does the OpenMP class initialise?"""
    config_mask = {
        "threads": threads,
        "particle_threads": particle_threads,
        "particle_update_threads": particle_update_threads,
        "chemistry_threads": chemistry_threads,
        "output_group_threads": output_group_threads,
        "output_process_threads": output_process_threads,
        "parallel_metread": parallel_metread,
        "parallel_metprocess": parallel_metprocess
    }
    all_expected_vals = {
        "use_openmp": "Yes",
        "threads": 1,
        "particle_threads": 2,
        "particle_update_threads": 3,
        "chemistry_threads": 4,
        "output_group_threads": 5,
        "output_process_threads": 6,
        "parallel_metread": "Yes",
        "parallel_metprocess": "No"
    }
    config = {"use_openmp": True}
    expected_vals: dict[str, str | int | None] = {"use_openmp": "Yes"}
    for k, v in openmp_config.items():
        if config_mask[k]:
            config[k] = v
            expected_vals[k] = all_expected_vals[k]
        else:
            expected_vals[k] = None

    tests = {}

    openmp = OpenMP.setup(
        **config
    )
    vals = openmp.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        openmp._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("threads", [True, False])
@pytest.mark.parametrize("particle_threads", [True, False])
@pytest.mark.parametrize("particle_update_threads", [True, False])
@pytest.mark.parametrize("chemistry_threads", [True, False])
@pytest.mark.parametrize("output_group_threads", [True, False])
@pytest.mark.parametrize("output_process_threads", [True, False])
@pytest.mark.parametrize("parallel_metread", [True, False])
@pytest.mark.parametrize("parallel_metprocess", [True, False])
@no_type_check
def test_openmp_str(
    openmp_config: OpenMPConfig,
    threads: bool,  # noqa: FBT001
    particle_threads: bool,  # noqa: FBT001
    particle_update_threads: bool,  # noqa: FBT001
    chemistry_threads: bool,  # noqa: FBT001
    output_group_threads: bool,  # noqa: FBT001
    output_process_threads: bool,  # noqa: FBT001
    parallel_metread: bool,  # noqa: FBT001
    parallel_metprocess: bool  # noqa: FBT001
):
    """Does the OpenMP class initialise?"""
    config_mask = {
        "threads": threads,
        "particle_threads": particle_threads,
        "particle_update_threads": particle_update_threads,
        "chemistry_threads": chemistry_threads,
        "output_group_threads": output_group_threads,
        "output_process_threads": output_process_threads,
        "parallel_metread": parallel_metread,
        "parallel_metprocess": parallel_metprocess
    }
    all_expected_vals = {
        "use_openmp": "Yes",
        "threads": "1",
        "particle_threads": "2",
        "particle_update_threads": "3",
        "chemistry_threads": "4",
        "output_group_threads": "5",
        "output_process_threads": "6",
        "parallel_metread": "Yes",
        "parallel_metprocess": "No"
    }
    col_names = {
        "threads": "Threads",
        "particle_threads": "Particle Threads",
        "particle_update_threads": "Particle Update Threads",
        "chemistry_threads": "Chemistry Threads",
        "output_group_threads": "Output Group Threads",
        "output_process_threads": "Output Process Threads",
        "parallel_metread": "Parallel MetRead",
        "parallel_metprocess": "Parallel MetProcess"
    }
    config = {"use_openmp": True}
    expected_cols = [
        "Use OpenMP?"
    ]
    expected_vals = [
        "Yes"
    ]
    for k, v in openmp_config.items():
        if config_mask[k]:
            config[k] = v
            expected_cols.append(col_names[k])
            expected_vals.append(all_expected_vals[k])


    expected_str = "\n".join([
        "OpenMP Options:",
        ",".join(expected_cols),
        ",".join(expected_vals)
    ])

    tests = {}


    openmp = OpenMP.setup(
        **config
    )

    block = str(openmp)
    print(repr(block))
    print(repr(expected_str))
    tests["Expected str"] = block == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize("threads", [True, False])
@pytest.mark.parametrize("particle_threads", [True, False])
@pytest.mark.parametrize("particle_update_threads", [True, False])
@pytest.mark.parametrize("chemistry_threads", [True, False])
@pytest.mark.parametrize("output_group_threads", [True, False])
@pytest.mark.parametrize("output_process_threads", [True, False])
@pytest.mark.parametrize("parallel_metread", [True, False])
@pytest.mark.parametrize("parallel_metprocess", [True, False])
@no_type_check
def test_openmp_repr(
    openmp_config: OpenMPConfig,
    threads: bool,  # noqa: FBT001
    particle_threads: bool,  # noqa: FBT001
    particle_update_threads: bool,  # noqa: FBT001
    chemistry_threads: bool,  # noqa: FBT001
    output_group_threads: bool,  # noqa: FBT001
    output_process_threads: bool,  # noqa: FBT001
    parallel_metread: bool,  # noqa: FBT001
    parallel_metprocess: bool  # noqa: FBT001
):
    """Does the OpenMP class initialise?"""
    config_mask = {
        "threads": threads,
        "particle_threads": particle_threads,
        "particle_update_threads": particle_update_threads,
        "chemistry_threads": chemistry_threads,
        "output_group_threads": output_group_threads,
        "output_process_threads": output_process_threads,
        "parallel_metread": parallel_metread,
        "parallel_metprocess": parallel_metprocess
    }
    all_expected_vals = {
        "use_openmp": "Yes",
        "threads": "1",
        "particle_threads": "2",
        "particle_update_threads": "3",
        "chemistry_threads": "4",
        "output_group_threads": "5",
        "output_process_threads": "6",
        "parallel_metread": "Yes",
        "parallel_metprocess": "No"
    }
    config = {"use_openmp": True}
    expected_repr = [
        "[OpenMP Options]",
        f"\t{'use_openmp':<30}: Yes"
    ]
    for k, v in openmp_config.items():
        if config_mask[k]:
            config[k] = v
            expected_repr.append(
                f"\t{k:<30}: {all_expected_vals[k]}"
            )
        else:
            expected_repr.append(
                f"\t{k:<30}: None"
            )

    tests = {}

    openmp = OpenMP.setup(
        **config
    )

    block = repr(openmp)
    tests["Expected repr"] = block == "\n".join(expected_repr)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_openmp_init_false(
    openmp_config: OpenMPConfig
):
    """Does OpenMP initialise and set all to none if openmp is false?"""
    tests = {}
    config = {"use_openmp": False} | openmp_config
    openmp = OpenMP.setup(
        **config
    )
    vals = openmp.__dict__
    expected_vals = {
        "use_openmp": "No",
        "threads": None,
        "particle_threads": None,
        "particle_update_threads": None,
        "chemistry_threads": None,
        "output_group_threads": None,
        "output_process_threads": None,
        "parallel_metread": None,
        "parallel_metprocess": None,
    }

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        openmp._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_openmp_str_false(
    openmp_config: OpenMPConfig
):
    """Does OpenMP initialise and set all to none if openmp is false?"""
    tests = {}
    config = {"use_openmp": False} | openmp_config
    openmp = OpenMP.setup(
        **config
    )
    block = str(openmp)

    expected_str = "\n".join([
        "OpenMP Options:",
        "Use OpenMP?",
        "No"
    ])

    tests["Expected str"] = block == expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_openmp_repr_false(
    openmp_config: OpenMPConfig
):
    """Does OpenMP initialise and set all to none if openmp is false?"""
    tests = {}
    config = {"use_openmp": False} | openmp_config
    other_keys = [
        "threads",
        "particle_threads",
        "particle_update_threads",
        "chemistry_threads",
        "output_group_threads",
        "output_process_threads",
        "parallel_metread",
        "parallel_metprocess",
    ]
    expected_repr = [
        "[OpenMP Options]",
        f"\t{'use_openmp':<30}: No"
    ] + [
        f"\t{k:<30}: None"
        for k in other_keys
    ]
    openmp = OpenMP.setup(
        **config
    )
    block = repr(openmp)
    tests["Expected repr"] = block == "\n".join(expected_repr)

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


@pytest.mark.parametrize(
    "bad_type",
    [
        ("threads", "BAD VALUE"),
        ("particle_threads", "BAD VALUE"),
        ("particle_update_threads", "BAD VALUE"),
        ("chemistry_threads", "BAD VALUE"),
        ("output_group_threads", "BAD VALUE"),
        ("output_process_threads", "BAD VALUE"),
        ("parallel_metread", "BAD VALUE"),
        ("parallel_metprocess", "BAD VALUE"),
    ]
)
@no_type_check
def test_openmp_bad_type(
    openmp_config: OpenMPConfig,
    bad_type: tuple[str, str | int]
):
    """Does the OpenMP class error with a bad type?"""
    config = {"use_openmp": True} | openmp_config | {bad_type[0]: bad_type[1]}

    with pytest.raises(TypeError, match=f"{bad_type[0]} is not "):
        _ = OpenMP.setup(**config)

@pytest.mark.parametrize(
    "negative_int",
    [
        "threads",
        "particle_threads",
        "particle_update_threads",
        "chemistry_threads",
        "output_group_threads",
        "output_process_threads",
    ]
)
@no_type_check
def test_openmp_negative_int(
    openmp_config: OpenMPConfig,
    negative_int: str
):
    """Does the OpenMP class error with negative integer?"""
    config = {"use_openmp": True} | openmp_config | {negative_int: -1}

    with pytest.raises(
        TypeError,
        match=f" integer value for {negative_int}. Got -1 instead."
    ):
        _ = OpenMP.setup(**config)


@pytest.fixture
def preset_dispersion_options() -> dict[str, int | str | bool]:
    return {
        "max_num_particles": 1000,
        "max_num_full_particles": 2000,
        "max_num_puffs": 2000,
        "max_num_original_puffs": 4000,
        "skew_time": "00:00",
        "velocity_memory_time": "00:30",
        "inhomogeneous_time": "2d 01:25",
        "mesoscale_velocity_memory_time": "1d 00:43",
        "puff_time": "00:00",
        "sync_time": "00:25:30",
        "computational_domain": "Domain",
        "puff_interval": "00:30:10",
        "delta_opt": "1",
        "time_of_fixed_met": "01/02/2005 12:30",
        "deep_convection": "No",
        "radioactive_decay": True,
        "agent_decay": False,
        "dry_deposition": True,
        "wet_deposition": False,
        "mesoscale_motions": True,
        "chemistry": False,
        "turbulence": True,
    }

@pytest.fixture
def dispersion_options_expected_str() -> str:
    return "\n".join([
        "Sets of Dispersion Options:",
        ",".join((
            "Max # Particles",
            "Max # Full Particles",
            "Max # Puffs",
            "Max # Original Puffs",
            "Skew Time",
            "Velocity Memory Time",
            "Inhomogeneous Time",
            "Mesoscale Velocity Memory Time",
            "Puff Time",
            "Sync Time",
            "Computational Domain",
            "Puff Interval",
            "DeltaOpt",
            "Time of Fixed Met",
            "Deep Convection?",
            "Radioactive Decay?",
            "Agent Decay?",
            "Dry Deposition?",
            "Wet Deposition?",
            "Mesoscale Motions?",
            "Chemistry?",
            "Turbulence?"
        )),
        ",".join((
            "1000",
            "2000",
            "2000",
            "4000",
            "00:00",
            "00:30",
            "2d 01:25",
            "1d 00:43",
            "00:00",
            "00:25:30",
            "Domain",
            "00:30:10",
            "1",
            "01/02/2005 12:30",
            "No",
            "Yes",
            "No",
            "Yes",
            "No",
            "Yes",
            "No",
            "Yes"
        )),
    ])

@pytest.fixture
def dispersion_options_expected_repr() -> str:
    return "\n".join([
        "[Sets of Dispersion Options]",
        "\tmax_num_particles             : 1000",
        "\tmax_num_full_particles        : 2000",
        "\tmax_num_puffs                 : 2000",
        "\tmax_num_original_puffs        : 4000",
        "\tparticle_ceiling              : None",
        "\tparticle_factor               : None",
        "\tskew_time                     : 00:00",
        "\tvelocity_memory_time          : 00:30",
        "\tinhomogeneous_time            : 2d 01:25",
        "\tmesoscale_velocity_memory_time: 1d 00:43",
        "\tdamping                       : None",
        "\tpuff_time                     : 00:00",
        "\tsync_time                     : 00:25:30",
        "\tcomputational_domain          : Domain",
        "\tpuff_interval                 : 00:30:10",
        "\tdelta_opt                     : 1",
        "\ttime_of_fixed_met             : 01/02/2005 12:30",
        "\tdeep_convection               : No",
        "\tradioactive_decay             : Yes",
        "\tagent_decay                   : No",
        "\tdry_deposition                : Yes",
        "\twet_deposition                : No",
        "\tmax_deposition_height         : None",
        "\tsedimentation_scheme          : None",
        "\tmesoscale_motions             : Yes",
        "\tchemistry                     : No",
        "\tturbulence                    : Yes",
        "\ta1                            : None",
        "\ta5                            : None",
        "\ta7                            : None",
        "\tvertical_velocity             : None",
        "\teulerian_bcs_filestem         : None",
        "\teulerian_bcs_dt               : None",
        "\tuse_next_bc_value             : None",
        "\tallow_particle_creation_error : None",
        "\tbc_domain                     : None",
        "\teulerian_monotonicity         : None",
    ])

@pytest.mark.parametrize("deep_convection", ["Old", "New", "No"])
def test_dispersion_options_init_preset(
    preset_dispersion_options: dict[str, int | str | bool],
    deep_convection: str
):
    """Does the OpenMP class initialise?"""
    expected_vals: dict[str, str | int | None] = {
        "max_num_particles": 1000,
        "max_num_full_particles": 2000,
        "max_num_puffs": 2000,
        "max_num_original_puffs": 4000,
        "skew_time": "00:00",
        "velocity_memory_time": "00:30",
        "inhomogeneous_time": "2d 01:25",
        "mesoscale_velocity_memory_time": "1d 00:43",
        "puff_time": "00:00",
        "sync_time": "00:25:30",
        "computational_domain": "Domain",
        "puff_interval": "00:30:10",
        "delta_opt": "1",
        "time_of_fixed_met": "01/02/2005 12:30",
        "deep_convection": deep_convection,
        "radioactive_decay": "Yes",
        "agent_decay": "No",
        "dry_deposition": "Yes",
        "wet_deposition": "No",
        "mesoscale_motions": "Yes",
        "chemistry": "No",
        "turbulence": "Yes",
        "particle_ceiling": None,
        "particle_factor": None,
        "damping": None,
        "a1": None,
        "a5": None,
        "a7": None,
        "vertical_velocity": None,
        "eulerian_bcs_filestem": None,
        "eulerian_bcs_dt": None,
        "use_next_bc_value": None,
        "allow_particle_creation_error": None,
        "bc_domain": None,
        "eulerian_monotonicity": None,
    }

    tests = {}

    config = preset_dispersion_options | {"deep_convection": deep_convection}
    disp = DispersionOptions.setup(
        **config
    )
    vals = disp.__dict__

    for k, v in expected_vals.items():
        tests[f"{k} present"] = k in vals
        tests[f"{k} correct"] = v == vals.get(k)

    tests["Environment present"] = isinstance(
        disp._environment,  #noqa: SLF001
        Environment
    )

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())

def test_dispersion_options_str(
    preset_dispersion_options: dict[str, int | str | bool],
    dispersion_options_expected_str: str
):
    """Does the OpenMP class initialise?"""

    tests = {}

    config = preset_dispersion_options
    disp = DispersionOptions.setup(
        **config
    )
    result = str(disp)
    print(dispersion_options_expected_str)
    print(result)

    tests["Expected str"] = result == dispersion_options_expected_str

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())


def test_dispersion_options_repr(
    preset_dispersion_options: dict[str, int | str | bool],
    dispersion_options_expected_repr: str
):
    """Does the OpenMP class initialise?"""

    tests = {}

    config = preset_dispersion_options
    disp = DispersionOptions.setup(
        **config
    )
    result = repr(disp)

    tests["Expected repr"] = result == dispersion_options_expected_repr

    for test, result in tests.items():
        if not result:
            print(test)

    assert all(tests.values())
@pytest.mark.parametrize(
    "bad_key",
    [
        "particle_ceiling",
        "particle_factor",
        "damping",
        "a1",
        "a5",
        "a7",
        "vertical_velocity",
        "eulerian_bcs_filestem",
        "eulerian_bcs_dt",
        "use_next_bc_value",
        "allow_particle_creation_error",
        "bc_domain",
        "eulerian_monotonicity"
    ]
)
def test_dispersion_options_bad_unimplemented_key(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: "BAD VALUE"}
    with pytest.raises(
        NotImplementedError,
        match=(
            f"{bad_key} was specified but is not implemented for Sets of "
            r"Dispersion Options\."
        )
    ):
        _ = DispersionOptions.setup(
            **config
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        "max_num_particles",
        "max_num_full_particles",
        "max_num_puffs",
        "max_num_original_puffs",
    ]
)
@pytest.mark.parametrize(
    "bad_value",
    [
        "BAD VALUE",
        -1,
    ]
)
def test_dispersion_options_bad_pos_int(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str,
    bad_value: str | int
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: bad_value}
    with pytest.raises(
        TypeError,
        match=(
            r"Expected \+ve integer value for|"
            r"is not.*int.*str"
        )
    ):
        _ = DispersionOptions.setup(
            **config
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        "skew_time",
        "velocity_memory_time",
        "inhomogeneous_time",
        "mesoscale_velocity_memory_time",
        "puff_time",
        "sync_time",
        "puff_interval",
    ]
)
def test_dispersion_options_bad_time_interval(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str,
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: "BAD VALUE"}
    with pytest.raises(
        ValueError,
        match=r"not a valid time interval recognised by NAME\."
    ):
        _ = DispersionOptions.setup(
            **config
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        "time_of_fixed_met",
    ]
)
def test_dispersion_options_bad_datetime(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str,
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: "BAD VALUE"}
    with pytest.raises(
        ValueError,
        match=r"not a valid time interval recognised by NAME\."
    ):
        _ = DispersionOptions.setup(
            **config
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        "radioactive_decay",
        "agent_decay",
        "dry_deposition",
        "wet_deposition",
        "mesoscale_motions",
        "chemistry",
        "turbulence",
    ]
)
def test_dispersion_options_bad_switch(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str,
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"bool.*str"
    ):
        _ = DispersionOptions.setup(
            **config
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        "computational_domain",
        "delta_opt",
        "skew_time",
        "velocity_memory_time",
        "inhomogeneous_time",
        "mesoscale_velocity_memory_time",
        "puff_time",
        "sync_time",
        "puff_interval",
        "time_of_fixed_met",
        "deep_convection"
    ]
)
def test_dispersion_options_bad_str(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str,
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: 1}
    with pytest.raises(
        TypeError,
        match=r"str.*int"
    ):
        _ = DispersionOptions.setup(
            **config
        )


@pytest.mark.parametrize(
    "bad_key",
    [
        "deep_convection"
    ]
)
def test_dispersion_options_bad_literals(
    preset_dispersion_options: dict[str, int | str | bool],
    bad_key: str,
):
    """Does the OpenMP class initialise?"""
    config = preset_dispersion_options | {bad_key: "BAD VALUE"}
    with pytest.raises(
        TypeError,
        match=r"is not a member of.*Expected one of"
    ):
        _ = DispersionOptions.setup(
            **config
        )
