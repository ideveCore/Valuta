# window.py
#
# Copyright 2023 Francisco Jeferson dos Santos Freires
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
from currencyconverter.components import CurrencySelector
from currencyconverter.api import Api, CurrenciesListModel
from currencyconverter.define import APP_ID

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/ui/window.ui')
class CurrencyconverterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CurrencyconverterWindow'

    src_currency_selector: CurrencySelector = Gtk.Template.Child()
    dest_currency_selector: CurrencySelector = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    from_value = Gtk.Template.Child()
    to_value = Gtk.Template.Child()
    info = Gtk.Template.Child()
    disclaimer = Gtk.Template.Child()
    src_currencies = []
    dest_currencies = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.currency_data = {
            "from_value": 1,
            "to_value": None,
            "currency_value": None,
        }
        self.src_currency_model = CurrenciesListModel(self._currency_names_func)
        self.dest_currency_model = CurrenciesListModel(self._currency_names_func)
        self.src_currency_selector.bind_models(self.src_currency_model)
        self.dest_currency_selector.bind_models(self.dest_currency_model)
        self.src_currency_model.set_langs(Api().codes)
        self.dest_currency_model.set_langs(Api().codes)
        self.connect('unrealize', self.save_settings)
        self.src_currencies = self.src_currency_model
        self.load_settings(APP_ID)
        if self.src_currencies is not None:
            self.src_currency_selector.set_selected(self.src_currencies)
            self.dest_currency_selector.set_selected(self.dest_currencies)

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

    @staticmethod
    def _thread_cb (task: Gio.Task, self, task_data: object, cancellable: Gio.Cancellable):
        try:
            self.currency_data["currency_value"] = Api().request(self.src_currencies, self.dest_currencies)
            task.return_value(self.currency_dataa)
        except Exception as e:
            task.return_value(e)

    def load_settings(self, id):
        self.settings = Gio.Settings.new(id);
        self.src_currencies = self.settings.get_string('src-currencies')
        self.dest_currencies = self.settings.get_string('dest-currencies')

    def _currency_names_func(self, code):
        return Api().codes[code]

    def save_settings(self, *args, **kwargs):
        self.settings.set_string('src-currencies', self.src_currencies)
        self.settings.set_string('dest-currencies', self.dest_currencies)

    @Gtk.Template.Callback()
    def _on_src_currency_changed(self, _obj, _param):
        code = self.src_currency_selector.selected
        if code != self.src_currencies:
            self.src_currencies = code
            if self.src_currencies == self.dest_currencies:
                self.stack.set_visible_child_name("loading")
                finish_callback = lambda self, task, nothing: self.finish_callback()
                task = Gio.Task.new(self, None, finish_callback, None)
                task.run_in_thread(self._thread_cb)
        
    @Gtk.Template.Callback()
    def _on_dest_currency_changed(self, _obj, _param):
        code = self.dest_currency_selector.selected
        if code != self.dest_currencies:
            self.dest_currencies = code
            self.stack.set_visible_child_name("loading")
            finish_callback = lambda self, task, nothing: self.finish_callback()
            task = Gio.Task.new(self, None, finish_callback, None)
            task.run_in_thread(self._thread_cb)

    @Gtk.Template.Callback()
    def _test(self, _entry):
        entry_text = _entry.get_text()
        if self.is_float(entry_text) and self.is_float(self.currency_data["to_value"]):
            value = float(entry_text)
            self.currency_data["from_value"] = value
            if not self.currency_data["to_value"] == None:
                value = float(self.currency_data["to_value"]) * float(self.currency_data["from_value"])
            else:
                value = self.currency_data["to_value"]

            self.to_value.set_text(str("{:,}".format(value)))

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
        src = self.src_currencies
        dest = self.dest_currencies
        self.src_currency_selector.set_selected(dest)
        self.dest_currency_selector.set_selected(src)

