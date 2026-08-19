"""Configuration objects for all of the misc NAME III Input Header Blocks.

Covers:
- Input Files: `Input`

"""
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from enw.utils import check_path_like, check_type

from ._base import NAMEIIIHeaderInputBlock



@dataclass(kw_only=True)
class InputFiles(NAMEIIIHeaderInputBlock):
    """Configuration for the Input Files block for NAME III.

    When a list of input files is given to NAME, it imports them in order.
    This can be used to separate the configuration file into several logical
    groups.

    This block is not configured by the user directly, the input files
    are separated by the program.

    The `Input Files:` block contains a single column:

    **File Names**

    A list of input files.

    _Accepted Values_

    Can use absolute or relative paths.

    """

    files: tuple[Path, ...]

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        files: Iterable[str]
    ) -> InputFiles:
        """Configure a config block with error checking and formatting.

        Parameters
        ----------
        files : Iterable[str]
            A list of input files.

        """
        for i, f in enumerate(files):
            check_path_like(f"Input Files (Index {i})", f)
        return cls(
            files=tuple(Path(f) for f in files)
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "inputfiles.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="inputfiles.jinja"
        --8<-- "./src/enw/files/block_templates/inputfiles.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("inputfiles.jinja")
        return template.render(
            files=self.files
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
                "[Input Files]"
            ] + [
                f"\t{f}" for f in self.files
            ]
        )


@dataclass(kw_only=True)
class Array(NAMEIIIHeaderInputBlock):
    """"""

    name: str
    values: list[str]
    comments: list[str] | None = None
    comments_name: str | None = None

    def __post_init__(self) -> None:
        super().__init__()

    @classmethod
    def setup(
        cls,
        *,
        name: str,
        values: list[str | int | float],
        comments: list[str] | None = None,
        comments_name: str | None = None
    ) -> Array:
        """"""
        check_type("name", name, str)
        if not isinstance(values, Iterable) or isinstance(values, str):
            msg = (
                "values should be an iterable object (e.g. list, tuple) of "
                "strings."
            )
            raise TypeError(msg)
        for i, v in enumerate(values):
            check_type(f"{i}.values", v, str | int | float)
        if comments is not None:
            if comments_name is None:
                msg = "comments set while comments_name is not."
                raise ValueError(msg)
            check_type("comments_name", comments_name, str)
            if not isinstance(comments, Iterable) or isinstance(comments, str):
                msg = (
                    "comments should be an iterable object (e.g. list, tuple) "
                    "of strings."
                )
                raise TypeError(msg)
            for i, v in enumerate(comments):
                if v is None:
                    continue
                check_type(f"{i}.comments", v, str)
            if all(v is None for v in comments):
                comments = None
                comments_name = None
            else:
                comments = [c if c is not None else "" for c in comments]

        if comments is not None and len(values) != len(comments):
            msg = "values and comments are different lengths."
            raise ValueError(msg)


        return cls(
            name=name,
            values=[str(v) for v in values],
            comments=comments,
            comments_name=comments_name
        )

    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Passes the block configuration into the "array.jinja" block
        template to get the appropriate configuration block.

        ``` jinja title="array.jinja"
        --8<-- "./src/enw/files/block_templates/array.jinja"
        ```

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header file.

        """
        template = self._environment.get_template("array.jinja")
        return template.render(
            name=self.name,
            values=self.values,
            comments=self.comments,
            comments_name=self.comments_name
        )

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Representation of object.

        """
        repr_lines = [
            f"[Array - {self.name}]",
            "\tvalues",
            *[f"\t\t{v}" for v in self.values],
            f"\t{'comments_name':<32}: {self.comments_name}",
        ]
        if self.comments is not None:
            repr_lines.extend([
                "\tcomments",
                *[
                    f"\t\t{v}" for v in self.comments
                ]
            ])
        else:
            repr_lines.append(
                f"\t{'comments':<32}: None",
            )

        return "\n".join(repr_lines)
