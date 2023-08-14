# theme_switcher.py
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


# Code modified from Dialect
#https://github.com/dialect-app/dialect/blob/c8bc7720fc8ef020eac4ec5e37c303a3624c15ee/dialect/widgets/theme_switcher.py

from gi.repository import Adw, Gio, GObject, Gtk

from currencyconverter.define import APP_ID

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/components/theme_switcher/theme_switcher.ui')
class ThemeSwitcher(Gtk.Box):
    __gtype_name__ = 'ThemeSwitcher'

    # Properties
    show_system = GObject.property(type=bool, default=True)
    color_scheme = 'light'

    # Child widgets
    system = Gtk.Template.Child()
    light = Gtk.Template.Child()
    dark = Gtk.Template.Child()

    @GObject.Property(type=str)
    def selected_color_scheme(self):
        """Read-write integer property."""
        return self.color_scheme

    @selected_color_scheme.setter
    def selected_color_scheme(self, color_scheme):
        self.color_scheme = color_scheme

        if color_scheme == 'auto':
            self.system.props.active = True
            self.style_manager.props.color_scheme = Adw.ColorScheme.PREFER_LIGHT
        if color_scheme == 'light':
            self.light.props.active = True
            self.style_manager.props.color_scheme = Adw.ColorScheme.FORCE_LIGHT
        if color_scheme == 'dark':
            self.dark.props.active = True
            self.style_manager.props.color_scheme = Adw.ColorScheme.FORCE_DARK

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.style_manager = Adw.StyleManager.get_default()
        self.settings = Gio.Settings.new(APP_ID)
        self.color_scheme = self.settings.get_string('color-scheme')

        self.settings.bind(
            'color-scheme',
            self,
            'selected_color_scheme',
            Gio.SettingsBindFlags.DEFAULT
        )
        self.style_manager.bind_property(
            'system-supports-color-schemes',
            self, 'show_system',
            GObject.BindingFlags.SYNC_CREATE
        )

    @Gtk.Template.Callback()
    def _on_color_scheme_changed(self, _widget, _paramspec):
        """ Called on (self.system, self.light, self.dark)::notify::active signal """
        if self.system.props.active:
            self.selected_color_scheme = 'auto'
        if self.light.props.active:
            self.selected_color_scheme = 'light'
        if self.dark.props.active:
            self.selected_color_scheme = 'dark'
