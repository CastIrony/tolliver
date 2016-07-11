import ezdxf

class DXFRenderer:

    def __init__(self, filename):
        self.dxf = ezdxf.new('AC1027')
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.dxf.saveas(self.filename)

    def draw_circle(self, center, diameter):
        self.dxf.modelspace().add_circle(center, radius=diameter * 0.5)

    def draw_line(self, point1, point2):
        self.dxf.modelspace().add_line(point1, point2)

    def draw_rectangle(self, center, size):
        center_x, center_y = center
        width, height = size

        left   = center_x - 0.5 * width
        right  = center_x + 0.5 * width
        top    = center_y + 0.5 * height
        bottom = center_y - 0.5 * height

        self.dxf.modelspace().add_line((left,  top),    (right, top))
        self.dxf.modelspace().add_line((right, top),    (right, bottom))
        self.dxf.modelspace().add_line((right, bottom), (left,  bottom))
        self.dxf.modelspace().add_line((left,  bottom), (left,  top))

    def draw_rectangle_dogbone_sides(self, center, size, drill):
        center_x, center_y = center
        width, height = size

        left   = center_x - 0.5 * width
        right  = center_x + 0.5 * width
        top    = center_y + 0.5 * height
        bottom = center_y - 0.5 * height
        radius = drill * 0.5

        self.dxf.modelspace().add_line((left, top), (right, top))
        self.dxf.modelspace().add_arc((right, top - radius), radius, -90, 90)
        self.dxf.modelspace().add_line((right, top - drill), (right, bottom + drill))
        self.dxf.modelspace().add_arc((right, bottom + radius), radius, -90, 90)
        self.dxf.modelspace().add_line((right, bottom), (left, bottom)) 
        self.dxf.modelspace().add_arc((left, bottom + radius), radius, 90, -90)
        self.dxf.modelspace().add_line((left, bottom + drill), (left, top - drill))
        self.dxf.modelspace().add_arc((left, top - radius), radius, 90, -90)

    def draw_rectangle_dogbone_ends(self, center, size, drill):
        center_x, center_y = center
        width, height = size

        left   = center_x - 0.5 * width
        right  = center_x + 0.5 * width
        top    = center_y + 0.5 * height
        bottom = center_y - 0.5 * height
        radius = drill * 0.5

        self.dxf.modelspace().add_arc((left + radius, top), radius, 0, 180)
        self.dxf.modelspace().add_line((left + drill, top), (right - drill, top))
        self.dxf.modelspace().add_arc((right - radius, top), radius, 0, 180)
        self.dxf.modelspace().add_line((right, top), (right, bottom))
        self.dxf.modelspace().add_arc((right - radius, bottom), radius, 180, 0)
        self.dxf.modelspace().add_line((right - drill, bottom), (left + drill, bottom))
        self.dxf.modelspace().add_arc((left + radius, bottom), radius, 180, 0)
        self.dxf.modelspace().add_line((left, bottom), (left, top))

    def draw_rectangle_dogbone_corners(self, center, size, drill):
        center_x, center_y = center
        width, height = size

        left   = center_x - 0.5 * width
        right  = center_x + 0.5 * width
        top    = center_y + 0.5 * height
        bottom = center_y - 0.5 * height
        radius = drill * 0.5
        offset = radius * pow(2.0, 0.5)

        self.dxf.modelspace().add_arc((left + 0.5 * offset, top - 0.5 * offset), radius, 45, 225)
        self.dxf.modelspace().add_line((left + offset, top), (right - offset, top))
        self.dxf.modelspace().add_arc((right - 0.5 * offset, top - 0.5 * offset), radius, 315, 135)
        self.dxf.modelspace().add_line((right, top - offset), (right, bottom + offset))
        self.dxf.modelspace().add_arc((right - 0.5 * offset, bottom + 0.5 * offset), radius, 225, 45)
        self.dxf.modelspace().add_line((right - offset, bottom), (left + offset, bottom))
        self.dxf.modelspace().add_arc((left + 0.5 * offset, bottom + 0.5 * offset), radius, 135, 315)
        self.dxf.modelspace().add_line((left, bottom + offset), (left, top - offset))

    def draw_triangle(self, center, diameter):
        center_x, center_y = center
        radius = diameter * 0.5
        sqrt3 = pow(3, 0.5)

        point1 = (center_x, center_y + 2 * radius)
        point2 = (center_x + sqrt3 * radius, center_y - radius)
        point3 = (center_x - sqrt3 * radius, center_y - radius)

        self.dxf.modelspace().add_line(point1, point2)
        self.dxf.modelspace().add_line(point2, point3)
        self.dxf.modelspace().add_line(point3, point1)

    def draw_hexagon(self, center, diameter):
        center_x, center_y = center
        radius = diameter * 0.5
        sqrt3 = pow(3, 0.5)

        point1 = (center_x -     radius / sqrt3, center_y + radius)
        point2 = (center_x +     radius / sqrt3, center_y + radius)
        point3 = (center_x + 2 * radius / sqrt3, center_y)
        point4 = (center_x +     radius / sqrt3, center_y - radius)
        point5 = (center_x -     radius / sqrt3, center_y - radius)
        point6 = (center_x - 2 * radius / sqrt3, center_y)

        self.dxf.modelspace().add_line(point1, point2)
        self.dxf.modelspace().add_line(point2, point3)
        self.dxf.modelspace().add_line(point3, point4)
        self.dxf.modelspace().add_line(point4, point5)
        self.dxf.modelspace().add_line(point5, point6)
        self.dxf.modelspace().add_line(point6, point1)

    def draw_hexagon_dogbone_sides(self, center, diameter, drill):
        center_x, center_y = center
        radius = diameter * 0.5
        drill_radius = drill * 0.5
        sqrt3 = pow(3, 0.5)

        point1a = (center_x -       radius / sqrt3 - 0.5 * drill_radius * sqrt3,  center_y + radius - 1.5 * drill_radius)
        point1  = (center_x -       radius / sqrt3,                               center_y + radius)
        point2  = (center_x +       radius / sqrt3,                               center_y + radius)
        point2b = (center_x +       radius / sqrt3 + 0.5 * drill_radius * sqrt3,  center_y + radius - 1.5 * drill_radius)
        point3a = (center_x + 2.0 * radius / sqrt3 - 0.5 * drill_radius * sqrt3,  center_y +          1.5 * drill_radius)
        point3  = (center_x + 2.0 * radius / sqrt3,                               center_y)
        point4  = (center_x +       radius / sqrt3,                               center_y - radius)
        point4b = (center_x +       radius / sqrt3 -       drill_radius * sqrt3,  center_y - radius)
        point5a = (center_x -       radius / sqrt3 +       drill_radius * sqrt3,  center_y - radius)
        point5  = (center_x -       radius / sqrt3,                               center_y - radius)
        point6  = (center_x - 2.0 * radius / sqrt3,                               center_y)
        point6b = (center_x - 2.0 * radius / sqrt3 + 0.5 * drill_radius * sqrt3,  center_y +          1.5 * drill_radius)

        center1 = (center_x -       radius / sqrt3,                               center_y + radius -       drill_radius)
        center2 = (center_x +       radius / sqrt3,                               center_y + radius -       drill_radius)
        center3 = (center_x + 2.0 * radius / sqrt3 - 0.5 * drill_radius * sqrt3,  center_y +          0.5 * drill_radius)
        center4 = (center_x +       radius / sqrt3 - 0.5 * drill_radius * sqrt3,  center_y - radius + 0.5 * drill_radius)
        center5 = (center_x -       radius / sqrt3 + 0.5 * drill_radius * sqrt3,  center_y - radius + 0.5 * drill_radius)
        center6 = (center_x - 2.0 * radius / sqrt3 + 0.5 * drill_radius * sqrt3,  center_y +          0.5 * drill_radius)

        self.dxf.modelspace().add_arc(center1, drill_radius, 90, 210)
        self.dxf.modelspace().add_line(point1, point2)
        self.dxf.modelspace().add_arc(center2, drill_radius, -30, 90)
        self.dxf.modelspace().add_line(point2b, point3a)
        self.dxf.modelspace().add_arc(center3, drill_radius, -30, 90)
        self.dxf.modelspace().add_line(point3, point4)
        self.dxf.modelspace().add_arc(center4, drill_radius, 210, 330)
        self.dxf.modelspace().add_line(point4b, point5a)
        self.dxf.modelspace().add_arc(center5, drill_radius, 210, 330)
        self.dxf.modelspace().add_line(point5, point6)
        self.dxf.modelspace().add_arc(center6, drill_radius, 90, 210)
        self.dxf.modelspace().add_line(point6b, point1a)

    def draw_hexagon_dogbone_ends(self, center, diameter, drill):
        center_x, center_y = center
        radius = diameter * 0.5
        drill_radius = drill * 0.5
        sqrt3 = pow(3, 0.5)

        point1  = (center_x -       radius / sqrt3,                              center_y + radius)
        point1b = (center_x -       radius / sqrt3 +       drill_radius * sqrt3, center_y + radius)
        point2a = (center_x +       radius / sqrt3 -       drill_radius * sqrt3, center_y + radius)
        point2  = (center_x +       radius / sqrt3,                              center_y + radius)
        point3  = (center_x + 2.0 * radius / sqrt3,                              center_y)
        point3b = (center_x + 2.0 * radius / sqrt3 - 0.5 * drill_radius * sqrt3, center_y -          1.5 * drill_radius)
        point4a = (center_x +       radius / sqrt3 + 0.5 * drill_radius * sqrt3, center_y - radius + 1.5 * drill_radius)
        point4  = (center_x +       radius / sqrt3,                              center_y - radius)
        point5  = (center_x -       radius / sqrt3,                              center_y - radius)
        point5b = (center_x -       radius / sqrt3 - 0.5 * drill_radius * sqrt3, center_y - radius + 1.5 * drill_radius)
        point6a = (center_x - 2.0 * radius / sqrt3 + 0.5 * drill_radius * sqrt3, center_y -          1.5 * drill_radius)
        point6  = (center_x - 2.0 * radius / sqrt3,                              center_y)

        center1 = (center_x -       radius / sqrt3 + 0.5 * drill_radius * sqrt3, center_y + radius - 0.5 * drill_radius)
        center2 = (center_x +       radius / sqrt3 - 0.5 * drill_radius * sqrt3, center_y + radius - 0.5 * drill_radius)
        center3 = (center_x + 2.0 * radius / sqrt3 - 0.5 * drill_radius * sqrt3, center_y -          0.5 * drill_radius)
        center4 = (center_x +       radius / sqrt3,                              center_y - radius +       drill_radius)
        center5 = (center_x -       radius / sqrt3,                              center_y - radius +       drill_radius)
        center6 = (center_x - 2.0 * radius / sqrt3 + 0.5 * drill_radius * sqrt3, center_y -          0.5 * drill_radius)

        self.dxf.modelspace().add_arc(center1, drill_radius, 30, 150)
        self.dxf.modelspace().add_line(point1b, point2a)
        self.dxf.modelspace().add_arc(center2, drill_radius, 30, 150)
        self.dxf.modelspace().add_line(point2, point3)
        self.dxf.modelspace().add_arc(center3, drill_radius, -90, 30)
        self.dxf.modelspace().add_line(point3b, point4a)
        self.dxf.modelspace().add_arc(center4, drill_radius, -90, 30)
        self.dxf.modelspace().add_line(point4, point5)
        self.dxf.modelspace().add_arc(center5, drill_radius, 150, 270)
        self.dxf.modelspace().add_line(point5b, point6a)
        self.dxf.modelspace().add_arc(center6, drill_radius, 150, 270)
        self.dxf.modelspace().add_line(point6, point1)

    def draw_hexagon_dogbone_corners(self, center, diameter, drill):
        center_x, center_y = center
        radius = diameter * 0.5
        drill_radius = drill * 0.5
        sqrt3 = pow(3, 0.5)

        point1a = (center_x -       radius / sqrt3 - 0.5 * drill_radius, center_y + radius - 0.5 * drill_radius * sqrt3)
        point1b = (center_x -       radius / sqrt3 +       drill_radius, center_y + radius)
        point2a = (center_x +       radius / sqrt3 -       drill_radius, center_y + radius)
        point2b = (center_x +       radius / sqrt3 + 0.5 * drill_radius, center_y + radius - 0.5 * drill_radius * sqrt3)
        point3a = (center_x + 2.0 * radius / sqrt3 - 0.5 * drill_radius, center_y +          0.5 * drill_radius * sqrt3)
        point3b = (center_x + 2.0 * radius / sqrt3 - 0.5 * drill_radius, center_y -          0.5 * drill_radius * sqrt3)
        point4a = (center_x +       radius / sqrt3 + 0.5 * drill_radius, center_y - radius + 0.5 * drill_radius * sqrt3)
        point4b = (center_x +       radius / sqrt3 -       drill_radius, center_y - radius)
        point5a = (center_x -       radius / sqrt3 +       drill_radius, center_y - radius)
        point5b = (center_x -       radius / sqrt3 - 0.5 * drill_radius, center_y - radius + 0.5 * drill_radius * sqrt3)
        point6a = (center_x - 2.0 * radius / sqrt3 + 0.5 * drill_radius, center_y -          0.5 * drill_radius * sqrt3)
        point6b = (center_x - 2.0 * radius / sqrt3 + 0.5 * drill_radius, center_y +          0.5 * drill_radius * sqrt3)

        center1  = (center_x -       radius / sqrt3 + 0.5 * drill_radius, center_y + radius - 0.5 * drill_radius * sqrt3)
        center2  = (center_x +       radius / sqrt3 - 0.5 * drill_radius, center_y + radius - 0.5 * drill_radius * sqrt3)
        center3  = (center_x + 2.0 * radius / sqrt3 -       drill_radius, center_y)
        center4  = (center_x +       radius / sqrt3 - 0.5 * drill_radius, center_y - radius + 0.5 * drill_radius * sqrt3)
        center5  = (center_x -       radius / sqrt3 + 0.5 * drill_radius, center_y - radius + 0.5 * drill_radius * sqrt3)
        center6  = (center_x - 2.0 * radius / sqrt3 +       drill_radius, center_y)

        self.dxf.modelspace().add_arc(center1, drill_radius,  60, 180)
        self.dxf.modelspace().add_line(point1b, point2a)
        self.dxf.modelspace().add_arc(center2, drill_radius,   0, 120)
        self.dxf.modelspace().add_line(point2b, point3a)
        self.dxf.modelspace().add_arc(center3, drill_radius, -60,  60)
        self.dxf.modelspace().add_line(point3b, point4a)
        self.dxf.modelspace().add_arc(center4, drill_radius, 240, 360)
        self.dxf.modelspace().add_line(point4b, point5a)
        self.dxf.modelspace().add_arc(center5, drill_radius, 180, 300)
        self.dxf.modelspace().add_line(point5b, point6a)
        self.dxf.modelspace().add_arc(center6, drill_radius, 120, 240)
        self.dxf.modelspace().add_line(point6b, point1a)

