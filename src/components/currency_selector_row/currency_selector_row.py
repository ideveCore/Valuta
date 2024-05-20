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

from gi.repository import GObject, Gtk
from ...define import CODES

@Gtk.Template(resource_path='/io/github/idevecore/Valuta/components/currency_selector_row/index.ui')
class CurrencySelectorRow(Gtk.ListBoxRow):
    __gtype_name__ = 'CurrencySelectorRow'

    name = Gtk.Template.Child()
    selection = Gtk.Template.Child()
    
    def __init__(self, currency):
        super().__init__()
        self.currency = currency
        #self.name.props.label = f'{CODES[str(self.currency)]["flag"]}   {self.currency} – {self.currency.name}'
        self.name.props.label = f'{self.currency} – {self.currency.name}'

        self.currency.bind_property(
            'selected',
            self.selection,
            'visible',
            GObject.BindingFlags.SYNC_CREATE
        )


