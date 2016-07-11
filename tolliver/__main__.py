"""
Usage: tolliver (circle | triangle | hexagon | square | rectangle) [options]

Options:
    -h, --help                     Show this help message

    -t, --type=<filetype>           The type of the file (dxf or svg) [default: dxf]
    -o, --output=<file>             The output file path [default: output.<filetype>]
    -w, --width=<value>             The overall width of the material [default: 10.0]
    -s, --spacing=<value>           The physical spacing between items [default: 1.0]
    -c, --center=<value>            The value at the center of the line [default: 0.5]
    -r, --ratio=<value>             The ratio of the last item's value to the first item's value [default: 1.1]
    -W, --rectangle-width=<value>   The width applied to rectangles [default: 0.5]
    -d, --dogbone=<dogbone-style>   The type of dogbone effect applied to shape corners [default: none]
    -D, --drill=<value>             The diameter of dogbone effects applied to shape corners [default: 0.1]

Arguments:

    dogbone-style: none     No dogbone effect applied to rectangles
                   sides    Dogbone effect applied to the left and right sides of rectangles
                   ends     Dogbone effect applied to the top and bottom ends of rectangles
                   corners  Dogbone effect applied to the corners of rectangles
"""

import os, sys
from DXFRenderer import DXFRenderer
from docopt import docopt, DocoptExit
from cerberus import Validator

try:
    arguments = docopt(__doc__)
except DocoptExit:
    sys.exit(__doc__)

schema = { 
    '--type'             : { 'type' : 'string', 'allowed' : ['dxf', 'svg'] }, 
    '--output'           : { 'type' : 'string', 'empty' : False }, 
    '--width'            : { 'type' : 'float', 'coerce' : float },
    '--spacing'          : { 'type' : 'float', 'coerce' : float },
    '--center'           : { 'type' : 'float', 'coerce' : float },
    '--ratio'            : { 'type' : 'float', 'coerce' : float },
    '--rectangle-width'  : { 'type' : 'float', 'coerce' : float },
    '--dogbone'          : { 'type' : 'string', 'allowed' : ['none', 'sides', 'ends', 'corners'] },
    '--drill'            : { 'type' : 'float', 'coerce' : float },
    'circle'             : { 'type' : 'boolean' },
    'square'             : { 'type' : 'boolean' },
    'rectangle'          : { 'type' : 'boolean' },
    'triangle'           : { 'type' : 'boolean' },
    'hexagon'            : { 'type' : 'boolean' },
}

validator = Validator(schema)
validator.allow_unknown = True

if not validator.validate(arguments):
    exit(validator.errors)

validatedArguments = validator.document

spacing = validatedArguments['--spacing']
width = validatedArguments['--width']
ratio = validatedArguments['--ratio']
center  = validatedArguments['--center']
rectangle_width = validatedArguments['--rectangle-width']
dogbone = validatedArguments['--dogbone']
drill = validatedArguments['--drill']
file_type = validatedArguments['--type']
is_circle = validatedArguments['circle']
is_square = validatedArguments['square']
is_rectangle = validatedArguments['rectangle']
is_triangle = validatedArguments['triangle']
is_hexagon = validatedArguments['hexagon']

path = validatedArguments['--output'].replace('<filetype>', file_type)

count = int(width / spacing)
maxIndex = count - 1

print("Center: {0}".format(center))
print("Total Ratio: {0}".format(ratio))
print("Delta Ratio: {0}".format(pow(ratio, 1.0 / maxIndex)))
print("")


if file_type == 'dxf':
    rendererClass = DXFRenderer
elif file_type == 'svg':
    pass

with rendererClass(path) as renderer:
    renderer.draw_rectangle(center=(0, 0), size=(width, spacing))

    for index in range(count):
        x = -0.5 * (spacing * float(maxIndex)) + spacing * float(index)
        proportion = (float(index) / float(maxIndex) - 0.5) * 2.0
        value = pow(pow(ratio, 0.5), proportion) * center

        coordinates = (x, 0.0)

        print("({0}/{1}): {2}".format(index + 1, count, value))

        if is_circle:
            renderer.draw_circle(center=coordinates, diameter=value)
        elif is_triangle:
            renderer.draw_triangle(center=coordinates, diameter=value)
        elif is_square:
            if dogbone == 'none':
                renderer.draw_rectangle(center=coordinates, size=(value, value))
            elif dogbone == 'sides':
                renderer.draw_rectangle_dogbone_sides(center=coordinates, size=(value, value), drill=drill)
            elif dogbone == 'ends':
                renderer.draw_rectangle_dogbone_ends(center=coordinates, size=(value, value), drill=drill)
            elif dogbone == 'corners':
                renderer.draw_rectangle_dogbone_corners(center=coordinates, size=(value, value), drill=drill)
        elif is_rectangle:
            if dogbone == 'none':
                renderer.draw_rectangle(center=coordinates, size=(rectangle_width, value))
            elif dogbone == 'sides':
                renderer.draw_rectangle_dogbone_sides(center=coordinates, size=(rectangle_width, value), drill=drill)
            elif dogbone == 'ends':
                renderer.draw_rectangle_dogbone_ends(center=coordinates, size=(rectangle_width, value), drill=drill)
            elif dogbone == 'corners':
                renderer.draw_rectangle_dogbone_corners(center=coordinates, size=(rectangle_width, value), drill=drill)
        elif is_hexagon:
            if dogbone == 'none':
                renderer.draw_hexagon(center=coordinates, diameter=value)
            elif dogbone == 'sides':
                renderer.draw_hexagon_dogbone_sides(center=coordinates, diameter=value, drill=drill)
            elif dogbone == 'ends':
                renderer.draw_hexagon_dogbone_ends(center=coordinates, diameter=value, drill=drill)
            elif dogbone == 'corners':
                renderer.draw_hexagon_dogbone_corners(center=coordinates, diameter=value, drill=drill)