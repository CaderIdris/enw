---
title: TODO
author: Idris Hayward
date: 2026-06-08
---

## Necessary Blocks:

* [x] Main Options
* [x] Restart File Options
* [x] Multiple Case Options
* [x] OpenMP Options
* [x] Output Options
* [x] Input Files
* [x] Horizontal Coordinate Systems
* [x] Vertical Coordinate Systems
* [x] Locations
* [x] Horizontal Grids
* [x] Vertical Grids
* [x] Temporal Grids
* [x] Domains
* [x] Output Requirements - Fields
* [x] Output Requirements - Set of Particle/Puff Information
* [x] Species
* [x] Sources
* [x] Sets of Dispersion Options - 22/36
* [x] NWP Met Definitions - 23(?)/24
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] NWP Met Module Instances - 10(?)/21
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] NWP Met File Structure Definition - 6/7
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] NWP Flow Module Instances - 5(?)/9
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] Flow Order - 2/2
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] Flow Attributes - 2/2
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] Species Uses - 4/5
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types
* [x] Array - 2/2
    * [x] Dataclass
        * [ ] Docstrings
    * [x] Setup function
        * [ ] Docstrings
    * [x] \_\_str\_\_
        * [x] Jinja
    * [x] \_\_repr\_\_
    * [x] Tests
        * [x] init
        * [x] str
        * [x] repr
        * [x] Bad types

* [ ] SPECIAL: Comment?

## Config

* [x] Main
    * [x] TypedDict
    * [x] Toml
    * [x] Defaults
    * [x] Tests
* [x] Output
    * [x] TypedDict
    * [x] Toml
    * [x] Defaults
    * [x] Tests
* [x] Restart
    * [x] TypedDict
    * [x] Toml
    * [x] Defaults
    * [x] Tests
* [x] OpenMP
    * [x] TypedDict
    * [x] Toml
    * [x] Defaults
    * [x] Tests
* [ ] Temporal Grids
    * [ ] Build off from main options (start and end time)
* [x] Hcoord
    * [x] TypedDict
    * Currently only accepts single value
    * [x] Defaults
    * [x] Tests
* [x] Vcoord
    * [x] TypedDict
    * Currently only accepts two values
    * [x] Defaults
    * [x] Tests
* [x] Multiple Case
    * [x] TypedDict
    * [x] Check
    * [x] Defaults
* [x] Locations
    * [x] TypedDict
    * [x] OpenGHG Defs loader (Sites)
        * [x] Tests
    * [x] Toml
        * [x] Overrides
    * [x] Tests
* [x] Domains
    * [x] TypedDict
    * [x] OpenGHG Defs loader (Domains)
        * [x] Tests
    * [x] Toml
        * [x] Overrides
    * [x] Tests
* [x] Horizontal Grids
    * [x] TypedDict
    * [x] OpenGHG Defs loader (Domains)
        * [x] Tests
    * [x] Toml
    * [x] Tests
* [ ] Vertical Grids
    * [x] TypedDict
    * [x] OpenGHG Defs loader (Locations)
        * [x] Tests
    * [x] Toml
    * [ ] Tests
* [x] Species
    * [x] TypedDict
    * [x] OpenGHG Defs loader (Species)
        * [x] Tests
    * [x] Toml
        * [x] Overrides
    * [x] Tests
* 🤷 Output Requirements
    * [x] TypedDict
        * [x] Fields
        * [x] Sets of Particle/Puff Information
    * ❌ Toml
        * ❌ Fields
        * ❌ Sets of Particle/Puff Information
    * [x] Defaults
        * [x] Fields
        * [x] Sets of Particle/Puff Information
    * ❌ Tests
        * ❌ Fields
        * ❌ Sets of Particle/Puff Information
    - ==Going to make it default for now, output both NAME III and NetCDF==
* [x] Sets of Dispersion Options
    * [x] TypedDict
    * [x] Toml
    * [x] Defaults
    * [x] Tests
* [ ] Sources
    * [ ] Build off from main options (start and end time)

* [ ] All the met and flow stuff AAAAAAAAAAAAAAAA

* [x] Set hcoord to lat-long when using openghg default (location)
* [x] Set hcoord to lat-long when using openghg default (domain)
* [ ] Raise error if openghg defaults used when lat-long not set
* [x] OpenGHG Locations: IGNORE:, heights, heights_units. subset
* [ ] Main domain title should default to "Dispersion Domain"
* [x] Add on_particles, on_fields, advect_fields to species return, default TFF
* [ ] Break up load function
* [ ] Main not present should raise error
* [ ] Output both NAME III and NetCDF for both particles and mixing ratio 
* [ ] Domains is HGrid ± (step size / 2)
