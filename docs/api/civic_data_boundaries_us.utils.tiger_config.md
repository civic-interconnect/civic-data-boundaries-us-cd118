# Module `civic_data_boundaries_us.utils.tiger_config`

## Classes

### `Path(self, *args, **kwargs)`

PurePath subclass that can make system calls.

Path represents a filesystem path but unlike PurePath, also offers
methods to do system calls on path objects. Depending on your system,
instantiating a Path will return either a PosixPath or a WindowsPath
object. You can also instantiate a PosixPath or WindowsPath directly,
but cannot instantiate a WindowsPath on a POSIX system or vice versa.

### `TigerConfig(self, base_url: str, state_layer_url: str, county_layer_url: str, local_state_dir: pathlib.Path, local_county_dir: pathlib.Path) -> None`

TigerConfig(base_url: str, state_layer_url: str, county_layer_url: str, local_state_dir: pathlib.Path, local_county_dir: pathlib.Path)

## Functions

### `dataclass(cls=None, /, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)`

Add dunder methods based on the fields defined in the class.

Examines PEP 526 __annotations__ to determine fields.

If init is true, an __init__() method is added to the class. If repr
is true, a __repr__() method is added. If order is true, rich
comparison dunder methods are added. If unsafe_hash is true, a
__hash__() method is added. If frozen is true, fields may not be
assigned to after instance creation. If match_args is true, the
__match_args__ tuple is added. If kw_only is true, then by default
all fields are keyword-only. If slots is true, a new class with a
__slots__ attribute is returned.

### `get_repo_root(levels_up: int = 3) -> pathlib.Path`

Return the root directory of this repo by walking up a fixed number of parent folders.

Defaults to 3 levels up, assuming this file is under `src/civic_data_boundaries_us/utils/`.
