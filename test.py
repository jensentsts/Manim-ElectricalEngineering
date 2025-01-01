# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 下午9:23
# @Author  : jensentsts
# @File    : test.py
# @Description : 测试文件
from manim import *

RADICAL = 0.3
LINE_LENGTH = 0.3
BUS_LENGTH = RADICAL * 1.6
TRIANGLE_SCALE = 0.15

NORMAL_COLOR = YELLOW_D


class Bus(Line):
    def __init__(self, buff=0, path_arc=None, **kwargs):
        """母线"""
        super().__init__(ORIGIN, [0, BUS_LENGTH, 0], buff, path_arc, **kwargs)


class Impedance(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """电阻/阻抗/导纳"""
        super().__init__(*vmobjects, **kwargs)
        # 阻抗符号（主体）
        self.rectangle: Rectangle = Rectangle(WHITE, LINE_LENGTH, LINE_LENGTH * 2.25)
        self.add(self.rectangle)
        # 引出线
        self.lines: list[Line] = [Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(self, RIGHT, buff=0),
                                  Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self, LEFT, buff=0)]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Inductance(VGroup):
    def __init__(self,
                 arc_amount: int = 5,
                 *vmobjects,
                 **kwargs):
        """电感"""
        super().__init__(*vmobjects, **kwargs)
        # 电感符号的圆弧
        self.arcs: list[Arc] = []
        for i in range(arc_amount):
            arc: Arc = Arc(0.11, angle=TAU / 2).next_to(self, LEFT, buff=0)
            self.add(arc)
            self.arcs.append(arc)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(self, DR, buff=0), Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self, DL, buff=0)
        ]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Capacitor(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """电容"""
        super().__init__(*vmobjects, **kwargs)
        # 电容符号的极板
        self.p1: Line = Line([LINE_LENGTH / 2, 0, 0], [LINE_LENGTH / 2, LINE_LENGTH * 2, 0])
        self.p2: Line = Line(ORIGIN, [0, LINE_LENGTH * 2, 0])
        self.add(self.p1, self.p2)
        self.move_to(ORIGIN)
        # 引出线
        self.lines: list[Line] = [Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(self.p1, RIGHT, buff=0),
                                  Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self.p2, LEFT, buff=0)]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class WithBuses:
    def __init__(self, bus: bool = False):
        """带母线元件"""
        self._bus = bus
        self.lines: list[Line] = []
        self.buses: list[Bus] = []
        self.bus = bus

    def _rectify_buses(self):
        """矫正母线角度和位置"""
        for l, b in zip(self.lines, self.buses):
            b.set_angle(l.get_angle() + 90 * DEGREES).move_to(l)

    @property
    def bus(self) -> bool:
        return self._bus

    @bus.setter
    def bus(self, value: bool = True):
        self._bus = value
        if self._bus:
            self._rectify_buses()
            self.add(*self.buses)
        else:
            self.remove(*self.buses)

    def add_bus(self):
        self._bus = True
        self._rectify_buses()
        return self.animate.add(*self.buses)

    def remove_bus(self):
        self._bus = False
        return self.animate.remove(*self.buses)


class Source(VGroup, WithBuses):
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """电源"""
        super().__init__(*vmobjects, **kwargs)
        # 电源符号
        self.arc_up: Arc = Arc(RADICAL / 4, angle=TAU / 2, color=NORMAL_COLOR)
        self.arc_down: Arc = self.arc_up.copy().rotate(180 * DEGREES).next_to(self.arc_up, DR, buff=0)
        self.c1: Circle = Circle(RADICAL, color=WHITE)
        self.add(self.arc_up, self.arc_down)
        self.move_to(ORIGIN)
        self.add(self.c1)
        # 引出线与母线
        self.lines: list[Line] = [
            Line((0, 0, 0), (LINE_LENGTH, 0, 0)).next_to(self, RIGHT, buff=0)
        ]
        self.add(*self.lines)
        # 母线
        self.buses: list[Bus] = [Bus()]
        self.bus = bus

        self.move_to(ORIGIN)


class Transformer3(VGroup, WithBuses):
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """三绕组变压器"""
        super().__init__(*vmobjects, **kwargs)
        # 圆圈
        triangle = Triangle().scale(0.01)  # 用于给三绕组变压器三个圆圈定位 正三角形辅助作图 简单方便
        self.c1: Circle = Circle(RADICAL, color=NORMAL_COLOR).next_to(triangle, UP, buff=-0.12)
        self.c2: Circle = self.c1.copy().next_to(triangle, DL, buff=-0.12)
        self.c3: Circle = self.c1.copy().next_to(triangle, DR, buff=-0.12)
        self.add(self.c1, self.c2, self.c3)
        self.move_to(ORIGIN)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, [0, LINE_LENGTH, 0]).next_to(self.c1, UP, buff=0),
            Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self.c2, LEFT, buff=0),
            Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(self.c3, RIGHT, buff=0)
        ]
        self.add(*self.lines)
        # 母线
        self.buses: list[Bus] = [Bus() for i in range(3)]
        self.bus = bus

        self.move_to(ORIGIN)


