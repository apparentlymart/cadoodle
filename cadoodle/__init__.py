
from dxfwrite import DXFEngine as dxf


class Drawing(object):

    def __init__(self):
        self.dwg = dxf.drawing(name="nonameyet.dxf")
        self.dwg.add_layer("LABELS")

    def save(self, filename):
        self.dwg.saveas(filename)

    def add_layer(self, name):
        self.dwg.add_layer(name, color=7)
        return Layer(self.dwg, name)


class Layer(object):

    def __init__(self, dwg, name):
        self.dwg = dwg
        self.name = name
        self.x = 0
        self.y = 0
        self._pen_down = True

    def pen_up(self):
        self._pen_down = False

    def pen_down(self):
        self._pen_down = True

    def move(self, xd, yd):
        self.x += xd
        self.y += yd

    def line(self, xd, yd):
        if self._pen_down:
            self.dwg.add(dxf.line(
                (self.x, self.y),
                (self.x + xd, self.y + yd),
                layer=self.name,
            ))
        self.move(xd, yd)

    def _arc(self, radius, a1, a2):
        if self._pen_down:
            self.dwg.add(dxf.arc(
                radius=radius,
                center=(self.x, self.y),
                startangle=a1,
                endangle=a2,
                layer=self.name,
            ))

    def north(self, dist):
        self.line(0, dist)

    def south(self, dist):
        self.line(0, -dist)

    def east(self, dist):
        self.line(dist, 0)

    def west(self, dist):
        self.line(-dist, 0)

    def curve_se_ccw(self, radius):
        self.y += radius
        self._arc(radius, 270, 360)
        self.x += radius

    def curve_ne_ccw(self, radius):
        self.x -= radius
        self._arc(radius, 0, 90)
        self.y += radius

    def curve_nw_ccw(self, radius):
        self.y -= radius
        self._arc(radius, 90, 180)
        self.x -= radius

    def curve_sw_ccw(self, radius):
        self.x += radius
        self._arc(radius, 180, 270)
        self.y -= radius

    def curve_se_cw(self, radius):
        self.x -= radius
        self._arc(radius, 270, 360)
        self.y -= radius

    def curve_ne_cw(self, radius):
        self.y -= radius
        self._arc(radius, 0, 90)
        self.x += radius

    def curve_nw_cw(self, radius):
        self.x += radius
        self._arc(radius, 90, 180)
        self.y += radius

    def curve_sw_cw(self, radius):
        self.y += radius
        self._arc(radius, 180, 270)
        self.x -= radius
