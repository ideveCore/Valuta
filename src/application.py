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
from .utils import Utils
from .window import create_main_window
from .actions import application_actions

from .define import APP_ID, VERSION, RES_PATH

class Application(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        Adw.ApplicationWindow.__init__(
                self,
                application_id=APP_ID,
                resource_base_path=RES_PATH,
                flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
            )
        self.utils = Utils(APP_ID)
        application_actions(application=self)
        self.from_currency_value = 0
        self.add_main_option('src-currency-value', b't', GLib.OptionFlags.NONE,
                             GLib.OptionArg.STRING, 'Value to convert currencies', None)

    def do_activate(self):
        if self.get_active_window() is not None:
            self.get_active_window().present()
        else:
            create_main_window(self, self.from_currency_value).present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        src_currency_value = ''
        if 'src-currency-value' in options:
            src_currency_value = options['src-currency-value']
        if self.get_active_window() is not None:
            self.get_active_window().load_convertion_page(src_currency_value)
        else:
            self.from_currency_value = src_currency_value

        self.activate()
        return 0
