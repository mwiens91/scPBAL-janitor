![Python version](https://img.shields.io/badge/python-2-blue.svg)

# scPBAL janitor

Imports a bunch of directories with names like

```
20161107_PX0443_breastxenografts
eaves49f_px0494_additional_lanes
px0444_lane2_scMDS_EGL-318
px0582_breast_xenografts_s501p10
px0738
```

into a common directory, renaming them to a common format, making use of

+ the ID (e.g., PX0443)
+ the date (e.g., 20161107)
+ the extra bits (e.g., breastxenografts)

provided those are available to manipulate (though a directory without a
recognized ID will be ignored). The default import operation is a copy,
although a move can be performed if specified.

There's also an option (or there will be eventually) to enforce a new or
existing naming format on the common directory.

## Usage

First you need to setup the common directory you want your scPBAL data
in: copy [`config.yaml.example`](config.yaml.example) to `config.yaml`
and fill in the `home_scpbal_directory` (the scPBAL common directory).

To run the script, specify the directories directly with

```
./scpbal_janitor /path/to/directory1 /path/to/directory2 ...
```

or if you have a text file with a bunch of directories you can also run

```
./scpbal_janitor --directories-files /path/to/text/file
```

When in doubt, type

```
./scpbal_janitor --help
```

## Fun facts!

*sc* stands for single cell, short for [single cell
sequencing](https://en.wikipedia.org/wiki/Single_cell_sequencing).
*PBAL* stands for [post-bisulfite adapter
ligation](https://www.nature.com/protocolexchange/protocols/5857). Wow!
Very science!