class Transformer2(VGroup, WithBuses):
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """双绕组变压器"""
        super().__init__(*vmobjects, **kwargs)
        # 圆圈
        self.c1 = Circle(RADICAL, color=NORMAL_COLOR)
        self.c2 = self.c1.copy().next_to(self.c1, LEFT, buff=-0.15)
        self.add(self.c1, self.c2)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(self.c1, RIGHT, buff=0),
            Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self.c2, LEFT, buff=0)
        ]
        self.add(*self.lines)
        # 母线
        self.buses: list[Bus] = [Bus() for i in range(2)]
        self.bus = bus

        self.move_to(ORIGIN)


class Load(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """负荷"""
        super().__init__(*vmobjects, **kwargs)
        # 三角形
        self.triangle = Triangle(color=NORMAL_COLOR).scale(TRIANGLE_SCALE).rotate(-90 * DEGREES)
        self.add(self.triangle)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self.triangle, LEFT, buff=0)
        ]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Gnd(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        """GND"""
        super().__init__(*vmobjects, **kwargs)
        # 引出线（竖向）
        self.lines: list[Line] = [
            Line(ORIGIN, [0, LINE_LENGTH * 2 / 3, 0])
        ]
        self.add(*self.lines)
        # 三条横线（从长到短）
        self.line_hor1 = Line(ORIGIN, [LINE_LENGTH * 4 / 3, 0, 0]).next_to(self.lines[0], DOWN, buff=0)
        self.line_hor2 = Line(ORIGIN, [LINE_LENGTH * 2 / 3, 0, 0]).next_to(self.line_hor1, DOWN, buff=LINE_LENGTH / 4)
        self.line_hor3 = Line(ORIGIN, [LINE_LENGTH / 2, 0, 0]).next_to(self.line_hor2, DOWN, buff=LINE_LENGTH / 4)
        self.add(self.line_hor1, self.line_hor2, self.line_hor3)

        self.move_to(ORIGIN)


class Scheme(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        """Scheme"""
        super().__init__(*vmobjects, **kwargs)


class ElementsDemo(Scene):
    def construct(self):
        induct = Inductance()
        cap = Capacitor()
        src = Source()
        t2 = Transformer2()
        t3 = Transformer3()
        load = Load()
        gnd = Gnd()

        self.play(Create(induct, 0.1))
        self.wait()
        self.play(induct.animate.to_edge(UP))
        self.play(Create(src, 0.1))
        self.wait()
        self.play(Create(t2.to_edge(RIGHT), 0.1))
        self.play(Create(t3.to_edge(DOWN), 0.1))
        self.wait()
        self.play(Create(load.to_edge(LEFT), 0.1))
        self.wait()
        self.play(t3.animate.scale(2))
        self.play(t3.animate.to_edge(DOWN))
        self.wait()
        self.play(src.animate.next_to(cap, LEFT),
                  Create(cap))
        self.play(Create(Line(src.lines[0].get_right(),
                              cap.lines[1].get_left())))
        self.wait()
        self.play(t3.animate.scale(0.5))
        self.play(t3.add_bus())

        self.wait(3)


class T232(Scene):
    def construct(self):
        t2 = Transformer2(bus=False)
        t22 = t2.copy()
        t3 = Transformer3(bus=True)
        self.add(t2)
        self.play(Transform(t2, t3))
        self.play(Transform(t2, t22))


class SimpleGraph(Scene):
    def construct(self):
        ind = Inductance().to_edge(ORIGIN)
        load = Load().next_to(ind.lines[0], RIGHT, buff=2)
        src = Source(True).next_to(ind.lines[1], LEFT, buff=0)
        load.triangle.set_color(WHITE)
        VGroup(ind, load, src).move_to(ORIGIN).scale(2)
        self.play(Create(src, 0.5),
                  Create(Line(src.lines[0].get_right(), ind.lines[1].get_left())),
                  Create(ind, 0.2),
                  Create(load))
        self.play(Create(Line(ind.lines[0].get_right(), load.lines[0].get_left())))
        self.play(load.triangle.animate.set_color(NORMAL_COLOR))

        self.wait()


class Power(Scene):
    def construct(self):
        v1 = Vector([2, 3])
        v2 = Vector([4, 6])
        label1 = v1.coordinate_label()
        label2 = v2.coordinate_label()
        plane = NumberPlane()
        self.add(plane, v1, v2, label1, label2)

