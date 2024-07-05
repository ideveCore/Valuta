# actions.py
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
from gi.repository import Gio, Adw
from .about import about

def application_actions(application: Adw.Application):
  quit_action = Gio.SimpleAction.new(name='quit')
  about_action = Gio.SimpleAction.new(name='about')
  switch_currencies = Gio.SimpleAction.new(name="switch_currencies")

  def invert_currencies():
    from_code = application.utils.settings.get_string('src-currency')
    to_code = application.utils.settings.get_string('dest-currency')
    application.utils.settings.set_string('src-currency', to_code)
    application.utils.settings.set_string('dest-currency', from_code)

  quit_action.connect('activate', lambda simple_action, parameter: application.quit())
  about_action.connect('activate', lambda simple_action, parameter : about(application).present(application.get_active_window()))
  switch_currencies.connect('activate', lambda simple_action, parameter : invert_currencies())

  application.add_action(quit_action)
  application.add_action(about_action)
  application.add_action(switch_currencies)
  application.set_accels_for_action('app.quit', ['<primary>q'])
  application.set_accels_for_action('app.quit', ['<primary>w'])
  application.set_accels_for_action('app.switch_currencies', ['<primary>s'])
  application.set_accels_for_action('win.show-help-overlay', ['<Primary>question'])
