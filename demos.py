# -*- coding: utf-8 -*-
# @Time    : 2025/1/1 下午4:17
# @Author  : jensentsts
# @File    : demos.py
# @Description :

from manimee import *


class SimpleChart(Scene):
    """
    一个含有串联电抗、并联电容的简单供电系统
    manim demos.py SimpleChart -p
    """
    def construct(self):
        src = Source()
        t1 = Transformer2(True).next_to(src, RIGHT, buff=0)
        t2 = Transformer2(True).next_to(t1, RIGHT, buff=5)
        x1 = Inductance().move_to((t1.get_center() + t2.get_center())/2).align_to(t1.lines[0], DOWN)
        l1 = Line(t1.lines[0].get_right(), x1.lines[1].get_left())
        l2 = Line(x1.lines[0].get_right(), t2.lines[1].get_left())
        load = Load().next_to(t2.lines[0], RIGHT, buff=0)
        c1 = Capacitor().rotate(90*DEGREES).next_to(load, DOWN)
        l3 = Line(c1.lines[0].get_top(), (t2.buses[0].get_x(), c1.lines[0].get_top()[1], 0))
        gnd = Gnd().next_to(c1.lines[1], DOWN, buff=0)

        # 手动调整母线长……
        bus_start = t2.buses[0].get_start()
        t2.buses[0].put_start_and_end_on((bus_start[0], bus_start[1] - LINE_LENGTH, bus_start[2]), t2.buses[0].get_end())
        # 去掉t1电源测的母线
        t1.remove(t1.buses[1])

        self.add(VGroup(src, t1, x1, t2, load, c1, gnd, l1, l2, l3).move_to(ORIGIN))


class Elements(Scene):
    """
    元件展示
    manim demos.py Elements -p
    """
    def construct(self):
        g = VGroup(
            Bus(),
            Gnd(),
            Voltage(),
            Impedance(),
            Inductance(),
            Capacitor(),
            Source(),
            Transformer2(),
            Transformer3(),
            AutoTransformer2(),
            Load(),
            Reactor(),
        )
        g.arrange_in_grid()
        self.add(g)


