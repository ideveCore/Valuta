# history.py
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

import gi, cairo, math, threading
from typing import Any, Dict, Union, Optional
from gettext import gettext as _

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gio, Gtk, GLib
from ...components import CurrencySelector
from ...utils import CurrenciesListModel
# pyrefly: ignore [missing-import]
from ...define import RES_PATH, CODES
from ...requests import HistoryRequest

resource = f"{RES_PATH}/pages/history/index.ui"

def history_page(application: Adw.Application, from_currency_value: int = 1):
  builder = Gtk.Builder.new_from_resource(resource)
  settings = application.utils.settings
  page = builder.get_object("toast_overlay")
  
  from_currency_selector: CurrencySelector = builder.get_object("from_currency_selector")
  to_currency_selector: CurrencySelector = builder.get_object("to_currency_selector")
  invert_currencies: Gtk.Button = builder.get_object("invert_currencies")
  stack: Gtk.Stack = builder.get_object("stack")
  reload_btn: Gtk.Button = builder.get_object("reload_btn")
  toast_overlay: Adw.ToastOverlay = builder.get_object("toast_overlay")

  rate_summary_label: Gtk.Label = builder.get_object("rate_summary_label")
  change_label: Gtk.Label = builder.get_object("change_label")
  date_label: Gtk.Label = builder.get_object("date_label")

  chart_area: Gtk.DrawingArea = builder.get_object("chart_area")
  stat_min_label: Gtk.Label = builder.get_object("stat_min_label")
  stat_avg_label: Gtk.Label = builder.get_object("stat_avg_label")
  stat_max_label: Gtk.Label = builder.get_object("stat_max_label")

  btn_1w: Gtk.ToggleButton = builder.get_object("btn_1w")
  btn_1m: Gtk.ToggleButton = builder.get_object("btn_1m")
  btn_3m: Gtk.ToggleButton = builder.get_object("btn_3m")
  btn_1y: Gtk.ToggleButton = builder.get_object("btn_1y")
  btn_5y: Gtk.ToggleButton = builder.get_object("btn_5y")

  period_buttons = {
    7: btn_1w,
    30: btn_1m,
    90: btn_3m,
    365: btn_1y,
    1825: btn_5y
  }

  current_days = 30
  history_data: Optional[Dict[str, Any]] = None
  hover_index: Optional[int] = None
  is_loading = False

  def currency_names_func(code):
    name = _(CODES.get(code, '')['name'])
    return name if name else None

  def load_currencies(provider: int):
    codes = {currency: details for currency, details in CODES.items() if str(provider) in details['providers']}
    from_currency_model = CurrenciesListModel(application, currency_names_func)
    to_currency_model = CurrenciesListModel(application, currency_names_func)
    from_currency_selector.bind_models(from_currency_model)
    from_currency_model.set_currencies(codes)
    to_currency_selector.bind_models(to_currency_model)
    to_currency_model.set_currencies(codes)
    
    if not settings.get_string('src-currency') in codes or not settings.get_string('dest-currency') in codes:
      settings.set_string("src-currency", "USD")
      settings.set_string("dest-currency", "EUR")

    from_currency_selector.set_selected(settings.get_string('src-currency'))
    to_currency_selector.set_selected(settings.get_string('dest-currency'))

  def update_summary(point_idx: Optional[int] = None):
    nonlocal history_data
    if not history_data or "points" not in history_data or not history_data["points"]:
      return

    points = history_data["points"]
    if point_idx is None or point_idx < 0 or point_idx >= len(points):
      point_idx = len(points) - 1

    target = points[point_idx]
    rate_val = target["rate"]
    date_val = target["date"]

    from_code = from_currency_selector.selected
    to_code = to_currency_selector.selected

    formatted_rate = application.utils.format_number(f"{rate_val:.4f}")
    if not formatted_rate:
      formatted_rate = f"{rate_val:.4f}"
    rate_summary_label.set_text(f"1 {from_code} = {formatted_rate} {to_code}")

    chg = history_data.get("change", 0.0)
    chg_pct = history_data.get("change_pct", 0.0)
    sign = "+" if chg >= 0 else ""
    change_text = f"{sign}{chg:.4f} ({sign}{chg_pct:.2f}%)"
    change_label.set_text(change_text)

    if chg >= 0:
      change_label.remove_css_class("error")
      change_label.add_css_class("success")
    else:
      change_label.remove_css_class("success")
      change_label.add_css_class("error")

    date_label.set_text(date_val)

  def fetch_history(force: bool = False):
    nonlocal history_data, hover_index, is_loading
    provider = settings.get_enum("providers")

    from_code = from_currency_selector.selected
    to_code = to_currency_selector.selected
    if not from_code or not to_code:
      return

    stack.set_visible_child_name("loading")
    hover_index = None
    is_loading = True

    def on_history_loaded(data: Dict[str, Any]):
      nonlocal history_data, is_loading
      is_loading = False
      if not isinstance(data, dict):
        stack.set_visible_child_name("error")
        return False

      if not data.get("supported", True):
        stack.set_visible_child_name("unsupported")
        return False

      if "error" in data:
        stack.set_visible_child_name("error")
        return False

      history_data = data
      stack.set_visible_child_name("result")

      min_fmt = application.utils.format_number(f"{data['min']:.4f}") or f"{data['min']:.4f}"
      avg_fmt = application.utils.format_number(f"{data['avg']:.4f}") or f"{data['avg']:.4f}"
      max_fmt = application.utils.format_number(f"{data['max']:.4f}") or f"{data['max']:.4f}"

      stat_min_label.set_text(min_fmt)
      stat_avg_label.set_text(avg_fmt)
      stat_max_label.set_text(max_fmt)

      update_summary()
      chart_area.queue_draw()
      return False

    def bg_worker(p, f, t, d):
      try:
        req = HistoryRequest(p, f, t, d)
        res = req.get()
        GLib.idle_add(on_history_loaded, res)
      except Exception as err:
        GLib.idle_add(on_history_loaded, {"supported": True, "error": str(err)})

    threading.Thread(target=bg_worker, args=(provider, from_code, to_code, current_days), daemon=True).start()

  def draw_chart(area, cr: cairo.Context, width: int, height: int):
    nonlocal history_data, hover_index
    if not history_data or "points" not in history_data or not history_data["points"]:
      return

    points = history_data["points"]
    rates = [p["rate"] for p in points]
    min_r = min(rates)
    max_r = max(rates)

    pad_top = 24
    pad_bottom = 32
    pad_left = 20
    pad_right = 20

    chart_w = width - pad_left - pad_right
    chart_h = height - pad_top - pad_bottom

    if chart_w <= 0 or chart_h <= 0:
      return

    if max_r == min_r:
      min_r -= min_r * 0.01 if min_r != 0 else 0.01
      max_r += max_r * 0.01 if max_r != 0 else 0.01

    val_span = max_r - min_r
    plot_min = min_r - val_span * 0.08
    plot_max = max_r + val_span * 0.08
    plot_span = plot_max - plot_min

    # Grid reference lines
    cr.set_line_width(1)
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.15)
    for i in range(3):
      y = pad_top + (i / 2.0) * chart_h
      cr.move_to(pad_left, y)
      cr.line_to(width - pad_right, y)
      cr.stroke()

    coords = []
    n = len(points)
    for i, p in enumerate(points):
      x = pad_left + (i / max(1, n - 1)) * chart_w
      y = pad_top + (1.0 - (p["rate"] - plot_min) / plot_span) * chart_h
      coords.append((x, y))

    is_positive = history_data.get("change", 0.0) >= 0
    if is_positive:
      line_r, line_g, line_b = (0.18, 0.76, 0.49)
    else:
      line_r, line_g, line_b = (0.88, 0.11, 0.14)

    # Area Gradient fill
    gradient = cairo.LinearGradient(0, pad_top, 0, height - pad_bottom)
    gradient.add_color_stop_rgba(0.0, line_r, line_g, line_b, 0.28)
    gradient.add_color_stop_rgba(1.0, line_r, line_g, line_b, 0.01)

    cr.move_to(coords[0][0], height - pad_bottom)
    for x, y in coords:
      cr.line_to(x, y)
    cr.line_to(coords[-1][0], height - pad_bottom)
    cr.close_path()
    cr.set_source(gradient)
    cr.fill()

    # Trend Line
    cr.set_line_width(2.5)
    cr.set_source_rgb(line_r, line_g, line_b)
    cr.move_to(coords[0][0], coords[0][1])
    for x, y in coords[1:]:
      cr.line_to(x, y)
    cr.stroke()

    # Dates at bottom
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.75)
    cr.set_font_size(10)

    start_str = points[0]["date"]
    end_str = points[-1]["date"]

    cr.move_to(pad_left, height - 8)
    cr.show_text(start_str)

    extents = cr.text_extents(end_str)
    cr.move_to(width - pad_right - extents.width, height - 8)
    cr.show_text(end_str)

    # Hover cursor indicator
    if hover_index is not None and 0 <= hover_index < len(coords):
      hx, hy = coords[hover_index]

      cr.set_source_rgba(0.5, 0.5, 0.5, 0.45)
      cr.set_line_width(1)
      cr.set_dash([4.0, 4.0])
      cr.move_to(hx, pad_top)
      cr.line_to(hx, height - pad_bottom)
      cr.stroke()
      cr.set_dash([])

      cr.set_source_rgba(line_r, line_g, line_b, 0.3)
      cr.arc(hx, hy, 8, 0, 2 * math.pi)
      cr.fill()

      cr.set_source_rgb(line_r, line_g, line_b)
      cr.arc(hx, hy, 4.5, 0, 2 * math.pi)
      cr.fill()

      cr.set_source_rgb(1.0, 1.0, 1.0)
      cr.arc(hx, hy, 2, 0, 2 * math.pi)
      cr.fill()

  chart_area.set_draw_func(draw_chart)

  # Mouse motion controller for hover interaction
  motion_controller = Gtk.EventControllerMotion.new()

  def on_motion(_controller, x, y):
    nonlocal hover_index, history_data
    if not history_data or "points" not in history_data or not history_data["points"]:
      return

    points = history_data["points"]
    n = len(points)
    if n <= 1:
      return

    w = chart_area.get_width()
    pad_left = 20
    pad_right = 20
    chart_w = w - pad_left - pad_right

    if chart_w > 0:
      rel_x = max(0, min(chart_w, x - pad_left))
      idx = min(int(round((rel_x / chart_w) * (n - 1))), n - 1)
      if idx != hover_index:
        hover_index = idx
        update_summary(hover_index)
        chart_area.queue_draw()

  def on_leave(_controller):
    nonlocal hover_index
    if hover_index is not None:
      hover_index = None
      update_summary()
      chart_area.queue_draw()

  motion_controller.connect("motion", on_motion)
  motion_controller.connect("leave", on_leave)
  chart_area.add_controller(motion_controller)

  def select_period(days: int):
    nonlocal current_days
    if current_days == days:
      return
    current_days = days
    for d, btn in period_buttons.items():
      btn.set_active(d == days)
    fetch_history()

  for d, btn in period_buttons.items():
    btn.connect("toggled", lambda b, days=d: select_period(days) if b.get_active() else None)

  def currency_selectors_changed(_obj, _param):
    from_code = from_currency_selector.selected
    to_code = to_currency_selector.selected
    if from_code and to_code and from_code != to_code:
      if settings.get_string("src-currency") != from_code:
        settings.set_string('src-currency', from_code)
      if settings.get_string("dest-currency") != to_code:
        settings.set_string('dest-currency', to_code)
      fetch_history()

  def on_invert_clicked(_button):
    from_code = from_currency_selector.selected
    to_code = to_currency_selector.selected
    if from_code and to_code and from_code != to_code:
      from_currency_selector.set_selected(to_code)
      to_currency_selector.set_selected(from_code)

  def change_provider(settings, key):
    load_currencies(settings.get_enum(key))
    fetch_history()

  load_currencies(settings.get_enum("providers"))
  from_currency_selector.connect('notify::selected', currency_selectors_changed)
  to_currency_selector.connect('notify::selected', currency_selectors_changed)
  invert_currencies.connect('clicked', on_invert_clicked)
  reload_btn.connect('clicked', lambda button: fetch_history(force=True))
  settings.connect("changed::providers", change_provider)
  settings.connect("changed::src-currency", lambda s, k: from_currency_selector.set_selected(s.get_string(k)))
  settings.connect("changed::dest-currency", lambda s, k: to_currency_selector.set_selected(s.get_string(k)))

  fetch_history()
  return page
