# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 下午9:23
# @Author  : jensentsts
# @File    : manimee.py
# @Description : Manim in electrical engineering. 电气工程Manim。
from manim import *
from manim.typing import Vector3D

CIRCLE_RADIUS: float = 0.3                  # 圆形的默认半径
LINE_LENGTH: float = 0.3                    # 引出线默认长度
BUS_LENGTH: float = CIRCLE_RADIUS * 1.6     # 母线默认长度
LOAD_TRIANGLE_SCALE: float = 0.15           # 负荷符号三角形 相对于 Manim默认三角形 的缩放比例
VOLTAGE_OUTER_RADIUS: float = 0.1           # 电压圆环默认外径
AUTO_TRANSFORMER_ARC_RATE: float = 1.2      # 自耦变压器弧线的半径对于CIRCLE_RADIUS的倍率

NORMAL_COLOR: ManimColor = YELLOW_D         # 特殊颜色的默认颜色


class Bus(Line):
    """
    母线
    """
    def __init__(self,
                 buff=0,
                 path_arc=None,
                 **kwargs):
        super().__init__(ORIGIN, (0, BUS_LENGTH, 0), buff, path_arc, **kwargs)

    def prolong(self,
                length: float,
                direction: Vector3D = DOWN):
        """
        延长
        :param length: 长度
        :param direction: 延长方向。取投影向量方向。
        :return: self
        """
        direction.prod()
        return self


