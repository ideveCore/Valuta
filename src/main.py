# main.py
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

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib, Gio, Adw
from currencyconverter.window import CurrencyconverterWindow
from currencyconverter.components import CurrencyConverterPreferences
from currencyconverter.define import APP_ID, VERSION

class CurrencyconverterApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        Adw.ApplicationWindow.__init__(
                self,
                application_id=APP_ID,
                flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE
            )
        self.set_resource_base_path('/io/github/idevecore/CurrencyConverter')
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.settings = Gio.Settings.new(APP_ID);
        self.window = None
        self.launch_value = ''
        self.add_main_option('value', b't', GLib.OptionFlags.NONE,
                             GLib.OptionArg.STRING, 'Value to converte currencies', None)
        self.load_theme()


    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        self.window = self.props.active_window

        if not self.window:
            self.window = CurrencyconverterWindow(
                application=self,
                title=_('Currency Converter'),
                value=self.launch_value,
            )

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        value = ''

        if 'value' in options:
            value = options['value']

        if self.window is not None:
            self.window.load_settings(APP_ID)
            self.window.calculate(value)
        else:
            self.launch_value = value

        self.activate()
        return 0

    def do_startup(self):
        Adw.Application.do_startup(self)

    def on_about_action(self, widget, _):
        print(VERSION)
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='Currency Converter',
                                application_icon=APP_ID,
                                developer_name='Ideve Core',
                                version=VERSION,
                                developers=['Ideve Core'],
                                copyright='© 2023 Ideve Core')
        about.present()

    def on_preferences_action(self, widget, _):
        CurrencyConverterPreferences().present()

    def load_theme(self):
        style_manager = Adw.StyleManager.get_default()
        if self.settings.get_string('theme') == 'default':
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        elif self.settings.get_string('theme') == 'dark':
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)



    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = CurrencyconverterApplication()
    return app.run(sys.argv)
