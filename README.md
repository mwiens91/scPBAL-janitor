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

+ the ID (e.g., px0444)
+ the date (e.g., 20161107)
+ the extra bits (e.g., breast_xenografts_s501p10)

provided those are available to manipulate (though a directory without a
recognized ID will be ignored).

There's also an option to enforce a new or existing naming format on the
common directory.

## Fun facts!

*sc* stands for single cell, short for [single cell
sequencing](https://en.wikipedia.org/wiki/Single_cell_sequencing).
*PBAL* stands for [post-bisulfite adapter
ligation](https://www.nature.com/protocolexchange/protocols/5857). Wow!
Very science!
