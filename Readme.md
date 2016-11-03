# Point cloud annotation

## Note

The present Readme explains how to annotate point-clouds using CloudCompare and to export annotations to various formats including PLY or Semantic3D.

## How-to

### CloudCompare source install and modification

1. Download CloudCompare, a tool for 3D point cloud and mesh processing: [http://www.danielgm.net/cc/](http://www.danielgm.net/cc/)
2. Modify it to be able to export semantic classes, following our own [modification procedure](modifications.md)
3. Compile following the [official instructions](https://github.com/cloudcompare/trunk/blob/master/BUILD.md)


### Annotation

1. Open your own point-cloud (say mirabello.ply)
2. Segment your point-cloud in various entities following this rule:

	```[building, low-vegetation, man-made-terrain, ...]_[rubble, safe]```

	such that for example:

	```building_rubble``` or ```man-made-terrain_safe```
3. Save the whole project as Ascii clouds (a separate ascii cloud for each entity), in for example: ```mirabello_asc/```

### Export

Use [cc2semantic.py](cc2semantic.py) to export the whole cloud to:

* standard [ply](https://en.wikipedia.org/wiki/PLY_%28file_format%29) format: list of points with color corresponding to the semantic class

* or [Semantic3D](http://semantic3d.net/) format: two files _mirabello.txt_ (containing the points and corresponding colors) and _mirabello.labels_ (containing the list of semantic classes in the same order)

Tune the python script to get the right inputs and outputs.