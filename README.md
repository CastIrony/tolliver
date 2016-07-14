#Tolliver

Tolliver generates a vector file containing a row of shapes in varying sizes. By importing this vector file into your CAM program, and cutting it out with a CNC machine, you can quickly identify the precise shape size needed to best achieve your desired fit.

Circles, triangles, squares, rectangles, and hexagons are supported. Squares, rectangles, and hexagons can have an optional dogbone effect added to the corners to compensate for the diameter of the mill:

![Tolliver shapes](https://cloud.githubusercontent.com/assets/260240/16830478/2a57ce34-4954-11e6-8cb2-57984c51eb5e.png)

All shapes are sized based on the diameter of an inscribed circle for ease of measurement:

![Tolliver sizing](https://cloud.githubusercontent.com/assets/260240/16830479/2a5963fc-4954-11e6-8932-2ab3efe26390.png)

**Installation**:

    Download and extract the lastest build. Run `python setup.py install` in the application folder.

**Usage**: 

    `tolliver (circle | triangle | square | rectangle | hexagon) [options]`

**Options**:

    `-h, --help                      Show this help message`
    `-t, --type=<filetype>           The type of the file (dxf or svg) [default: dxf]`
    `-o, --output=<file>             The output file path [default: output.<filetype>]`
    `-w, --width=<value>             The overall width of the material [default: 10.0]`
    `-s, --spacing=<value>           The physical spacing between items [default: 1.0]`
    `-c, --center=<value>            The value at the center of the line [default: 0.5]`
    `-r, --ratio=<value>             The ratio of the last item's value to the first item's value [default: 1.1]`
    `-W, --rectangle-width=<value>   The width applied to rectangles [default: 0.5]`
    `-d, --dogbone=<dogbone-style>   The type of dogbone effect applied to shape corners [default: none]`
    `-D, --drill=<value>             The diameter of dogbone effects applied to shape corners [default: 0.1]`

**Arguments**:

    `dogbone-style: none     No dogbone effect applied to rectangles`
                   `sides    Dogbone effect applied to the left and right sides of rectangles`
                   `ends     Dogbone effect applied to the top and bottom ends of rectangles`
                   `corners  Dogbone effect applied to the corners of rectangles`