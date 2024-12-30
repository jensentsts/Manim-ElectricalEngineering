# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 下午9:23
# @Author  : jensentsts
# @File    : test.py
# @Description : 测试文件

from manim import *


RADICAL = 0.3
LINE_LENGTH = 0.3
BUS_SIZE = RADICAL * 1.6
TRIANGLE_SCALE = 0.15

NORMAL_COLOR = YELLOW_D


class Bus(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """母线"""
        super().__init__(*vmobjects, **kwargs)
        self.add(Line(ORIGIN,[0, BUS_SIZE, 0]))
        self.move_to(ORIGIN)


class Resistor(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """电阻/阻抗/导纳"""
        super().__init__(*vmobjects, **kwargs)
        self.add(Rectangle(WHITE, LINE_LENGTH, LINE_LENGTH * 2.25))
        # 引出线
        self.l1 = Line(ORIGIN,[LINE_LENGTH, 0, 0]).next_to(self, RIGHT, buff=0)
        self.l2 = Line(ORIGIN,[-LINE_LENGTH, 0, 0]).next_to(self, LEFT, buff=0)
        self.add(self.l1)
        self.add(self.l2)
        self.move_to(ORIGIN)


class Inductance(VGroup):
    def __init__(self,
                 *vmobjects,
                 arc_amount: int = 5,
                 **kwargs):
        """电感"""
        super().__init__(*vmobjects, **kwargs)
        for i in range(arc_amount):
            arc = Arc(0.11, angle=TAU/2)
            self.add(arc.next_to(self, LEFT, buff=0))
        # 引出线
        self.l1 = Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(self, DR, buff=0)
        self.l2 = Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(self, DL, buff=0)
        self.add(self.l1)
        self.add(self.l2)
        self.move_to(ORIGIN)


class Capacitor(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """电容"""
        super().__init__(*vmobjects, **kwargs)
        c1 = Line(ORIGIN, [0, LINE_LENGTH*2, 0])
        c2 = Line([LINE_LENGTH/2, 0, 0], [LINE_LENGTH/2, LINE_LENGTH*2, 0])
        self.add(c1, c2)
        self.move_to(ORIGIN)
        # 引出线
        self.l1 = Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(c1, LEFT, buff=0)
        self.l2 = Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(c2, RIGHT, buff=0)
        self.add(self.l1, self.l2)
        self.move_to(ORIGIN)


class Source(VGroup):
    def __init__(self,
                 *vmobjects,
                 bus: bool = False,
                 **kwargs):
        """电源"""
        super().__init__(*vmobjects, **kwargs)
        arc_up = Arc(RADICAL/4, angle=TAU/2, color=NORMAL_COLOR)
        arc_down = arc_up.copy().rotate(180*DEGREES).next_to(arc_up, DR, buff=0)
        c = Circle(RADICAL, color=WHITE)
        self.add(arc_up, arc_down)
        self.move_to(ORIGIN)
        self.add(c)
        # 引出线
        self.line = Line((0, 0, 0), (LINE_LENGTH, 0, 0)).next_to(self, RIGHT, buff=0)
        self.add(self.line)
        # 母线
        if bus:
            bus1 = Line(ORIGIN, [0, BUS_SIZE, 0]).move_to(self.line)
            self.add(bus1)
        self.move_to(ORIGIN)


class Transformer3(VGroup):
    def __init__(self,
                 *vmobjects,
                 bus: bool = False,
                 **kwargs):
        """三绕组变压器"""
        super().__init__(*vmobjects, **kwargs)
        # 圆圈
        triangle = Triangle().scale(0.01)
        c1 = Circle(RADICAL, color=NORMAL_COLOR).next_to(triangle, UP, buff=-0.12)
        c2 = c1.copy().next_to(triangle, DL, buff=-0.12)
        c3 = c1.copy().next_to(triangle, DR, buff=-0.12)
        self.add(c1, c2, c3)
        self.move_to(ORIGIN)
        # 引出线
        # TODO: 决定引出线方向
        self.l1 = Line(ORIGIN, [0, LINE_LENGTH, 0]).next_to(c1, UP, buff=0)
        self.l2 = Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(c2, LEFT, buff=0)
        self.l3 = Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(c3, RIGHT, buff=0)
        self.add(self.l1, self.l2, self.l3)
        # 母线
        if bus:
            bus1 = Line(ORIGIN, [BUS_SIZE, 0, 0]).move_to(self.l1)
            bus2 = bus1.copy().rotate(90*DEGREES).move_to(self.l2)
            bus3 = bus1.copy().rotate(90*DEGREES).move_to(self.l3)
            self.add(bus1, bus2, bus3)
        self.move_to(ORIGIN)


class Transformer2(VGroup):
    def __init__(self, *vmobjects,
                 bus: bool = False,
                 **kwargs):
        """双绕组变压器"""
        super().__init__(*vmobjects, **kwargs)
        # 圆圈
        c1 = Circle(RADICAL, color=NORMAL_COLOR)
        c2 = c1.copy().next_to(c1, LEFT, buff=-0.15)
        self.add(c1, c2)
        # 引出线
        # TODO: 决定引出线方向
        self.l1 = Line(ORIGIN, [LINE_LENGTH, 0, 0]).next_to(c1, RIGHT, buff=0)
        self.l2 = Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(c2, LEFT, buff=0)
        self.add(self.l1, self.l2)
        # 母线
        if bus:
            bus1 = Line(ORIGIN, [0, BUS_SIZE, 0]).move_to(self.l1)
            bus2 = bus1.copy().move_to(self.l2)
            self.add(bus1, bus2)
        self.move_to(ORIGIN)


class Load(VGroup):
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        """负荷"""
        super().__init__(*vmobjects, **kwargs)
        triangle = Triangle(color=NORMAL_COLOR).scale(TRIANGLE_SCALE).rotate(-90*DEGREES)
        line = Line(ORIGIN, [-LINE_LENGTH, 0, 0]).next_to(triangle, LEFT, buff=0)
        self.add(triangle, line)
        self.move_to(ORIGIN)


class Gnd(VGroup):
    def __init__(self, *vmobjects, **kwargs):
        """GND"""
        super().__init__(*vmobjects, **kwargs)
        self.line_vec = Line(ORIGIN, [0, LINE_LENGTH*2/3, 0])
        line_hor1 = Line(ORIGIN, [LINE_LENGTH*4/3, 0, 0]).next_to(self.line_vec, DOWN, buff=0)
        line_hor2 = Line(ORIGIN, [LINE_LENGTH*2/3, 0, 0]).next_to(line_hor1, DOWN, buff=LINE_LENGTH/4)
        line_hor3 = Line(ORIGIN, [LINE_LENGTH/2, 0, 0]).next_to(line_hor2, DOWN, buff=LINE_LENGTH/4)
        self.add(self.line_vec, line_hor1, line_hor2, line_hor3)
        self.move_to(ORIGIN)


class Elf(Scene):
    def construct(self):
        induct = Inductance()
        cap = Capacitor()
        src = Source()
        t2 = Transformer2()
        t3 = Transformer3()
        load = Load()

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
        self.play(FadeOut(src))
        self.play(Create(cap, 0.1))
        self.play(cap.animate.to_corner(UR))
        self.play(cap.animate.move_to(src))
        self.wait()
        self.play(Transform(cap, src))
        self.wait()


class SimpleGraph(Scene):
    def construct(self):
        ind = Inductance().to_edge(ORIGIN)
        gnd = Gnd().next_to(ind, DL, buff=0)
        self.play(Create(ind, 0.2), Create(Line(gnd.line_vec.get_top(), ind.l2.get_left())), Create(gnd, 0.4))

        self.wait()


class SimpleGraph2(Scene):
    def construct(self):
        src = Source()
        t1 = Transformer2().next_to(src, RIGHT, buff=0)
        load = Load().next_to(t1, RIGHT, buff=3)
        l1 = Line(t1.get_right(), load.get_left())
        self.play(Create(src, 0.15))
        self.play(Create(t1, 0.15))
        self.play(Create(load, 0.1), Create(l1, 0.15))
        self.wait()

        g = VGroup(src, t1, load, l1)
        self.play(g.animate.move_to(ORIGIN))
        self.play(g.animate.rotate(10*360*DEGREES), run_time=1)

        self.wait()

