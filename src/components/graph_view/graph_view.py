# graph_view.py
#
# Copyright 2023 Ideve Core
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations
import sys, time
from typing import List, Union
from gi.repository import Adw, Gio, GObject, Gdk, Gtk, cairo

from currencyconverter.define import APP_ID, RES_PATH


class GraphPoint:
    time: int
    value: int


@Gtk.Template(resource_path=f"{RES_PATH}/components/graph_view/graph_view.ui")
class GraphView(Adw.Bin):
    __gtype_name__ = "GraphView"

    TOP_PADDING: int = 24
    START_VALUE: int = 0
    END_VALUE: int = 1
    YELLOW_1: str = "#f9f06b"
    YELLOW_5: str = "#e5a50a"
    points: List[GraphPoint] = []
    min: Union[None, float] = None
    max: Union[None, float] = None
    duration: int
    last_index: int
    start_time: float
    current_time: float

    drawing_area = Gtk.Template.Child()
    min_label = Gtk.Template.Child()
    max_label = Gtk.Template.Child()

    def __init__(self):
        super(GraphView, self).__init__()
        self.drawing_area.set_draw_func(self.__draw_cb)

        def __callback_animation_target(value):
            self.current_time = time.perf_counter()

            self.drawing_area.queue_draw()

        spring_params = Adw.SpringParams.new(1, 1, 1)
        self.animation = Adw.SpringAnimation.new(
            self,
            self.START_VALUE,
            self.END_VALUE,
            spring_params,
            Adw.CallbackAnimationTarget.new(__callback_animation_target),
        )

        def animation_done(value):
            self.current_time = sys.maxsize
            self.drawing_area.queue_draw()

        self.animation.connect("done", animation_done)

        self.animation.follow_enable_animations_setting = False

        def darea_notify(value):
            self.drawing_area.queue_draw()

        self.drawing_area.connect("notify::scale-factor", darea_notify)
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect("notify::dark", self.drawing_area.queue_draw)
        style_manager.connect("notify::high-contrast", self.drawing_area.queue_draw)

    def run_animation(self):
        self.start_time = time.perf_counter()
        print(self.start_time)
        self.animation.play()

    def set_min(self, min: float):
        self.min = min
        self.min_label.label = "min"

    def set_max(self, min: float):
        self.max = min
        self.max_label.label = "min"

    def prepare_graph(self):
        self.animation.reset()

        self.points = []

        self.min = min(self.START_VALUE, self.END_VALUE)
        self.max = max(self.START_VALUE, self.END_VALUE)
        self.start_time = self.current_time = 0
        self.last_index = 0

        # spring.apply(animation)

        estimated = self.animation.estimated_duration

        if estimated == float("inf"):
            self.duration = -1

            self.label_box.opacity = 0
        else:
            self.duration = int(estimated * 1000)
            self.duration_label.label = "f"

            initial_point = {-10000000, self.START_VALUE - 1}

    def __set_color_from_fg(
        self, widget: Gtk.widget, cr: cairo.Context, alpha_multiplier: float
    ):
        rgba: Gdk.RGBA = self.drawing_area.get_color()
        rgba.alpha = rgba.alpha * alpha_multiplier
        Gdk.cairo_set_source_rgba(cr, rgba)

    def __set_color_from_string(
        self, widget: Gtk.Widget, cr: cairo.Context, color: str, alpha_multiplier: float
    ):
        rgba: Gdk.RGBA = {0, 0, 0, 1}

        rgba.parse(color)
        rgba.alpha = rgba.alpha * alpha_multiplier

        Gdk.cairo_set_source_rgba(cr, rgba)

    def __inverse_lerp(self, a: int, b: int, t: int):
        return (t - a) / (b - a)

    def __transform_y(self, hight: int, y: int) -> int:
        bottom_padding = self.label_box.get_height()
        height = hight - bottom_padding

        if self.min == self.max:
            return height / 2

        start = height - (height - self.TOP_PADDING) * self.__inverse_lerp(
            self.min, self.max, self.START_VALUE
        )
        end = height - (height - self.TOP_PADDING) * self.__inverse_lerp(
            self.min, self.max, self.END_VALUE
        )

        return Adw.lerp(start, end, y)

    def __transform_x(self, width: float, x: float) -> float:
        return x * width / self.duration

    def __draw_cb(
        self, drawing_area: Gtk.DrawingArea, cr: cairo.Content, width: int, height: int
    ):
        dark = Adw.StyleManager.get_default().get_dark()
        hc = Adw.StyleManager.get_default().get_high_contrast()

        y1: int = self.__transform_y(height, self.START_VALUE)
        y2: int = self.__transform_y(height, self.END_VALUE)

        assert not self.points is None

        if len(self.points) == 0:
            return

        cr.set_line_width(1)
        self.__set_color_from_fg(drawing_area, cr, 0.5 if hc else 0.15)

        cr.save()
        cr.translate(0, 0.5)

        cr.save()
        cr.set_dash({4, 2}, 0)
        cr.move_to(0, y1)
        cr.line_to(width, y1)
        cr.move_to(0, y2)
        cr.line_to(width, y2)
        cr.stroke()
        cr.restore()

        self.__set_color_from_fg(drawing_area, cr, 0.65 if hc else 0.25)
        for i in range(self.last_index, len(self.points)):
            x = self.__transform_x(width, self.points[i].time)
            y = self.__transform_y(height, self.points[i].value)

            if i == self.last_index:
                cr.move_to(x, y)

            cr.line_to(x, y)

        cr.stroke()
        cr.restore()

        if self.current_time == 0:
            return

        cr.new_path()

        last_x = 0

        for i in range(0, len(self.points)):
            if self.points[i].time > self.current_time:
                self.last_index = i - 1
                break

            x = self.__transform_x(width, self.points[i].time)
            y = self.__transform_y(height, self.points[i].value)
            last_x = x

            cr.line_to(x, y)

        path = cr.copy_path()

        if dark:
            self.__set_color_from_string(drawing_area, cr, self.YELLOW_5, 0.25)
        else:
            self.__set_color_from_string(drawing_area, cr, self.YELLOW_1, 0.5)

        cr.line_to(last_x, height)
        cr.line_to(self.__transform_x(width, self.points[0].time), height)
        cr.line_to(
            self.__transform_x(width, self.points[0].time),
            self.__transform_y(height, self.points[0].value),
        )
        cr.close_path()
        cr.fill()

        cr.append_path(path)

        cr.set_line_width(2)
        self.__set_color_from_string(
            drawing_area, cr, self.YELLOW_1 if dark else self.YELLOW_5, 1
        )
        cr.stroke()

    def unmap(self):
        super(GraphView, self).unmap()
        self.prepare_graph()