class Gnd(VGroup):
    """
    GND
    """
    def __init__(self, *vmobjects, **kwargs):
        """
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(*vmobjects, **kwargs)
        # 引出线（竖向）
        self.lines: list[Line] = [
            Line(ORIGIN, (0, LINE_LENGTH * 2 / 3, 0))
        ]
        self.add(*self.lines)
        # 三条横线（从长到短）
        self.line_hor1 = Line(ORIGIN, (LINE_LENGTH * 3 / 3, 0, 0)).next_to(self.lines[0], DOWN, buff=0)
        self.line_hor2 = Line(ORIGIN, (LINE_LENGTH * 2 / 3, 0, 0)).next_to(self.line_hor1, DOWN, buff=LINE_LENGTH / 4)
        self.line_hor3 = Line(ORIGIN, (LINE_LENGTH * 1 / 3, 0, 0)).next_to(self.line_hor2, DOWN, buff=LINE_LENGTH / 4)
        self.add(self.line_hor1, self.line_hor2, self.line_hor3)

        self.move_to(ORIGIN)


class Voltage(Annulus):
    """
    可视化电压电压，效果为圆环，外径反应电压数值大小，内径反应电压横分量大小。
    """
    def __init__(self,
                 voltage_level: float = 0,
                 voltage: complex = 0):
        """
        电压可视化
        :param voltage_level: 电压等级
        :param voltage: 实际电压
        """
        super().__init__(inner_radius=0, outer_radius=VOLTAGE_OUTER_RADIUS)
        self._voltage_level: float = voltage_level
        self._voltage: complex = 0
        self.voltage = voltage

    def _rectify_radius(self):
        self.clear_points()
        if self.voltage_level <= 0:
            self.outer_radius = VOLTAGE_OUTER_RADIUS
            self.inner_radius = 0
        else:
            self.outer_radius = abs(self.voltage) / self.voltage_level * VOLTAGE_OUTER_RADIUS
            if self.voltage.real == 0:
                self.inner_radius = self.outer_radius - 0.001
            else:
                self.inner_radius = self.voltage.imag / self.voltage.real * self.outer_radius
        self.generate_points()

    @property
    def voltage_level(self) -> float:
        """电压等级"""
        return self._voltage_level

    @voltage_level.setter
    def voltage_level(self,
                      voltage_level: float):
        self._voltage_level = voltage_level
        self._rectify_radius()

    @property
    def voltage(self) -> complex:
        """实际电压"""
        return self._voltage

    @voltage.setter
    def voltage(self,
                voltage: complex):
        self._voltage = voltage
        self._rectify_radius()


class Impedance(VGroup):
    """
    电阻/阻抗/导纳
    """
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        super().__init__(*vmobjects, **kwargs)
        # 阻抗符号（主体）
        self.rectangle: Rectangle = Rectangle(WHITE, LINE_LENGTH, LINE_LENGTH * 2.25)
        self.add(self.rectangle)
        # 引出线
        self.lines: list[Line] = [Line(ORIGIN, (LINE_LENGTH, 0, 0)).next_to(self, RIGHT, buff=0),
                                  Line(ORIGIN, (-LINE_LENGTH, 0, 0)).next_to(self, LEFT, buff=0)]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Inductance(VGroup):
    """
    电感
    """
    def __init__(self,
                 arc_amount: int = 5,
                 *vmobjects,
                 **kwargs):
        """
        :param arc_amount: 圆弧数量
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(*vmobjects, **kwargs)
        # 电感符号的圆弧
        self._arc_amount: int = arc_amount
        self.arcs: list[Arc] = []
        for i in range(self._arc_amount):
            arc: Arc = Arc(0.11, angle=TAU / 2).next_to(self, LEFT, buff=0)
            self.add(arc)
            self.arcs.append(arc)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, (LINE_LENGTH, 0, 0)).next_to(self, DR, buff=0), Line(ORIGIN, (-LINE_LENGTH, 0, 0)).next_to(self, DL, buff=0)
        ]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Capacitor(VGroup):
    """
    电容
    """
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        super().__init__(*vmobjects, **kwargs)
        # 电容符号的极板
        self.p1: Line = Line((LINE_LENGTH / 2, 0, 0), (LINE_LENGTH / 2, LINE_LENGTH * 2, 0))
        self.p2: Line = Line(ORIGIN, (0, LINE_LENGTH * 2, 0))
        self.add(self.p1, self.p2)
        self.move_to(ORIGIN)
        # 引出线
        self.lines: list[Line] = [Line(ORIGIN, (LINE_LENGTH, 0, 0)).next_to(self.p1, RIGHT, buff=0),
                                  Line(ORIGIN, (-LINE_LENGTH, 0, 0)).next_to(self.p2, LEFT, buff=0)]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class WithBuses(VGroup):
    """
    带母线元件基类
    """
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """
        :param bus: 是否绘制母线
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(*vmobjects, **kwargs)
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
    def bus(self,
            value: bool = True):
        self._bus = value
        if self._bus:
            self._rectify_buses()
            self.add(*self.buses)
        else:
            self.remove(*self.buses)

    def show_bus(self):
        self._bus = True
        self._rectify_buses()
        return self.animate.add(*self.buses)

    def hide_bus(self):
        self._bus = False
        return self.animate.remove(*self.buses)


class Source(WithBuses):
    """
    电源
    """
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """
        :param bus: 是否绘制母线
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(bus, *vmobjects, **kwargs)
        # 电源符号
        self.arc_up: Arc = Arc(CIRCLE_RADIUS / 4, angle=TAU / 2, color=NORMAL_COLOR)
        self.arc_down: Arc = self.arc_up.copy().rotate(180 * DEGREES).next_to(self.arc_up, DR, buff=0)
        self.circles: list[Circle] = [
            Circle(CIRCLE_RADIUS, color=WHITE)
        ]
        self.add(self.arc_up, self.arc_down)
        self.move_to(ORIGIN)
        self.add(*self.circles)
        # 引出线与母线
        self.lines: list[Line] = [
            Line((0, 0, 0), (LINE_LENGTH, 0, 0)).next_to(self, RIGHT, buff=0)
        ]
        self.add(*self.lines)
        # 母线
        self.buses: list[Bus] = [Bus()]
        self.bus = bus

        self.move_to(ORIGIN)


