# about.py
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

import gi

gi.require_version('Adw', '1')

from gi.repository import Adw, Gio, GLib, Gtk, GObject
from .define import APP_ID, VERSION

def about(application: Adw.Application):
    def get_flatpak_info():
        key_file = GLib.KeyFile.new();
        try:
            key_file.load_from_file("/.flatpak-info", GLib.KeyFileFlags.NONE);
        except Exception as error:
            return None;
        return key_file.get_value("Instance", "flatpak-version");

    app_info = f'{APP_ID} {VERSION}'
    glib_os_info = f'{GLib.get_os_info("ID")} {GLib.get_os_info("VERSION_ID")}'
    pygobject_info = f'PyGObject {".".join(map(str, GObject.pygobject_version))}'
    adw_info = f'Adw {Adw.MAJOR_VERSION}'
    gtk_info = f'Gtk {Gtk.get_major_version()}'
    glib_info = f'GLib {".".join(map(str, GLib.glib_version))}'
    flatpak_info = f'Flatpak {get_flatpak_info()}'
    blueprint_info = 'Blueprint 0.10.0'

    debug_info = f'{app_info}\n{glib_os_info}\n{pygobject_info}\n{adw_info}\n{gtk_info}\n{glib_info}\n{flatpak_info}\n{blueprint_info}'

    """Callback for the app.about action."""

    return Adw.AboutDialog(
        application_name=gettext('Valuta'),
        application_icon=APP_ID,
        developer_name='Ideve Core',
        version=VERSION,
        developers=['Ideve Core'],
        designers=['Brage Fuglseth https://bragefuglseth.dev'],
        issue_url='https://github.com/ideveCore/valuta/issues',
        debug_info=debug_info,
        license_type=Gtk.License.GPL_3_0,
        copyright='© 2023 Ideve Core'
    )
