# utils.py
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

from typing import Any, Dict, Union, Callable
from gi.repository import Adw, Gio, GObject, GLib
from babel.numbers import format_number, parse_decimal
from .requests import Requests
from .define import CODES

class CurrencyObject(GObject.Object):
    __gtype_name__ = 'CurrencyObject'

    code = GObject.Property(type=str)
    name = GObject.Property(type=str)
    selected = GObject.Property(type=bool, default=False)

    def __init__(self, code, name, selected=False):
        super().__init__()
        self.code = code
        self.name = name
        self.selected = selected

    def __str__(self):
        return self.code

class CurrenciesListModel(GObject.GObject, Gio.ListModel):
    __gtype_name__ = 'CurrenciesListModel'

    def __init__(self, names_func):
        super().__init__()

        self.names_func = names_func
        self.currencies = []

    def __iter__(self):
        return iter(self.currencies)

    def do_get_item(self, position):
        return self.currencies[position]

    def do_get_item_type(self):
        return CurrencyObject

    def do_get_n_items(self):
        return len(self.currencies)

    def set_currencies(self, currencies):
        removed = len(self.currencies)
        self.currencies.clear()
        for code in currencies:
            self.currencies.append(CurrencyObject(code, self.names_func(code)))
        self.items_changed(0, removed, len(self.currencies))

    def set_selected(self, code):
        for item in self.currencies:
            item.props.selected = (item.code == code)

class Convertion:
    def __init__(self, settings: Gio.Settings):
        self.converted_data: Dict[str, Union[str, int]] = {
            "base": 1,
            "from": "",
            "to": "",
            "amount": 1,
            "info": "",
            "disclaimer": "",
            "provider": settings.get_enum("providers"),
            "converted": False,
        }
        self.__events = {
            "converted": [],
        }
        self.settings = settings
    def convert(self, from_currency_value: int, from_currency: str, to_currency: str, provider: int) -> Dict[str, Union[str, int]]:
        if not from_currency == to_currency:
            if not self.match_data(from_currency, to_currency, provider) or not self.converted_data["converted"]:
                try:
                  response = Requests(provider, from_currency, to_currency, 1).get()
                  if isinstance(response, str):
                      self.converted_data["converted"] = False
                      return self.__event('converted', self.converted_data)
                  self.converted_data = response
                  self.converted_data["converted"] = True

                  from_currency = from_currency_value
                  base_currency = self.converted_data["base"]

                  self.converted_data = {**self.converted_data, "amount": from_currency * base_currency}
                  self.__event('converted', self.converted_data)
                  return self.converted_data
                except Exception as error:
                  self.converted_data["converted"] = False
                  self.converted_data = {**self.converted_data, "amount": 0}
                  self.__event('converted', self.converted_data)
                  return self.converted_data
            else:
              self.converted_data = {**self.converted_data, "amount": from_currency_value * self.converted_data["base"]}
              self.__event('converted', self.converted_data)
        else:
            self.converted_data["converted"] = False

    def convert_raw(self, from_currency_value: int, from_currency: str, to_currency: str, provider: int) -> int:
        if not from_currency == to_currency:
            response = Requests(provider, from_currency, to_currency, 1).get()
            if not isinstance(response, str):
                return response["base"]
            else:
                self.converted_data["converted"] = False
        else:
            self.converted_data["converted"] = False

    def match_data(self, from_currency: str, to_currency: str, provider: int) -> bool:
        if self.converted_data["from"] != from_currency:
            return False
        if self.converted_data["to"] != to_currency:
            return False
        if self.converted_data["provider"] != provider:
            return False
        else:
            return True

    def connect(self, event: str, callback: Callable):
        self.__events[event].append(callback)

    def get_convertion(self) -> Dict[str, Union[str, int]]:
        return self.converted_data

    def __event(self, event: str, data: Dict[str, Union[str, int]]):
        for listener in self.__events[event]:
            listener(data)


class Settings(Gio.Settings):
    def __init__(self, *args):
        super().__init__(*args)

class Utils:
    def __init__(self, application_id):
        self.settings = Settings(application_id)
        self.convertion = Convertion(self.settings)
        self.locale = GLib.get_locale_variants(GLib.get_language_names()[0])
        self.currencies = CODES
        self.providers = {
          "0": "ECB"
        }
    def format_number(self, number):
        try:
            if number:
                return format_number(number, locale=self.locale[1])
            else:
                return False
        except:
            return False
    def parse_number(self, number):
        try:
            if number:
                return parse_decimal(number, locale=self.locale[1])
            else:
                return False
        except:
            return False
