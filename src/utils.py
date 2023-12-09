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

from __future__ import annotations
from typing import Union, Any, Dict, Callable
import gi, json, logging, re
gi.require_version('Soup', '3.0')
from gi.repository import Adw, Gio, GObject, GLib, Soup
from .define import CODES, BASE_URL, BASE_URL_LANG_PREFIX

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

    def set_currencies(self, currencies, auto=False):
        removed = len(self.currencies)
        self.currencies.clear()
        for code in currencies:
            self.currencies.append(CurrencyObject(code, self.names_func(code)))
            self.items_changed(0, removed, len(self.currencies))

    def set_selected(self, code):
        for item in self.currencies:
            item.props.selected = (item.code == code)

class SoupSession(Soup.Session):
    """
        Currency Converter soup session handler
    """

    instance = None
    _headers = {
        'User-Agent': ' 	Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Referer': 'https://www.google.com',
    }

    _src_currency: str = ''
    _dest_currency: str = ''
    _default_response: Dict[str, Any] = {
        "from"     : _src_currency,
        "to"       : _dest_currency,
        "amount"   : 0,
        "converted": False
    }
    _formated_response: Dict[str, Any] = {
        "dest_currency_value": 0,
        "info": '',
        "disclaimer": '',
    }

    def __init__(self):
        Soup.Session.__init__(self)

    @staticmethod
    def new() -> SoupSession:
        """Create a new instance of Session."""
        session = Soup.Session()
        session.__class__ = SoupSession
        return session

    @staticmethod
    def get() -> SoupSession:
        """Return an active instance of Session."""
        if SoupSession.instance is None:
            SoupSession.instance = SoupSession.new()
        return SoupSession.instance

    @staticmethod
    def format_request(src_currency: str, dest_currency: str) -> SoupSession.create_request:
        SoupSession._src_currency = src_currency
        SoupSession._dest_currency = dest_currency
        return SoupSession.create_request('GET', SoupSession.__mount_url(), SoupSession._headers)

    @staticmethod
    def __mount_url(src_currency_value = 1) -> str:
        url = f'{BASE_URL}+{src_currency_value}+{SoupSession._src_currency}+to+{SoupSession._dest_currency}{BASE_URL_LANG_PREFIX}'
        return url
    
    @staticmethod
    def encode_data(data) -> GLib.Bytes | None:
        """ Convert dict to JSON and bytes """
        data_glib_bytes = None
        try:
            data_bytes = json.dumps(data).encode('utf-8')
            data_glib_bytes = GLib.Bytes.new(data_bytes)
        except Exception as exc:
            logging.warning(exc)
        return data_glib_bytes

    @staticmethod
    def create_request(method: str, url: str, headers: dict = {}) -> Soup.Message:
        """ Helper for creating Soup.Message """

        message = Soup.Message.new(method, url)
        if headers:
            for name, value in headers.items():
                message.get_request_headers().append(name, value)
        if 'User-Agent' not in headers:
            message.get_request_headers().append('User-Agent', 'Currency Converter')
        return message

    def get_response(self, message: Soup.Message) -> Union[Soup._formated_response, Any]:
        response = None
        try:
            response = self.send_and_read(message, None)
            data = response.get_data()
            return self.get_currency_value(data)
        except GLib.GError as exc:
            return exc.message

    def get_raw_value(self, message: Soup.Message) -> Union[Soup._formated_response, Any]:
        response = None
        try:
            response = self.send_and_read(message, None)
            data = response.get_data()
            return self.get_currency_raw_value(data)
        except GLib.GError as exc:
            return exc.message


    @staticmethod
    def get_currency_value(data):
        data = data.decode('utf-8')
        try:
            results = re.findall(f'[\d*\,]*\.\d* {CODES[SoupSession._dest_currency]["name"]}', data)
            if results.__len__() > 0:
                converted_amount_str = results[0]
                converted_currency = re.findall('[\d*\,]*\.\d*', converted_amount_str)[0]
                SoupSession._default_response["amount"]    = converted_currency
                SoupSession._default_response["converted"] = True
                return SoupSession.format_response(SoupSession._default_response)
            else:
                raise Exception(gettext("Unable to convert currency, failed to fetch results from Google"))
        except Exception as error:
            return SoupSession._default_response

    @staticmethod
    def get_currency_raw_value(data):
        data = data.decode('utf-8')
        try:
            results = re.findall(f'[\d*\,]*\.\d* {CODES[SoupSession._dest_currency]["name"]}', data)
            if results.__len__() > 0:
                converted_amount_str = results[0]
                converted_currency = re.findall('[\d*\,]*\.\d*', converted_amount_str)[0]
                return converted_currency
            else:
                raise Exception(gettext("Unable to convert currency, failed to fetch results from Google"))
        except Exception as error:
            return SoupSession._default_response

    @staticmethod
    def format_response(default_response: Dict[str, Any]) -> Dict[str, Any]:
        url = SoupSession.__mount_url(default_response['amount'])
        current_date = GLib.DateTime.new_now_local()
        date = f'{current_date.get_day_of_month()} {gettext("of")} {current_date.format("%B")}'
        time = current_date.format("%H:%M:%S")
        SoupSession._formated_response['dest_currency_value'] = default_response['amount']
        SoupSession._formated_response['info'] = f'{date} - {time}'
        SoupSession._formated_response['disclaimer'] = url

        return SoupSession._formated_response

class Settings(Gio.Settings):
    def __init__(self, *args):
        super().__init__(*args)


def settings(application: Adw.Application):
    gsettings = Gio.Settings(
        schema_id= application.get_application_id(),
    )

    bind: Callable[[str, GObject.Object, str, Gio.SettingsBindFlags], Dict[any, any]] = lambda key, object, property, flags: gsettings.bind(key, object, property, flags)

    return {
        "bind": bind,
    }


def utils(application: Adw.Application) -> Dict[any, any]:
    settings_instance = Settings(application.get_application_id())

    return {
        'settings': settings_instance,
    }
