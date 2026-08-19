from dataclasses import dataclass

from jinja2 import Environment, PackageLoader

_environment = Environment(
    loader=PackageLoader("enw", "files/block_templates"),
    autoescape=True
)
#INFO: This is initialised outside of the template class so all dataclasses
# share the same environment instead of creating a new one each time.
# Jinja prefers a shared environment and this reduces the memory requirements
# when building out a large set of blocks

@dataclass(kw_only=True)
class NAMEIIIHeaderInputBlock:
    """Template class for NAME config blocks."""

    def __init__(self) -> None:
        """Initialise the class without error checking or formatting."""
        self._environment = _environment

    def __repr__(self) -> str:
        """Return representation of object to print to console.

        Returns
        -------
        str
            Object contents, used for printing to console.

        Raises
        ------
        NotImplementedError
            This is the base config, it should not be called.

        """
        msg = "This functionality has not been implemented for BaseConfig."
        raise NotImplementedError(msg)
        return ""


    def __str__(self) -> str:
        """Return the configuration block for the NAME input header file.

        Returns
        -------
        str
            Formatted configuration block for NAME III Input Header File.

        Raises
        ------
        NotImplementedError
            This is the base config, it should not be called.

        """
        msg = "This functionality has not been implemented for BaseConfig."
        raise NotImplementedError(msg)
        return ""
