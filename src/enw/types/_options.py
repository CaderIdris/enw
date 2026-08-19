"""Discrete options in the NAME configuration blocks."""
from typing import Literal

Switch = Literal["Yes", "No"]
"""Represents a 'Switch' variable in the NAME III Input Header Files.

These variables are NAME's equivalent of boolean values, used to configure
'Switch' columns which end with a question mark (?) character.
Though NAME is mostly case insensitive, a single capital case option is
provided for each option to maintain consistency.
"""

AbsOrRelOpts = Literal[
    "Gregorian",
    "Absolute",
    "Relative",
    "360-day years"
]
"""`Absolute or Relative?` options in the `Main Options` configuration block.

These are the four valid options when informing NAME how the user will be
providing the date/time variables. Annoyingly, this option ends with a
question mark character (?) despite it not being a `Switch` variable.
"""

RandomSeedOpts = Literal[
    "Fixed",
    "Random",
    "Fixed (Parallel)",
    "Random (Parallel)"
]
"""`Random Seed` options in the `Main Options` configuration block.

These are the four valid options used to set how the random number generator
within NAME functions. The first two cover single threaded NAME runs, the
last two cover parallel runs. More information can be found in the
documentation of the `Main Options` block.
"""

HorizontalCoordSystems = Literal[
    "Lat-Long",
    "EMEP 50km Grid",
    "EMEP 150km Grid",
    "UK National Grid (m)",
    "UK National Grid (100m)",
]
"""`Name` options in the `Horizontal Coordinate Systems` configuration block.

These are all the preset names for the horizontal coordinate systems in NAME.
Using another value would result in a custom coordinate system.
"""

VerticalCoordSystems = Literal[
    "m agl",
    "m asl",
    "FL",
    "Pa"
]
"""`Name` options in the `Vertical Coordinate Systems` configuration block.

These are all the preset names for the vertical coordinate systems in NAME.
Using another value would result in a custom coordinate system.
"""

SourceShapeOpts = Literal[
    "Cuboid",
    "Ellipsoid",
    "Cylindroid",
    "Suzuki"
]
"""`Shape` options in the `Sources` configuration block.

These are the four valid shapes a source can take in NAME.
- Cuboid
- Ellipsoid
- Cylindroid
- Suzuki
"""

QuantityOpts = Literal[
    "Air Concentration", #INFO: Air concentration from particles or puffs
    "Mixing Ratio", #INFO: Mixing ratio output from particles or puffs
    "Dry Deposition Rate",
    "Wet Deposition Rate",
    "Deposition Rate",
    "Min Z", #INFO: Plume base height
    "# Particles",
    "# Puffs",
    "# Particle Steps",
    "# Puff Steps",
    "Mass",
    "Mean Z",
    "Sigma Z",
    "X Stats",
    "Mean Travel Time",
    "Puff Centres",
    "Sigma C",
    "Chemistry Field",
    "Eulerian Concentration", #INFO: Air concentration on Eulerian field
    "E Mixing Ratio", #INFO: Mixing ratio output for Chemistry Field species
    "Concentration", #INFO: Combined air concentration from particles and
    # fields
    "Sigma WW",
    "HSigma WW", #INFO: Vertical velocity variance for homogeneous turbulence
    # scheme in boundary layer or free-tropospheric turbulence value, depending
    # on the height
    "HSigma UU", #INFO: Horizontal velocity variance for homogeneous turbulence
    # scheme in boundary layer or free-tropospheric turbulence value, depending
    # on the height
    "Tau WW",
    "Mean Flow U",
    "Mean Flow V",
    "Mean Flow W",
    "Temperature (K)",
    "Potential Temperature (K)",
    "Specific Humidity",
    "Pressure (Pa)",
    "Density",
    "Topography",
    "u-star",
    "Sensible Heat Flux",
    "Boundary Layer Depth",
    "Wind Speed",
    "Wind Direction (degrees)",
    "Precipitation Rate (mm/hr)",
    "Temperature (C)",
    "Cloud Amount (oktas)",
    "Relative Humidity (%)",
    "Pasquill Stability",
    "# Particles By Species",
    "Progress (%)",
    "Clock Time",
    "X", #INFO: X coord at output location in user specified coordinate system
    "Y", #INFO: Y coord at output location in user specified coordinate system
    "Sigma VV",
    "Mesoscale Sigma VV",
    "Cloud Water (kg/kg)",
    "Cloud Ice (kg/kg)",
    "3d Cloud (Fraction)",
    "Roughness Length",
    "Sea Level Pressure (Pa)",
    "Photon Flux",
    "Adult Effective Cloud Gamma Dose",
    "Adult Lung Cloud Gamma Dose",
    "Adult Thyroid Cloud Gamma Dose",
    "Adult Bone Surface Cloud Gamma Dose",
    "Area at risk",
    "Land Use Fractions",
    "Canopy Water",
    "Leaf Area Index",
    "Canopy Height",
    "Stomatal Conductance",
    "Soil Moisture",
    "Land Fraction",
    "Convective Cloud Base", #INFO: Convective cloud base in m agl
    "Convective Cloud Top", #INFO: Convective cloud top in m agl
    "Eulerian Total Deposition Rate", #INFO: Total deposition rate from
    # Eulerian field
    "Eulerian Dry Deposition Rate", #INFO: Dry deposition rate from
    # Eulerian field
    "Eulerian Wet Deposition Rate", #INFO: Wet deposition rate from
    # Eulerian field
    "Reference Source Strength", #INFO: Reference source strength used by an
    # emission scheme
    "Actual Source Strength", #INFO: Actual source strength for a source taking
    # account of any emission scheme
    "Max Plume Rise Height", #INFO: Maximum rise height of (volcanic) plume
    "Plume Depth", #INFO: Depth of (volcanic) plume
    "Final volume flux", #INFO: Volume flux of (volcanic) plume at maximum rise
    # height
]
"""`Quantity` options in the `Output Requirements - Fields` config block.

These are all the quantities that NAME can output.

"""