class Transformer2(WithBuses):
    """
    双绕组变压器
    """
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """
        :param bus: 是否绘制母线
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(bus, *vmobjects, **kwargs)
        # 圆圈
        self.circles: list[Circle] = [
            Circle(CIRCLE_RADIUS, color=NORMAL_COLOR)
        ]
        self.circles.append(self.circles[0].copy().next_to(self.circles[0], LEFT, buff=-0.15))
        self.add(*self.circles)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, (LINE_LENGTH, 0, 0)).next_to(self.circles[0], RIGHT, buff=0),
            Line(ORIGIN, (-LINE_LENGTH, 0, 0)).next_to(self.circles[1], LEFT, buff=0)
        ]
        self.add(*self.lines)
        # 母线
        self.buses: list[Bus] = [Bus() for i in range(2)]
        self.bus = bus

        self.move_to(ORIGIN)


class Transformer3(WithBuses):
    """
    三绕组变压器
    """
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """
        :param bus: 是否绘制母线
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(bus, *vmobjects, **kwargs)
        # 圆圈
        triangle = Triangle().scale(0.01)  # 用于给三绕组变压器三个圆圈定位 正三角形辅助作图 简单方便
        self.circles: list[Circle] = [
            Circle(CIRCLE_RADIUS, color=NORMAL_COLOR).next_to(triangle, DR, buff=-0.12),
            Circle(CIRCLE_RADIUS, color=NORMAL_COLOR).next_to(triangle, UP, buff=-0.12),
            Circle(CIRCLE_RADIUS, color=NORMAL_COLOR).next_to(triangle, DL, buff=-0.12)
        ]
        self.add(*self.circles)
        self.move_to(ORIGIN)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, (LINE_LENGTH, 0, 0)).next_to(self.circles[0], RIGHT, buff=0),
            Line(ORIGIN, (0, LINE_LENGTH, 0)).next_to(self.circles[1], UP, buff=0),
            Line(ORIGIN, (-LINE_LENGTH, 0, 0)).next_to(self.circles[2], LEFT, buff=0)
        ]
        self.add(*self.lines)
        # 母线
        self.buses: list[Bus] = [Bus() for i in range(3)]
        self.bus = bus

        self.move_to(ORIGIN)


class AutoTransformer2(WithBuses):
    """
    自耦双绕组变压器
    """
    def __init__(self,
                 bus: bool = False,
                 *vmobjects,
                 **kwargs):
        """
        :param bus: 是否绘制母线
        :param vmobjects: 同 VGroup
        :param kwargs: 同 VGroup
        """
        super().__init__(bus, *vmobjects, **kwargs)
        # 源泉
        self.circle: Circle = Circle(CIRCLE_RADIUS)
        # 弧线
        self.arc: Arc = Arc(CIRCLE_RADIUS * AUTO_TRANSFORMER_ARC_RATE, start_angle=TAU*3/4, angle=TAU/4)
        self.arc.align_to(self.circle, DOWN)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, (LINE_LENGTH, 0, 0)),
            Line(ORIGIN, (-LINE_LENGTH, 0, 0))
        ]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Load(VGroup):
    """
    负荷
    """
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        super().__init__(*vmobjects, **kwargs)
        # 三角形
        self.triangle = Triangle(color=NORMAL_COLOR).scale(LOAD_TRIANGLE_SCALE).rotate(-90 * DEGREES)
        self.add(self.triangle)
        # 引出线
        self.lines: list[Line] = [
            Line(ORIGIN, (-LINE_LENGTH, 0, 0)).next_to(self.triangle, LEFT, buff=0)
        ]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Reactor(VGroup):
    """
    电抗器
    """
    def __init__(self,
                 *vmobjects,
                 **kwargs):
        super().__init__(*vmobjects, **kwargs)
        # 3/4圆弧
        self.arc: Arc = Arc(CIRCLE_RADIUS, 0, TAU * 3 / 4)
        self.add(self.arc)
        # 直角
        arc_l1 = Line((-CIRCLE_RADIUS, -CIRCLE_RADIUS, 0), (-CIRCLE_RADIUS, 0, 0))
        arc_l2 = Line((-CIRCLE_RADIUS, -CIRCLE_RADIUS, 0), (0, -CIRCLE_RADIUS, 0))
        self.right_angle: RightAngle = RightAngle(arc_l1, arc_l2, length=CIRCLE_RADIUS)
        self.add(self.right_angle)
        # 引出线
        self.lines: list[Line] = [
            Line((CIRCLE_RADIUS, 0, 0), (2*CIRCLE_RADIUS, 0, 0)),
            Line((-CIRCLE_RADIUS, 0, 0), (-2*CIRCLE_RADIUS, 0, 0))
        ]
        self.add(*self.lines)

        self.move_to(ORIGIN)


class Scheme(VGroup):
    """
    Scheme
    """
    def __init__(self, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

