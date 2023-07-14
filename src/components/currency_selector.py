# currency_selector.py
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



import re
from gi.repository import Adw, Gdk, Gtk, GObject

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/ui/components/currency_selector.ui')
class CurrencySelector(Adw.Bin):
    __gtype_name__ = 'CurrencySelector'
    __gsignals__ = {
        'user-selection-changed': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, ())
    }

    selected = GObject.Property(type=str)
    insight = Gtk.Template.Child()
    button = Gtk.Template.Child()
    label = Gtk.Template.Child()
    popover = Gtk.Template.Child()
    search = Gtk.Template.Child()
    scroll = Gtk.Template.Child()
    currency_list = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = None
        self.search.set_key_capture_widget(self.popover)
        key_events = Gtk.EventControllerKey.new()
        key_events.connect('key-pressed', self.on_key_pressed)
        self.search.add_controller(key_events)

    def bind_models(self, currencies):
        self.model = currencies
        self.filter = Gtk.CustomFilter()
        self.filter.set_filter_func(self.filter_currencies)
        sorter = Gtk.CustomSorter.new(self.sort_currencies)
        sorted_model = Gtk.SortListModel.new(model=self.model, sorter=sorter)
        filter_model = Gtk.FilterListModel.new(sorted_model, self.filter)
        self.currency_list.bind_model(filter_model, self.create_currency_row)

    def set_insight(self, code):
        if self.selected == 'auto':
            self.insight.props.label = f'({self._get_currency_name(code)})'

    def _get_currency_name(self, code):
        return self.model.names_func(code)

    @Gtk.Template.Callback()
    def _on_selected_changed(self, _self, _pspec):
        if self.model is not None:
            self.model.set_selected(self.selected)
            self.label.props.label = self._get_currency_name(self.selected)
            self.insight.props.label = ''

    def set_selected(self, code):
        if self.model is not None:
            self.selected = code
            self.model.set_selected(self.selected)
            self.label.props.label = self._get_currency_name(self.selected)
            self.insight.props.label = ''


    @Gtk.Template.Callback()
    def _activated(self, _list, row):
        self.popover.popdown()
        self.selected = row.currency.code
        self.emit('user-selection-changed')

    @Gtk.Template.Callback()
    def _popover_show(self, _popover):
        self.search.grab_focus()

    @Gtk.Template.Callback()
    def _popover_closed(self, _popover):
        vscroll = self.scroll.get_vadjustment()
        vscroll.props.value = 0
        self.search.props.text = ''
  
    def filter_currencies(self, item):
        search = self.search.get_text()
        return bool(re.search(search, item.name, re.IGNORECASE))

    def sort_currencies(self, currency_a, currency_b, _data):
        a = currency_a.name.lower()
        b = currency_b.name.lower()
        return (a > b) - (a < b)

    def create_currency_row(self, currency):
        return CurrencyRow(currency)

    @Gtk.Template.Callback()
    def _on_search(self, _entry):
        self.filter.emit('changed', Gtk.FilterChange.DIFFERENT)

    @Gtk.Template.Callback()
    def _on_search_activate(self, _entry):
        if self.search.props.text:
            row = self.currency_list.get_row_at_index(0)
            if row:
                self.currency_list.emit('row-activated', row)
        return Gdk.EVENT_PROPAGATE

    def on_key_pressed(self,_controller, keyval, _keycode, _mod):
        if keyval == Gdk.KEY_Escape:
            self.popover.popdown()
        elif keyval == Gdk.KEY_Down:
            return Gdk.EVENT_STOP

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/ui/components/currency_row.ui')
class CurrencyRow(Gtk.ListBoxRow):
    __gtype_name__ = 'CurrencyRow'

    name = Gtk.Template.Child()
    selection = Gtk.Template.Child()
    
    def __init__(self, currency):
        super().__init__()
        self.currency = currency
        self.name.props.label = self.currency.name

        self.currency.bind_property(
            'selected',
            self.selection,
            'visible',
            GObject.BindingFlags.SYNC_CREATE
        )

