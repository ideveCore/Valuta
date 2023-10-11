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

from gi.repository import Adw, Gio, Gtk
import re
from .components import CurrencySelector
from .components import CurrencyConverterShortcutsWindow, ThemeSwitcher
from .utils import CurrenciesListModel, SoupSession
from .define import APP_ID, CODES

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/window.ui')
class CurrencyConverterWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'CurrencyConverterWindow'

    src_currency_selector: CurrencySelector = Gtk.Template.Child()
    dest_currency_selector: CurrencySelector = Gtk.Template.Child()
    dest_currency_label = Gtk.Template.Child()
    src_currency_entry = Gtk.Template.Child()
    convert_button = Gtk.Template.Child()
    convert_button_spinner = Gtk.Template.Child()
    disclaimer = Gtk.Template.Child()
    info = Gtk.Template.Child()
    menu_btn = Gtk.Template.Child()
    overlay = Gtk.Template.Child()
    src_currencies = []
    dest_currencies = []

    def __init__(self, src_currency_value, **kwargs):
        super().__init__(**kwargs)
        theme_switcher = ThemeSwitcher()
        self.menu_btn.props.popover.add_child(theme_switcher, 'theme')
        self.set_help_overlay(CurrencyConverterShortcutsWindow())
        self.is_loading = True
        self.currency_data = {
            "src_currency_value": 1,
            "dest_currency_value": None,
            "src_currency": None,
            "dest_currency": None,
            "info": None,
            "disclaimer": None,
            "convertion_value": None,
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
        self.load_settings(APP_ID)
        self.connect('unrealize', self.save_settings)
        self.convert_button.connect('clicked', lambda button: self._convert_currencies())
        self.src_currency_entry.connect('entry-activated', lambda entry: self._convert_currencies())
        self.src_currency_selector.connect('notify::selected', self.on_currency_selectors_changed)
        self.dest_currency_selector.connect('notify::selected', self.on_currency_selectors_changed)
        task = Gio.Task.new(self, None, self.finish_callback, None)
        task.run_in_thread(self._thread_cb)

        if self.launch_src_currency_value:
            self.src_currency_entry.set_text(self.launch_src_currency_value)
        action_try_again = Gio.SimpleAction.new(
            name = "try_again",
        )
        
        action_try_again.connect('activate', self.try_again_get_data)
        self.add_action(action_try_again)

    def try_again_get_data(self, _target, _data):
        self.convert_button.set_sensitive(False)
        spinner = Gtk.Spinner.new()
        self.convert_button.set_child(spinner)
        spinner.set_spinning(True)
        task = Gio.Task.new(self, None, self.finish_callback, None)
        task.run_in_thread(self._thread_cb)


    def load_data(self):
        self.src_currency_entry.set_title(self.src_currency)
        src_value = self.src_currency_entry.get_text()
        self.src_currency_entry.set_text('1' if  src_value == '' else src_value)
        self.dest_currency_label.set_text(CODES[self.dest_currency]["symbol"])
        if self.currency_data['convertion_value']:
            formatted_value = str("{:,}".format(self.currency_data['convertion_value']))
            self.dest_currency_label.set_text(f'{CODES[self.dest_currency]["symbol"]} {formatted_value}')
            self.info.set_text(self.currency_data['info'])
            self.disclaimer.set_uri(self.currency_data['disclaimer'])

    def finish_callback(self, task, nothing, data):
        self.is_loading = False
        self.convert_button.set_sensitive(True)
        self.convert_button.set_label(gettext('Convert'))

        if self.currency_data['dest_currency_value']:
            self._convert_currencies()
        else:
            toast = Adw.Toast.new(
                title = gettext('Error when get currencies data'),
            )
            toast.props.button_label = gettext('Try again')
            toast.props.priority = Adw.ToastPriority.HIGH
            toast.set_action_name('win.try_again')
            self.overlay.add_toast(toast);
    
    @staticmethod
    def _thread_cb (task: Gio.Task, self, task_data: object, cancellable: Gio.Cancellable):
        try:
            self.is_loading = True
            session = SoupSession.get()
            message = session.format_request(self.src_currency, self.dest_currency)
            response_data = session.get_response(message)
            self.currency_data['dest_currency_value'] = response_data['dest_currency_value']
            self.currency_data['info'] = response_data['info']
            self.currency_data['disclaimer'] = response_data['disclaimer']
            self.currency_data['src_currency'] = self.src_currency
            self.currency_data['dest_currency'] = self.dest_currency

            task.return_value(self.currency_data)
        except Exception as e:
            self.is_loading = False
            task.return_value(e)

    def load_settings(self, id):
        self.settings = Gio.Settings.new(id);
        self.src_currency = self.settings.get_string('src-currency')
        self.dest_currency = self.settings.get_string('dest-currency')
        if self.src_currency is not None:
            self.src_currency_selector.set_selected(self.src_currency)
            self.dest_currency_selector.set_selected(self.dest_currency)
        self.load_data()

    def _currency_names_func(self, code):
        name = gettext(CODES.get(code, '')['name'])
        return name if name else None

    def save_settings(self, *args, **kwargs):
        self.settings.set_string('src-currency', self.src_currency)
        self.settings.set_string('dest-currency', self.dest_currency)

    def on_currency_selectors_changed(self, _obj, _param):
        src_code = self.src_currency_selector.selected
        dest_code = self.dest_currency_selector.selected
        self.src_currency = src_code
        self.dest_currency = dest_code
        self.save_settings()
        self.load_data()
        self.convert_button.set_sensitive(False)
        spinner = Gtk.Spinner.new()
        self.convert_button.set_child(spinner)
        spinner.set_spinning(True)
        task = Gio.Task.new(self, None, self.finish_callback, None)
        task.run_in_thread(self._thread_cb)

    def _convert_currencies(self):
        if not self.is_loading:
            if self.src_currency == self.currency_data['src_currency'] and self.dest_currency == self.currency_data['dest_currency']:
                src_value = re.sub(r'[^\d.]', '', self.src_currency_entry.get_text())
                if self.is_number(src_value) and self.is_number(self.currency_data['dest_currency_value']):
                    self.currency_data['src_currency_value'] = float(src_value)
                    convertion_value = float(self.currency_data["src_currency_value"]) * float(self.currency_data["dest_currency_value"])
                    self.currency_data['convertion_value'] = convertion_value
                    self.load_data()
            else:
                self.convert_button.set_sensitive(False)
                spinner = Gtk.Spinner.new()
                self.convert_button.set_child(spinner)
                spinner.set_spinning(True)
                task = Gio.Task.new(self, None, self.finish_callback, None)
                task.run_in_thread(self._thread_cb)

    def is_number(self, v):
        if not v:
            return False
        try:
            f=float(v)
            return True
        except ValueError:
            return False

    @Gtk.Template.Callback()
    def _switch_currencies(self, _button):
        self.src_currency_selector.handler_block_by_func(self.on_currency_selectors_changed)
        src_currency = self.src_currency
        dest_currency = self.dest_currency
        self.src_currency = dest_currency
        self.dest_currency = src_currency
        self.save_settings()
        self.load_settings(APP_ID)
        self.src_currency_selector.handler_unblock_by_func(self.on_currency_selectors_changed)
