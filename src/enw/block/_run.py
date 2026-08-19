"""Configuration objects for all of the core NAME III Input Header Blocks.

Covers:

- Main Options: `Main`
- Output Options: `Output`
- Restart Options: `Restart`

"""
from dataclasses import dataclass
from typing import cast, TYPE_CHECKING

from enw.types import (
    AbsOrRelOpts,
    DateTime,
    DeepConvectionOpts,
    RandomSeedOpts,
    TimeInterval
)
from enw.utils import (
    check_datetime,
    check_literal,
    check_mutually_exclusive,
    check_path_like,
    check_pos_int,
    check_time_interval,
    check_type,
    make_switch,
    make_time_interval,
)

from ._base import NAMEIIIHeaderInputBlock

if TYPE_CHECKING:
    from types import NotImplementedType
    from enw.types import Switch


@dataclass(kw_only=True)
class Main(NAMEIIIHeaderInputBlock):
    """Configuration for the Main Options block for NAME III.

    The `Main Options:` block contains the following columns:

    **Absolute or Relative Time?**

    How should time variables be configured?

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Gregorian"/"Absolute" | Gregorian Calendar |
    | "Relative" | Relative time frame |
    | "360-day years" | 360 day years |

    !!! note
        Despite being noted as a switch column with the '?', this does not
        accept only a "Yes" or "No"

    **Backwards?**

    Run NAME III in backward mode, evaluating the influence of the
    surrounding environment on the source location instead of the effect
    of the source on the surrounding environment.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Run in backwards mode |
    | "No" | Run in forwards mode |

    **Fixed Met?**

    Should the Met be fixed or should it change with time?

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Met is fixed |
    | "No" | Met changes with time |

    **Flat Earth?**

    Should the model simulate a flat earth?

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | The Earth is modelled as flat |
    | "No" | The Earth is modelled as a globe |

    **Run Name**

    The name to use for the run.

    _Accepted Values_

    Any valid string

    **Random Seed**

    How the seed for the random number generator should be selected.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Fixed" | Fortran compiler standard RNG with fixed seed |
    | "Random" | Fortran compiler standard RNG with random seed |
    | "Fixed (Parallel)" | Parallel RNG with fixed seed |
    | "Random (Parallel)" | Parallel RNG with random seed |

    !!! note
        When running NAME in parallel with OpenMP, a parallel seed must be
        used.

    **Max # Sources**

    The maximum number of sources allowed during a run. NAME will error if
    this threshold is exceeded.

    _Accepted Values_

    Any positive integer.

    **Max # Sources**

    The maximum number of sources allowed during a run. NAME will error if
    this threshold is exceeded.

    _Accepted Values_

    Any positive integer.

    **Max # Field Reqs**

    The maximum number of field requirements allowed during a run. NAME will
    error if this threshold is exceeded.

    _Accepted Values_

    Any positive integer.

    **Max # Field Output Groups**

    The maximum number of field output groups allowed during a run. NAME will
    error if this threshold is exceeded.

    _Accepted Values_

    Any positive integer.

    **Run-To File**

    !!! warning
        This configuration option is currently unused and will raise a
        `NotImplementedError` if configured in the config file.

    **Same Results With/Without Update on Demand?**

    !!! warning
        This configuration option is currently unused and will raise a
        `NotImplementedError` if configured in the config file.
    """

    #TODO: More info about what the Met is
    name: str
    backwards: Switch
    max_num_sources: int
    max_num_field_reqs: int
    max_num_field_output_groups: int
    absolute_or_relative: AbsOrRelOpts
    fixed_met: Switch
    flat_earth: Switch
    random_seed: RandomSeedOpts

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        backwards: bool,
        max_num_sources: int,
        max_num_field_reqs: int,
        max_num_field_output_groups: int,
        absolute_or_relative: str,
        fixed_met: bool,
        flat_earth: bool,
        random_seed: str
    ) -> Main:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        name : str
            The name of the run, used in the "Main Options" block.
        backwards : bool
            Whether to do a backward (Yes) or forward (No) run.
        max_num_sources : int
            Maximum allowed number of sources.
        max_num_field_reqs : int
            Maximum allowed number of field requirements.
        max_num_field_output_groups : int
            Maximum allowed number of field output groups.
        absolute_or_relative : str
            Set to Gregorian calendar, relative time frame or 360-days.
            Allowed options:

            - Gregorian
            - Relative
            - 360-day years
        fixed_met : bool
            Does the met change with time?
        flat_earth : bool
            Simulate a flat earth?
        random_seed : str
            Seed of the random number generator.
            This must be set to a parallel option if the run is parallelised
            with OpenMP.
            Allowed options:

            - Fixed
                - Fortran compiler standard RNG, fixed seed
            - Random
                - Fortran compiler standard RNG, random seed
            - Fixed (Parallel)
                - Parallel RNG with fixed seed
            - Random (Parallel)
                - Parallel RNG with random seed

            Random numbers are specific to each particle/puff in the stack
            in parallel runs.

        """
        check_type(
            "name",
            name,
            str
        )
        check_type(
            "backwards",
            backwards,
            bool
        )
        check_pos_int("max_num_sources", max_num_sources)
        check_pos_int("max_num_field_reqs", max_num_field_reqs)
        check_pos_int(
            "max_num_field_output_groups",
            max_num_field_output_groups
        )
        check_literal(
            "absolute_or_relative",
            absolute_or_relative,
            "AbsOrRelOpts",
            AbsOrRelOpts
        )
        check_type(
            "fixed_met",
            fixed_met,
            bool
        )
        check_type(
            "flat_earth",
            flat_earth,
            bool
        )
        check_literal(
            "random_seed",
            random_seed,
            "RandomSeedOpts",
            RandomSeedOpts
        )
        return cls(
            name=name,
            backwards=make_switch(backwards),
            max_num_sources=max_num_sources,
            max_num_field_reqs=max_num_field_reqs,
            max_num_field_output_groups=max_num_field_output_groups,
            absolute_or_relative=cast("AbsOrRelOpts", absolute_or_relative),
            fixed_met=make_switch(fixed_met),
            flat_earth=make_switch(flat_earth),
            random_seed=cast("RandomSeedOpts", random_seed)
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "main.jinja" block template
        to get the appropriate configuration block.

        ``` jinja title="main.jinja"
        --8<-- "./src/enw/files/block_templates/main.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("main.jinja")
        return template.render(
            name=self.name,
            absolute_or_relative=self.absolute_or_relative,
            fixed_met=self.fixed_met,
            flat_earth=self.flat_earth,
            random_seed=self.random_seed,
            max_num_sources=self.max_num_sources,
            max_num_field_reqs=self.max_num_field_reqs,
            max_num_field_output_groups=self.max_num_field_output_groups,
            backwards=self.backwards
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Main Options]"
            ] + [
                f"\t{k:<30}: {v}"
                for k, v in self.__dict__.items()
                if k[0] != "_"
            ]
        )


@dataclass(kw_only=True)
class Output(NAMEIIIHeaderInputBlock):
    """Configuration for the Output Options block for NAME III.

    The `Output Options:` block contains the following columns:

    **Folder**

    Where should the results be stored?

    _Accepted Values_

    Any path-like string. Can be absolute or relative.

    **Seconds?**

    Write seconds in the output time field?

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Use seconds in timestamps |
    | "No" | Do not use seconds in timestamps |

    **Time Decimal Places**

    !!! warning
        This configuration option is currently unused and will raise a
        `NotImplementedError` if configured in the config file.
    """

    folder: str
    seconds: Switch

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        folder: str,
        seconds: bool
    ) -> Output:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        folder : str
            Path to save output
        seconds : bool
            Whether to use seconds in timestamp (True) or not (False).

        """
        check_path_like("folder", folder)
        check_type(
            "seconds",
            seconds,
            bool
        )
        return cls(
            folder=folder,
            seconds=make_switch(seconds)
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "output.jinja" block template
        to get the appropriate configuration block.

        ``` jinja title="output.jinja"
        --8<-- "./src/enw/files/block_templates/output.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("output.jinja")
        return template.render(
            folder=self.folder,
            seconds=self.seconds
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Output Options]"
            ] + [
                f"\t{k:<30}: {v}"
                for k, v in self.__dict__.items()
                if k[0] != "_"
            ]
        )


@dataclass(kw_only=True)
class Restart(NAMEIIIHeaderInputBlock):
    """Configuration for the Restart Options block for NAME III.

    A restart file is effectively a checkpoint for a NAME run. If a run is
    cancelled for any reason, it can be restarted from said checkpoint instead
    of from the beginning. However, frequent writes to a restart file will
    slow NAME down, it's important to strike a balance when using this feature.

    This block is optional, if the user does not set any values it will not be
    included in the input header file.

    The `Restart Options:` block contains the following columns:

    **# Cases Between Writes**

    The number of cases to run before writing a restart file.

    _Accepted Values_

    Any positive integer.

    **Time Between Writes**

    The amount of time between writing restart files.

    _Accepted Values_

    A relative time stamp, see TODO about formatting.

    !!! warning
        Only one of **# Cases Between Writes** and **Time Between Writes** can
        be set. Setting both will cause an error to be raised.

    **Delete Old Files?**

    Only keep the latest restart file.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Delete old restart files |
    | "No" | Keep restart files |

    **Write on Suspend?**

    Write a restart file when the program is suspended.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Write a restart file when the program suspends |
    | "No" | Do not write a restart file on program suspension |

    """

    cases_between_writes: int | None = None
    time_between_writes: TimeInterval | None = None
    delete_old_files: Switch | None = None
    write_on_suspend: Switch | None = None

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        cases_between_writes: int | None = None,
        time_between_writes: str | None = None,
        delete_old_files: bool | None = None,
        write_on_suspend: bool | None = None
    ) -> Restart:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        cases_between_writes : int | None
            Number of cases to run before writing to a restart file.
        time_between_writes : str | None
            Time between saving snapshots as a restart file, in the format
            of a time interval. (See LINK)  #TODO
        delete_old_files : bool | None
            Delete old restart files when a new one is created?
        write_on_suspend : Switch | None
            Write a restart file if the program suspends?

        """
        check_mutually_exclusive(
            "cases_between_writes",
            cases_between_writes,
            "time_between_writes",
            time_between_writes
        )
        if cases_between_writes is None and time_between_writes is None:
            return cls(
                cases_between_writes=None,
                time_between_writes=None,
                delete_old_files=None,
                write_on_suspend=None
            )
        if cases_between_writes is not None:
            check_type(
                "cases_between_writes",
                cases_between_writes,
                int
            )
            check_pos_int(
                "cases_between_writes",
                cases_between_writes
            )
        if time_between_writes is not None:
            check_type(
                "time_between_writes",
                time_between_writes,
                str
            )
        if delete_old_files is not None:
            check_type(
                "delete_old_files",
                delete_old_files,
                bool
            )
        if write_on_suspend is not None:
            check_type(
                "write_on_suspend",
                write_on_suspend,
                bool
            )
        delete_old_files_switch = (
            make_switch(delete_old_files)
            if delete_old_files is not None
            else None
        )
        write_on_suspend_switch = (
            make_switch(write_on_suspend)
            if write_on_suspend is not None
            else None
        )
        time_between_writes_interval = (
            make_time_interval(time_between_writes)
            if time_between_writes is not None
            else None
        )
        return cls(
            cases_between_writes=cases_between_writes,
            time_between_writes=time_between_writes_interval,
            delete_old_files=delete_old_files_switch,
            write_on_suspend=write_on_suspend_switch
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "restart.jinja" block template
        to get the appropriate configuration block.

        ``` jinja title="restart.jinja"
        --8<-- "./src/enw/files/block_templates/restart.jinja"
        ```

        If neither `cases_between_writes` or `time_between_writes` are
        configured, an empty string is returned.

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file, or
            empty string if no configuration required.

        """
        template = self._environment.get_template("restart.jinja")
        if (
            self.cases_between_writes is None and
            self.time_between_writes is None
        ):
            return ""
        return template.render(
            cases_between_writes=self.cases_between_writes,
            time_between_writes=self.time_between_writes,
            delete_old_files=self.delete_old_files,
            write_on_suspend=self.write_on_suspend
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Restart Options]"
            ] + [
                f"\t{k:<30}: {v}"
                for k, v in self.__dict__.items()
                if k[0] != "_"
            ]
        )


@dataclass(kw_only=True)
class MultipleCase(NAMEIIIHeaderInputBlock):
    """Configuration for the Multiple Case Options block for NAME III.

    This is a **named block**.
    A name can be given to it using the `name` keyword argument.

    The `Multiple Case Options:` block contains the following columns:

    **Dispersion Options Ensemble Size**

    The number of sets of dispersion options in the ensemble.

    _Accepted Values_

    Any positive integer.

    **Met Ensemble Size**

    The number of met cases in the ensemble.

    _Accepted Values_

    Any positive integer.

    !!! warning
        Enw currently defaults these both to 1. Attempts at customising
        this within the config will result in an error.
    """

    name: str
    dispersion_options_ensemble_size: int
    met_ensemble_size: int

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str | None,
        dispersion_options_ensemble_size: int,
        met_ensemble_size: int
    ) -> MultipleCase:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        name : str | None
            Name of the block.
        dispersion_options_ensemble_size : int
            The number of sets of dispersion options in the ensemble.
        met_ensemble_size : int
            The number of met cases in the ensemble.

        """
        if name is None:
            name = ""
        check_type("name", name, str)
        check_type(
            "dispersion_options_ensemble_size",
            dispersion_options_ensemble_size,
            int
        )
        check_pos_int(
            "dispersion_options_ensemble_size",
            dispersion_options_ensemble_size
        )
        check_type(
            "met_ensemble_size",
            met_ensemble_size,
            int
        )
        check_pos_int("met_ensemble_size", met_ensemble_size)
        return cls(
            name=name,
            dispersion_options_ensemble_size=dispersion_options_ensemble_size,
            met_ensemble_size=met_ensemble_size
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "multiplecase.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="multiplecase.jinja"
        --8<-- "./src/enw/files/block_templates/multiplecase.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("multiplecase.jinja")
        return template.render(
            name=self.name,
            dispersion_options_ensemble_size=(
                self.dispersion_options_ensemble_size
            ),
            met_ensemble_size=self.met_ensemble_size
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Multiple Case Options]"
            ] + [
                f"\t{k:<35}: {v}"
                for k, v in self.__dict__.items()
                if k[0] != "_"
            ]
        )


@dataclass(kw_only=True)
class OpenMP(NAMEIIIHeaderInputBlock):
    """Configuration for the OpenMP Options block for NAME III.

    The `OpenMP Options:` block contains the following columns:

    **Use OpenMP?**

    Enable parallelisation using OpenMP.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Parallelise the run |
    | "No" | Single threaded run |

    **Threads**

    Number of threads to use in any parallelised for loop.

    _Accepted Values_

    Any positive integer.

    **Particle Threads**

    Number of threads to use in the particle for loop.

    **Set to `Threads` if not specified**

    _Accepted Values_

    Any positive integer.

    **Particle Update Threads**

    Number of threads to use in the particle update for loop.

    **Set to `Threads` if not specified**

    _Accepted Values_

    Any positive integer.

    **Chemistry Threads**

    Number of threads to use in the chemistry for loop.

    **Set to `Threads` if not specified**

    _Accepted Values_

    Any positive integer.

    **Output Group Threads**

    Number of threads to use in the output group for loop.

    **Set to `Threads` if not specified**

    _Accepted Values_

    Any positive integer.

    **Output Process Threads**

    Number of threads to use when processing the output.

    _Accepted Values_

    Any positive integer.

    **Parallel MetRead**

    Read the NWP MetData with a separate IO thread.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Use a separate thread. |
    | "No" | Use the same thread. |

    !!! note
        This is a Switch variable but is not closed with a question mark (?)
        character...

    **Parallel MetProcess**

    Process the NWP MetData with a separate IO thread.

    _Accepted Values_

    | Option | Result |
    |--------|--------|
    | "Yes" | Use a separate thread. |
    | "No" | Use the same thread. |

    !!! note
        This is a Switch variable but is not closed with a question mark (?)
        character...

    """

    use_openmp: Switch
    threads: int | None
    particle_threads: int | None
    particle_update_threads: int | None
    chemistry_threads: int | None
    output_group_threads: int | None
    output_process_threads: int | None
    parallel_metread: Switch | None
    parallel_metprocess: Switch | None

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        use_openmp: bool,
        threads: int | None = None,
        particle_threads: int | None = None,
        particle_update_threads: int | None = None,
        chemistry_threads: int | None = None,
        output_group_threads: int | None = None,
        output_process_threads: int | None = None,
        parallel_metread: bool | None = None,
        parallel_metprocess: bool | None = None
    ) -> OpenMP:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        use_openmp : bool
            Enable parallelisation.
        threads : int | None, default=None
            Number of threads to use.
        particle_threads : int | None, default=None
            Number of threads to use for particle loop.
        particle_update_threads : int | None, default=None
            Number of threads to use for particle update loop.
        chemistry_threads : int | None, default=None
            Number of threads to use for chemistry loop.
        output_group_threads : int | None, default=None
            Number of threads to use for output group loop.
        output_process_threads : int | None, default=None
            Number of threads to use for output processing.
        parallel_metread : bool | None, default=None
            Read met data in separate thread?
        parallel_metprocess : bool | None, default=None
            Process met data in separate thread?

        """
        check_type("use_openmp", use_openmp, bool)
        use_openmp_switch = make_switch(use_openmp)
        if not use_openmp:
            return cls(
                use_openmp=use_openmp_switch,
                threads=None,
                particle_threads=None,
                particle_update_threads=None,
                chemistry_threads=None,
                output_group_threads=None,
                output_process_threads=None,
                parallel_metread=None,
                parallel_metprocess=None
            )

        if threads is not None:
            check_type("threads", threads, int)
            check_pos_int("threads", threads)
        if particle_threads is not None:
            check_type("particle_threads", particle_threads, int)
            check_pos_int("particle_threads", particle_threads)
        if particle_update_threads is not None:
            check_type("particle_update_threads", particle_update_threads, int)
            check_pos_int("particle_update_threads", particle_update_threads)
        if chemistry_threads is not None:
            check_type("chemistry_threads", chemistry_threads, int)
            check_pos_int("chemistry_threads", chemistry_threads)
        if output_group_threads is not None:
            check_type("output_group_threads", output_group_threads, int)
            check_pos_int("output_group_threads", output_group_threads)
        if output_process_threads is not None:
            check_type("output_process_threads", output_process_threads, int)
            check_pos_int("output_process_threads", output_process_threads)
        if parallel_metread is not None:
            check_type("parallel_metread", parallel_metread, bool)
            parallel_metread_switch = make_switch(parallel_metread)
        else:
            parallel_metread_switch = None
        if parallel_metprocess is not None:
            check_type("parallel_metprocess", parallel_metprocess, bool)
            parallel_metprocess_switch = make_switch(parallel_metprocess)
        else:
            parallel_metprocess_switch = None
        return cls(
            use_openmp=use_openmp_switch,
            threads=threads,
            particle_threads=particle_threads,
            particle_update_threads=particle_update_threads,
            chemistry_threads=chemistry_threads,
            output_group_threads=output_group_threads,
            output_process_threads=output_process_threads,
            parallel_metread=parallel_metread_switch,
            parallel_metprocess=parallel_metprocess_switch
        )


    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "openmp.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="openmp.jinja"
        --8<-- "./src/enw/files/block_templates/openmp.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("openmp.jinja")
        return template.render(
            use_openmp=self.use_openmp,
            threads=self.threads,
            particle_threads=self.particle_threads,
            particle_update_threads=self.particle_update_threads,
            chemistry_threads=self.chemistry_threads,
            output_group_threads=self.output_group_threads,
            output_process_threads=self.output_process_threads,
            parallel_metread=self.parallel_metread,
            parallel_metprocess=self.parallel_metprocess
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[OpenMP Options]"
            ] + [
                f"\t{k:<30}: {v}"
                for k, v in self.__dict__.items()
                if k[0] != "_"
            ]
        )

@dataclass(kw_only=True)
class DispersionOptions(NAMEIIIHeaderInputBlock):
    """Configuration for the Sets of Dispersion Options block for NAME III.

    The `Sets of Dispersion Options:` block contains the following columns:

    ??? information Columns
        **Max # Particles**

        Maximum number of particles that can be used.

        _Accepted Values_

        Positive integer value.

        **Max # Full Particles**

        Maximum number of full particles that can be used. A full particle
        is a particle that has options that differ it from a basic particle.
        i.e. velocity memory or plume rise. This is not particularly well
        documented in the input header file documentation.

        _Accepted Values_

        Positive integer value.

        **Max # Puffs**

        Maximum number of puffs that can be used.

        _Accepted Values_

        Positive integer value.

        **Max # Original Puffs**

        Maximum number of original puffs that can be used. Original puffs
        are those released at the source, not created by puff splitting.

        _Accepted Values_

        Positive integer value.

        **Particle Ceiling**

        !!! warning
            Not currently implemented.

        **Particle Factor**

        !!! warning
            Not currently implemented.

        **Skew Time**

        Travel time over which the model allows for skewness in the velocity
        variance profile.

        _Accepted Values_

        Time interval.

        **Velocity Memory Time**

        Travel time for which the more expensive dispersion scheme with
        velocity memory is used. Set to 00:00 to use cheap scheme for the whole
        run.

        _Accepted Values_

        Time interval.

        **Inhomogeneous Time**

        Travel time for which the height dependent inhomogeneous velocity
        variance profile is used. Set to 00:00 to use the homogenous profile
        for the whole run.

        _Accepted Values_

        Time interval.

        **Mesoscale Velocity Memory Time**

        Travel time for which the more expensive dispersion scheme with
        velocity memory is used for the unresolved mesoscale motions component
        of the velocity field. Set to 00:00 to use the cheap scheme for the
        while run.

        _Accepted Values_

        Time interval.

        **Damping?**

        !!! warning
            Not currently implemented.

        **Puff Time**

        Travel time over which puffs are used. Set to 00:00 to use particles
        for entire run.

        _Accepted Values_

        Time interval.

        **Sync Time**

        Time interval at which particles are synchronised.

        _Accepted Values_

        Time interval.

        **Computational Domain**

        Domain of interest.

        _Accepted Values_

        Any previously defined domain.

        **Puff Interval**

        Interval between puff releases.

        _Accepted Values_

        Time interval.

        **DeltaOpt**

        Modelling option applied in puff scheme.

        _Accepted Values_

        **==Unclear==**

        **Time of Fixed Met**

        Time of met to use for fixed met run.

        _Accepted Values_

        Datetime.

        **Deep Convection?**

        Switch a deep convection scheme on/off.

        !!! information
            Not actually a switch statement...

        _Accepted Values_

        `No`, `Old` or `New`.

        **Radioactive Decay?**

        Switch radioactive decay on/off for relevant species.

        _Accepted Values_

        `Yes` or `No`.

        **Agent Decay?**

        Switch agent decay on/off.

        _Accepted Values_

        `Yes` or `No`.

        **Dry Deposition?**

        Switch dry deposition on/off.

        _Accepted Values_

        `Yes` or `No`.

        **Wet Deposition?**

        Switch wet deposition on/off.

        _Accepted Values_

        `Yes` or `No`.

        **Max Deposition Height**

        !!! warning
            Not currently implemented.

        **Sedimentation Scheme**

        !!! warning
            Not currently implemented.

        **Mesoscale Motions?**

        Switch modelling of unresolved mesoscale motions on/off.

        _Accepted Values_

        `Yes` or `No`.

        **Chemistry?**

        Switch chemistry on/off.

        _Accepted Values_

        `Yes` or `No`.

        **Turbulence?**

        Switch turbulence on/off.

        _Accepted Values_

        `Yes` or `No`.

        **A1**

        !!! warning
            Not currently implemented.

        **A5**

        !!! warning
            Not currently implemented.

        **A7**

        !!! warning
            Not currently implemented.

        **Vertical Velocity?**

        !!! warning
            Not currently implemented.

        **Eulerian BCs File Stem**

        !!! warning
            Not currently implemented.

        **Eulerian BCs dT**

        !!! warning
            Not currently implemented.

        **Use Next BC Value?**

        !!! warning
            Not currently implemented.

        **Allow Particle Creation Error?**

        !!! warning
            Not currently implemented.

        **BC Domain**

        !!! warning
            Not currently implemented.

        **Eulerian Monotonicity?**

        !!! warning
            Not currently implemented.


    """

    max_num_particles: int
    "Corresponds to **Max # Particles**."
    max_num_full_particles: int
    max_num_puffs: int
    max_num_original_puffs: int
    particle_ceiling: NotImplementedType | None = None
    particle_factor: NotImplementedType | None = None
    skew_time: TimeInterval
    velocity_memory_time: TimeInterval
    inhomogeneous_time: TimeInterval
    mesoscale_velocity_memory_time: TimeInterval
    damping: NotImplementedType | None = None
    puff_time: TimeInterval
    sync_time: TimeInterval
    computational_domain: str
    puff_interval: TimeInterval
    delta_opt: str #INFO: I'm not sure about this one so use str for now
    time_of_fixed_met: DateTime
    deep_convection: DeepConvectionOpts
    radioactive_decay: Switch
    agent_decay: Switch
    dry_deposition: Switch
    wet_deposition: Switch
    max_deposition_height: NotImplementedType | None = None
    sedimentation_scheme: NotImplementedType | None = None
    mesoscale_motions: Switch
    chemistry: Switch
    turbulence: Switch
    a1: NotImplementedType | None = None
    a5: NotImplementedType | None = None
    a7: NotImplementedType | None = None
    vertical_velocity: NotImplementedType | None = None
    eulerian_bcs_filestem: NotImplementedType | None = None
    eulerian_bcs_dt: NotImplementedType | None = None
    use_next_bc_value: NotImplementedType | None = None
    allow_particle_creation_error: NotImplementedType | None = None
    bc_domain: NotImplementedType | None = None
    eulerian_monotonicity: NotImplementedType | None = None

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        max_num_particles: int,
        max_num_full_particles: int,
        max_num_puffs: int,
        max_num_original_puffs: int,
        skew_time: str,
        velocity_memory_time: str,
        inhomogeneous_time: str,
        mesoscale_velocity_memory_time: str,
        puff_time: str,
        sync_time: str,
        computational_domain: str,
        puff_interval: str,
        delta_opt: str,
        time_of_fixed_met: str,
        deep_convection: str,
        radioactive_decay: bool,
        agent_decay: bool,
        dry_deposition: bool,
        wet_deposition: bool,
        mesoscale_motions: bool,
        chemistry: bool,
        turbulence: bool,
        particle_ceiling: None = None,
        particle_factor: None = None,
        damping: None = None,
        max_deposition_height: None = None,
        sedimentation_scheme: None = None,
        a1: None = None,
        a5: None = None,
        a7: None = None,
        vertical_velocity: None = None,
        eulerian_bcs_filestem: None = None,
        eulerian_bcs_dt: None = None,
        use_next_bc_value: None = None,
        allow_particle_creation_error: None = None,
        bc_domain: None = None,
        eulerian_monotonicity: None = None,
    ) -> DispersionOptions:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        max_num_particles : int
            Maximum number of particles that can be used.

            Corresponds to **Max # Particles**

        max_num_full_particles : int
            Maximum number of full particles that can be used.

            Corresponds to **Max # Full Particles**

        max_num_puffs : int
            Maximum number of puffs that can be used,

            Corresponds to **Max # Puffs**

        max_num_original_puffs : int
            Maximum number of original puffs that can be used.

            Corresponds to **Max # Original Puffs**

        skew_time : str
            Travel time over which skew ca eist in velocity variance profile.

            Corresponds to **Skew Time**

        velocity_memory_time : str
            How long to use the more expensive dispersion scheme for.

            Corresponds to **Velocity Memory Time**

        inhomogeneous_time : str
            How long to use high dependent inhomogeneous velocity variance
            profile.

            Corresponds to **Inhomogeneous Time**

        mesoscale_velocity_memory_time : str
            How long to use more expensive diffusion scheme with velocity
            memory.

            Corresponds to **Menoscale Velocity Memory Time**

        puff_time : str
            How long are puffs used?

            Corresponds to **Puff Time**

        sync_time : str
            How long until particles are synchronised.

            Corresponds to **Sync Time**

        computational_domain : str
            Domain of interest.

            Corresponds to **Computational Domain**

        puff_interval : str
            Interval between puff releases.

            Corresponds to **Puff Interval**

        delta_opt : str
            Modelling option applied in puff scheme.

            Corresponds to **DeltaOpt**

        time_of_fixed_met : str
            Time of met used for fixed met run.

            Corresponds to **Time of Fixed Met**

        deep_convection : str
            Use a deep convection scheme?

            Corresponds to **Deep Convection?**

        radioactive_decay : bool
            Toggle radioactive decay for relevant species.

            Corresponds to **Radioactive Decay?**

        agent_decay : bool
            Toggle agent decay.

            Corresponds to **Agent Decay?**

        dry_deposition : bool
            Toggle dry deposition.

            Corresponds to **Dry Deposition?**

        wet_deposition : bool
            Toggle wet deposition.

            Corresponds to **Wet Deposition?**

        mesoscale_motions : bool
            Toggle mesoscale motions.

            Corresponds to **Menoscale Motions?**

        chemistry : bool
            Toggle chemistry.

            Corresponds to **Chemistry?**

        turbulence : bool
            Toggle turbulence.

            Corresponds to **Turbulence?**

        particle_ceiling : None = None
            ==Not currently implemented==

            Corresponds to **Particle Ceiling**

        particle_factor : None = None
            ==Not currently implemented==

            Corresponds to **Particle Factor**

        damping : None = None
            ==Not currently implemented==

            Corresponds to **Damping?**

        a1 : None = None
            ==Not currently implemented==

            Corresponds to **A1**

        a5 : None = None
            ==Not currently implemented==

            Corresponds to **A5**

        a7 : None = None
            ==Not currently implemented==

            Corresponds to **A7**

        vertical_velocity : None, default=None
            ==Not currently implemented==

            Corresponds to **Vertical Velocity?**

        eulerian_bcs_filestem : None, default=None
            ==Not currently implemented==

            Corresponds to **Eulerian BCs File Stem**

        eulerian_bcs_dt : None, default=None
            ==Not currently implemented==

            Corresponds to **Eulerian BCs dT**

        use_next_bc_value : None, default=None
            ==Not currently implemented==

            Corresponds to **Use Next BC Value?**

        allow_particle_creation_error : None, default=None
            ==Not currently implemented==

            Corresponds to **Allow Particle Creation Error?**

        bc_domain : None, default=None
            ==Not currently implemented==

            Corresponds to **BC Domain**

        eulerian_monotonicity : None, default=None
            ==Not currently implemented==

            Corresponds to **Eulerian Monotonicity?**


        Returns
        -------
        DispersionOptions

        Raises
        ------
        NotImplementedError
            Unimplemented keys are used.

        """
        _pos_int_args = (
            ("max_num_particles", max_num_particles),
            ("max_num_full_particles", max_num_full_particles),
            ("max_num_puffs", max_num_puffs),
            ("max_num_original_puffs", max_num_original_puffs),
        )
        _time_intervals = (
            ("skew_time", skew_time),
            ("velocity_memory_time", velocity_memory_time),
            ("inhomogeneous_time", inhomogeneous_time),
            ("mesoscale_velocity_memory_time", mesoscale_velocity_memory_time),
            ("puff_time", puff_time),
            ("sync_time", sync_time),
            ("puff_interval", puff_interval),
        )
        _datetimes = (
            ("time_of_fixed_met", time_of_fixed_met),
        )
        _switch_statements = (
            ("radioactive_decay", radioactive_decay),
            ("agent_decay", agent_decay),
            ("dry_deposition", dry_deposition),
            ("wet_deposition", wet_deposition),
            ("mesoscale_motions", mesoscale_motions),
            ("chemistry", chemistry),
            ("turbulence", turbulence),
        )
        _base_types = (
            ("computational_domain", computational_domain, str),
            ("delta_opt", delta_opt, str),
        )
        _unimplemented = (
            ("particle_ceiling", particle_ceiling),
            ("particle_factor", particle_factor),
            ("damping", damping),
            ("a1", a1),
            ("a5", a5),
            ("a7", a7),
            ("vertical_velocity", vertical_velocity),
            ("eulerian_bcs_filestem", eulerian_bcs_filestem),
            ("eulerian_bcs_dt", eulerian_bcs_dt),
            ("use_next_bc_value", use_next_bc_value),
            ("allow_particle_creation_error", allow_particle_creation_error),
            ("bc_domain", bc_domain),
            ("eulerian_monotonicity", eulerian_monotonicity)
        )
        #INFO: Check positive integers
        for name, val in _pos_int_args:
            check_type(name, val, int)
            check_pos_int(name, val)

        #INFO: Check time intervals
        time_intervals: dict[str, TimeInterval] = {}
        for name, val in _time_intervals:
            check_type(name, val, str)
            check_time_interval(name, val)
            time_intervals[name] = make_time_interval(val)

        #INFO: Check datetimes
        datetimes: dict[str, DateTime] = {}
        for name, val in _datetimes:
            check_type(name, val, str)
            check_datetime(name, val)
            datetimes[name] = DateTime(val)

        #INFO: Check switch_statements
        switches: dict[str, Switch] = {}
        for name, val in _switch_statements:
            check_type(name, val, bool)
            switches[name] = make_switch(val)

        #INFO: Check standard types
        for name, val, type_to_check in _base_types:
            check_type(name, val, type_to_check)

        #INFO: Check literals
        literals = {}
        check_type("deep_convection", deep_convection, str)
        check_literal(
            "deep_convection",
            deep_convection,
            "DeepConvectionOpts",
            DeepConvectionOpts
        )
        literals["deep_convection"] = cast(
            "DeepConvectionOpts",
            deep_convection
        )

        #INFO: Check not implemented variables
        for k, v in _unimplemented:
            if v is not None:
                msg = (
                    f"{k} was specified but is not implemented for Sets of "
                    "Dispersion Options."
                )
                raise NotImplementedError(msg)

        return cls(
            max_num_particles=max_num_particles,
            max_num_full_particles=max_num_full_particles,
            max_num_puffs=max_num_puffs,
            max_num_original_puffs=max_num_original_puffs,
            skew_time=time_intervals["skew_time"],
            velocity_memory_time=time_intervals["velocity_memory_time"],
            inhomogeneous_time=time_intervals["inhomogeneous_time"],
            mesoscale_velocity_memory_time=time_intervals["mesoscale_velocity_memory_time"],
            puff_time=time_intervals["puff_time"],
            sync_time=time_intervals["sync_time"],
            computational_domain=computational_domain,
            puff_interval=time_intervals["puff_interval"],
            delta_opt=delta_opt,
            time_of_fixed_met=datetimes["time_of_fixed_met"],
            deep_convection=literals["deep_convection"],
            radioactive_decay=switches["radioactive_decay"],
            agent_decay=switches["agent_decay"],
            dry_deposition=switches["dry_deposition"],
            wet_deposition=switches["wet_deposition"],
            mesoscale_motions=switches["mesoscale_motions"],
            chemistry=switches["chemistry"],
            turbulence=switches["turbulence"],
            particle_ceiling=particle_ceiling,
            particle_factor=particle_factor,
            damping=damping,
            max_deposition_height=max_deposition_height,
            sedimentation_scheme=sedimentation_scheme,
            a1=a1,
            a5=a5,
            a7=a7,
            vertical_velocity=vertical_velocity,
            eulerian_bcs_filestem=eulerian_bcs_filestem,
            eulerian_bcs_dt=eulerian_bcs_dt,
            use_next_bc_value=use_next_bc_value,
            allow_particle_creation_error=allow_particle_creation_error,
            bc_domain=bc_domain,
            eulerian_monotonicity=eulerian_monotonicity
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "dispersionoptions.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="dispersionoptions.jinja"
        --8<-- "./src/enw/files/block_templates/dispersionoptions.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("dispersionoptions.jinja")
        return template.render(
            max_num_particles=self.max_num_particles,
            max_num_full_particles=self.max_num_full_particles,
            max_num_puffs=self.max_num_puffs,
            max_num_original_puffs=self.max_num_original_puffs,
            skew_time=self.skew_time,
            velocity_memory_time=self.velocity_memory_time,
            inhomogeneous_time=self.inhomogeneous_time,
            mesoscale_velocity_memory_time=self.mesoscale_velocity_memory_time,
            puff_time=self.puff_time,
            sync_time=self.sync_time,
            computational_domain=self.computational_domain,
            puff_interval=self.puff_interval,
            delta_opt=self.delta_opt,
            time_of_fixed_met=self.time_of_fixed_met,
            deep_convection=self.deep_convection,
            radioactive_decay=self.radioactive_decay,
            agent_decay=self.agent_decay,
            dry_deposition=self.dry_deposition,
            wet_deposition=self.wet_deposition,
            max_deposition_height=self.max_deposition_height,
            sedimentation_scheme=self.sedimentation_scheme,
            mesoscale_motions=self.mesoscale_motions,
            chemistry=self.chemistry,
            turbulence=self.turbulence,
            particle_ceiling=self.particle_ceiling,
            particle_factor=self.particle_factor,
            damping=self.damping,
            a1=self.a1,
            a5=self.a5,
            a7=self.a7,
            vertical_velocity=self.vertical_velocity,
            eulerian_bcs_filestem=self.eulerian_bcs_filestem,
            eulerian_bcs_dt=self.eulerian_bcs_dt,
            use_next_bc_value=self.use_next_bc_value,
            allow_particle_creation_error=self.allow_particle_creation_error,
            bc_domain=self.bc_domain,
            eulerian_monotonicity=self.eulerian_monotonicity,
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        return "\n".join(
            [
                "[Sets of Dispersion Options]"
            ] + [
                f"\t{k:<30}: {v}"
                for k, v in self.__dict__.items()
                if k[0] != "_"
            ]
        )
