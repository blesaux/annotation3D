# Cloud Compare for point cloud annotation

## Note
This method discribed bellow has been tested with [CloudCompare 2.6.3.1](https://github.com/cloudcompare/trunk/releases/tag/v2.6.3.1)

A similar modification should be possible with newer version

## Objective
In order to generate the annotation file.
The cloud name needs to be added in the ASCII file generated during ASCII export.

## File to be modified

libs/qCC_io/AsciiFilter.cpp and cloudcompare_modified/libs/qCC_io/AsciiFilter.cpp

## Modification

In the include part of the cpp file, add:

```cpp
#include <iostream>
#include <QString>
#include <string>
#include <sstream>
```

At line 213, after:

```cpp
if (saveColumnsHeader){
    QString header("//");

    // INSERT HERE

    ...
}
```

insert :

```cpp
// modification for saving name
QString name_ = cloud->getName();
std::string name_std = name_.toStdString();
header.append(name_std.c_str());
header.append("\n");
header.append("//");
```
