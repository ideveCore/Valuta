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

from gi.repository import Adw, Gtk, Gio
from currencyconverter.define import RES_PATH

resource = f'{RES_PATH}/components/preferences/index.ui'

def preferences(application: Adw.Application, settings: Gio.Settings):
    builder = Gtk.Builder.new_from_resource(resource)
    component = builder.get_object('component')
    providers = builder.get_object('providers')
    component.set_transient_for(application.get_active_window())

    settings.bind(
        key="providers",
        object=providers,
        property="selected",
        flags=Gio.SettingsBindFlags.DEFAULT,
    )

    #providers.connect('notify::selected-item', lambda user_data : print('change'))

    return component