TAvOrIntOpts = Literal[
    "Av",
    "Int",
    "No"
]
"""`T Av Or Int` options in the `Output Requirements - Fields` config block.

Can be one of the following three options:

|Option|Description|
|------|-----------|
|Av|Time averaging|
|Int|Time integrating|
|No|No time averaging or integration|

"""

DeepConvectionOpts = Literal[
    "No",
    "Old",
    "New"
]
"""`Deep Convection?` options in the `Sets of Dispersion Options` config block.

Despite allegedly being a Switch variable, it does not exclusively take Yes or
No.
In fact, it doesn't take Yes at all...
Can be one of the following three options:

|Option|Description|
|------|-----------|
|New|Use the new deep convection scheme.|
|Old|Use the old deep convection scheme.|
|No|Do not use any deep convection scheme.|

"""

BinaryFormatOpts = Literal[
    "BIG_ENDIAN",
    "NATIVE"
]
"""`Binary Format` options in the `NWP Met Definitions` config block.

Dictates how the binary data is stored. There are two examples given, but there
may be others including LITTLE_ENDIAN.

Can be one of at least two options:

|Option|Description|
|------|-----------|
|BIG_ENDIAN|Big endian style|
|NATIVE|The format native to the platform|

"""

FieldQualifierOpts = Literal[
    "Dynamic",
    "Total"
]
"""`Field Qualifiers` options in the `NWP Met File Structure Definition` block.

Specifies additional qualifiers for the input field.

Can be one of two options:

|Option|Description|
|------|-----------|
|Dynamic|Large scale|
|Total|Use with cloud fields|
"""

FileTypeOpts = Literal[
    "Name II",
    "PP",
    "GRIB",
    "NetCDF"
]
"""`File Type` options in the `NWP Met Definitions` config block.

File format of the met data.

Can be one of four options:

|Option|Description|
|------|-----------|
|Name II|NAME II formatted met data|
|PP|PP formatted met data|
|GRIB|GRIB formatted met data [^1]|
|NetCDF|NetCDF formatted met data [^2]|


[^1]:
    !!! info "GRIB Format"
        NAME must be compiled with ecCodes support.

[^2]:
    !!! info "NetCDF Format"
        NAME must be compiled with NetCDF support.

"""


FlowAttributeOpts = Literal[
    "Update",
    "Convert",
    "Flow",
    "Cloud",
    "Rain"
]
"""`Flow Order` and `Name` options in the `Flow Attributes` config block."""
