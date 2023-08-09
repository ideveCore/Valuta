# window.py
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

from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio

from .components import CurrencySelector
from .components import CurrencyConverterShortcutsWindow
from currencyconverter.api import Api, CurrenciesListModel
from currencyconverter.define import APP_ID, CODES

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/window.ui')
class CurrencyConverterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CurrencyConverterWindow'

    src_currency_selector: CurrencySelector = Gtk.Template.Child()
    dest_currency_selector: CurrencySelector = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    from_value = Gtk.Template.Child()
    to_value = Gtk.Template.Child()
    info = Gtk.Template.Child()
    disclaimer = Gtk.Template.Child()
    src_currencies = []
    dest_currencies = []

    def __init__(self, src_currency_value, **kwargs):
        super().__init__(**kwargs)
        self.set_help_overlay(CurrencyConverterShortcutsWindow())
        self.currency_data = {
            "from_value": 1,
            "to_value": None,
            "currency_value": None,
        }
        self.launch_src_currency_value = src_currency_value
        self.src_currency_model = CurrenciesListModel(self._currency_names_func)
        self.dest_currency_model = CurrenciesListModel(self._currency_names_func)
        self.src_currency_selector.bind_models(self.src_currency_model)
        self.dest_currency_selector.bind_models(self.dest_currency_model)
        self.src_currency_model.set_currencies(CODES)
        self.dest_currency_model.set_currencies(CODES)
        self.src_currency = None
        self.dest_currency = None
        self.connect('unrealize', self.save_settings)
        self.load_settings(APP_ID)
        self.load_data()
        finish_callback = lambda self, task, nothing: self.finish_callback()
        task = Gio.Task.new(self, None, finish_callback, None)
        task.run_in_thread(self._thread_cb)

    def load_data(self):
        self.from_value.set_text(str(self.currency_data["from_value"]))
        if self.currency_data["to_value"]:
            value = float(self.currency_data["to_value"]) * float(self.currency_data["from_value"])
            self.to_value.set_text(str(str("{:,}".format(value))))
            self.info.set_text(self.currency_data["currency_value"]["info"])
            self.disclaimer.set_uri(self.currency_data["currency_value"]["disclaimer"])

    def finish_callback(self):
        self.stack.set_visible_child_name("result")
        if self.currency_data["currency_value"]:
            self.currency_data["to_value"] = self.currency_data["currency_value"]["value"]
            self.load_data()
            if self.is_float(self.launch_src_currency_value):
                self.calculate(self.launch_src_currency_value)

    @staticmethod
    def _thread_cb (task: Gio.Task, self, task_data: object, cancellable: Gio.Cancellable):
        try:
            self.currency_data["currency_value"] = Api().request(self.src_currency, self.dest_currency)
            task.return_value(self.currency_dataa)
        except Exception as e:
            task.return_value(e)

    def load_settings(self, id):
        self.settings = Gio.Settings.new(id);
        self.src_currency = self.settings.get_string('src-currency')
        self.dest_currency = self.settings.get_string('dest-currency')
        if self.src_currency is not None:
            self.src_currency_selector.set_selected(self.src_currency)
            self.dest_currency_selector.set_selected(self.dest_currency)

    def _currency_names_func(self, code):
        return CODES[code]

    def save_settings(self, *args, **kwargs):
        self.settings.set_string('src-currency', self.src_currency)
        self.settings.set_string('dest-currency', self.dest_currency)

    @Gtk.Template.Callback()
    def _on_src_currency_changed(self, _obj, _param):
        code = self.src_currency_selector.selected
        if code != self.src_currency:
            self.src_currency = code
            if self.src_currency != self.dest_currency:
                self.stack.set_visible_child_name("loading")
                finish_callback = lambda self, task, nothing: self.finish_callback()
                task = Gio.Task.new(self, None, finish_callback, None)
                task.run_in_thread(self._thread_cb)
        self.save_settings()
    
    @Gtk.Template.Callback()
    def _on_dest_currency_changed(self, _obj, _param):
        code = self.dest_currency_selector.selected
        if code != self.dest_currency:
            self.dest_currency = code
            self.stack.set_visible_child_name("loading")
            finish_callback = lambda self, task, nothing: self.finish_callback()
            task = Gio.Task.new(self, None, finish_callback, None)
            task.run_in_thread(self._thread_cb)
        self.save_settings()

    @Gtk.Template.Callback()
    def _on_from_value_changed(self, _entry):
        entry_text = _entry.get_text()
        self._calculate(entry_text)

    def _calculate(self, value):
        if self.is_float(value) and self.is_float(self.currency_data["to_value"]):
            from_value = float(value)
            self.currency_data["from_value"] = from_value
            if not self.currency_data["to_value"] == None:
                from_value = float(self.currency_data["to_value"]) * float(self.currency_data["from_value"])
            else:
                from_value = self.currency_data["to_value"]

            if self.from_value.get_text() != value:
                self.from_value.set_text(value)
            self.to_value.set_text(str("{:,}".format(from_value)))


    def is_float(self, v):
        if not v:
            return False
        try:
            f=float(v)
            return True
        except ValueError:
            return False

    @Gtk.Template.Callback()
    def _invert_currencies(self, _button):
        src = self.src_currency
        dest = self.dest_currency
        self.src_currency_selector.set_selected(dest)
        self.dest_currency_selector.set_selected(src)

