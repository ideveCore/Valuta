# window.py
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

import gi, math

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from typing import Union, Any, Dict
from gi.repository import Adw, Gdk, Gio, Graphene, Gtk
from .define import RES_PATH

# from .components import GraphView

resource = f"{RES_PATH}/window.ui"


class GraphView(Gtk.Box):
    __gtype_name__ = "GraphView"

    def __init__(self) -> None:
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=0, name="graph_box"
        )

    def do_snapshot(self, snapshot):
        allocation: Gdk.Rectangle = self.get_allocation()

        rect = Graphene.Rect()
        rect.init(0, 0, allocation.width, allocation.height)

        cr = snapshot.append_cairo(rect)
        cr.save()
        # temps is a array with graph position values
        temps = [
            83.12,
            81.14,
            80.06,
            80.06,
            79.88,
            79.88,
            80.06,
            79.7,
            78.62,
            78.62,
            78.62,
            78.62,
            78.44,
            78.25999999999999,
            79.52,
            81.5,
            82.4,
            84.2,
            84.92,
            85.64,
            86.53999999999999,
            86.36,
            85.46000000000001,
            83.66,
        ]

        min_temp = min(temps)
        max_temp = max(temps)

        values = None

        if not min_temp == max_temp:
            values = list(map(lambda t: (t - min_temp) / (max_temp - min_temp), temps))
        else:
            values = list(map(lambda t: t / 2, temps))

        width = self.get_allocated_width()
        height = self.get_allocated_height()

        entry_width = 75
        separator_width = 1

        line_width = 2
        entry_image_y = 56
        entry_image_height = 32
        entry_temperature_label_height = 19

        spacing = 18

        grap_min_y = line_width / 2 + entry_image_y + entry_image_height + spacing
        graph_max_y = (
            height - line_width / 2 - spacing - entry_temperature_label_height - spacing
        )
        graph_height = graph_max_y - grap_min_y

        points_gap = entry_width + separator_width

        stroke_color = self.get_style_context().lookup_color('weather_temp_chart_stroke_color')
        stroke_color = stroke_color.color
        Gdk.cairo_set_source_rgba(cr, stroke_color)
        # print(stroke_color.color)
        # TODO: i stoped here
        y_cords = []
        for i in range(len(values)):
            print(i)
            y_cords.append((grap_min_y + ((1 - values[i]) * graph_height)))


        gradients = []
        gradient_angles = []
        for i in range(len(y_cords)):
            prev_val = y_cords[i]
            next_val = prev_val
            if i > 0:
                prev_val = y_cords[i - 1]
            if i < len(y_cords) - 1:
                next_val = y_cords[i + 1]

            gradients.append((next_val - prev_val) / (2 * points_gap))
            gradient_angles.append(math.atan((next_val - prev_val) / (points_gap * 2)))

        x = -points_gap / 2

        cr.move_to(x, y_cords[0])
        smoothness_val = 0.4

        for i in range(len(y_cords)):
            x_dist_prev = points_gap * smoothness_val
            if i > 0:
                x_dist_prev = math.cos(gradient_angles[i - 1]) * points_gap * smoothness_val

            x_dist_current = points_gap * smoothness_val
            if i < len(y_cords):
                x_dist_current = math.cos(gradient_angles[i]) * points_gap * smoothness_val

            test = False

            prev_y_cord = (y_cords[i - 1]) if i > 0 else y_cords[i]
            prev_grad = (gradients[i - 1]) if i > 0 else  0

            curr_y_cord = (y_cords[i]) if i < len(y_cords) else y_cords[i - 1]
            curr_g_rad = (gradients[i]) if i < len(y_cords) else 0

            pt1 = [x + x_dist_prev, prev_y_cord + prev_grad * x_dist_prev]
            pt2 = [x + points_gap - x_dist_current, curr_y_cord - curr_g_rad * x_dist_current]

            cr.curve_to(
                pt1[0], pt1[1],
                pt2[0], pt2[1],
                x + points_gap, curr_y_cord
            )

            x += points_gap

        cr.line_to(width, grap_min_y + ((1 - values[len(values) - 1]) * graph_height))

        cr.set_line_width(line_width);
        cr.stroke_preserve()

        fill_color = self.get_style_context().lookup_color('weather_temp_chart_fill_color');
        fill_color = fill_color.color

        Gdk.cairo_set_source_rgba(cr, fill_color)

        cr.line_to(width, height)
        cr.line_to(0, height)
        cr.fill()
        cr.restore();

def create_main_window(application: Adw.Application):
    builder = Gtk.Builder.new_from_resource(resource)
    settings = application.utils["settings"]
    window = builder.get_object("window")
    graph_view = GraphView()
    add_graph = builder.get_object("graph_view")
    add_graph.set_child(graph_view)

    def load_window_state():
        settings["bind"](
            key="width",
            object=window,
            property="default-width",
            flags=Gio.SettingsBindFlags.DEFAULT,
        )
        settings["bind"](
            key="height",
            object=window,
            property="default-height",
            flags=Gio.SettingsBindFlags.DEFAULT,
        )
        settings["bind"](
            key="is-maximized",
            object=window,
            property="maximized",
            flags=Gio.SettingsBindFlags.DEFAULT,
        )
        settings["bind"](
            key="is-fullscreen",
            object=window,
            property="fullscreened",
            flags=Gio.SettingsBindFlags.DEFAULT,
        )

    load_window_state()
    window.set_application(application)
    return window
