# application.py
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
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gio, GLib, Gtk
from .utils import utils
from .window import create_main_window

# from .components import CurrencyConverterPreferences
from .define import APP_ID, VERSION, RES_PATH

application = Adw.Application(
    application_id=APP_ID,
    resource_base_path=RES_PATH,
    flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
)


def startup(application: Adw.Application):
    application.utils = utils(application)


def load_main_window(application: Adw.Application):
    create_main_window(application).present()


application.connect("startup", startup)
application.connect("activate", load_main_window)
