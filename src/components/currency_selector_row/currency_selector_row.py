# currency_selector_row.py
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

import textwrap
from gi.repository import Gio, GObject, Gtk

@Gtk.Template(resource_path='/io/github/idevecore/Valuta/components/currency_selector_row/index.ui')
class CurrencySelectorRow(Gtk.ListBoxRow):
  __gtype_name__ = 'CurrencySelectorRow'

  name = Gtk.Template.Child()
  selection = Gtk.Template.Child()
  favorite_button = Gtk.Template.Child()

  def __init__(self, currency):
    super().__init__()
    self.currency = currency
    self.name.props.label = f'{self.currency} – {textwrap.shorten(self.currency.name, width=30, placeholder="...")}'

    self.currency.bind_property(
      'selected',
      self.selection,
      'visible',
      GObject.BindingFlags.SYNC_CREATE
    )

    self.currency.connect('notify::is-favorite', self._update_favorite_icon)
    self._update_favorite_icon()

  def _update_favorite_icon(self, *_args):
    if self.currency.is_favorite:
      self.favorite_button.set_icon_name('star-large-symbolic')
    else:
      self.favorite_button.set_icon_name('star-outline-rounded-symbolic')

  @Gtk.Template.Callback()
  def on_favorite_currency(self, _button):
    app = Gio.Application.get_default()
    if not app or not hasattr(app, 'utils'):
      return

    settings = app.utils.settings
    favorites = list(settings.get_strv('favorite-currencies'))
    code = self.currency.code

    if code in favorites:
      favorites.remove(code)
      self.currency.is_favorite = False
    else:
      favorites.append(code)
      self.currency.is_favorite = True

    settings.set_strv('favorite-currencies', favorites)
