# requests.py
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

from typing import Any, Dict, Union
from datetime import datetime
import gi, json, re
gi.require_version('Soup', '3.0')
from gi.repository import Soup, GLib
from .define import BASE_URL_LANG_PREFIX, CODES

class Providers:
    GOOGLE_BASE_URL: str = 'https://www.google.com/search?q=convert'
    ECB_BASE_URL: str = 'https://api.frankfurter.app/latest'
    MI_BASE_URL: str = 'https://cdn.moeda.info/api/latest.json'
    response = {
        "from": "",
        "to": "",
        "amount": "",
        "converted": False,
        "info": "",
        "disclaimer": "",
        "provider": "",
    }

    def __init__(self, from_currency: str, to_currency: str, from_currency_value: int):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.from_currency_value = from_currency_value

    def mount_url(self):
        pass

    def serializer(self):
        pass

    def default_response(self):
        pass

    def create_info(self, date: str, time: str = "00:00:00"):
        date = date.split("-")
        time = time.split(":")
        date_time = GLib.DateTime.new_utc(float(date[0]), float(date[1]), float(date[2]), float(time[0]), float(time[1]), float(time[2]))
        return f"{_('Results for')} {date_time.format('%d')} {date_time.format('%B')} {date_time.format('%Y')} {date_time.format('%H:%M')} - UTC"

class ECB(Providers):
    def mount_url(self):
        return f'{self.ECB_BASE_URL}?amount={self.from_currency_value}&from={self.from_currency}&to={self.to_currency}'

    def serializer(self, data: bytes) -> Dict[str, Union[str, int]]:
        return self.default_response(json.loads(data))

    def default_response(self, data: Dict[str, str]):
        self.response["base"] = data["rates"][self.to_currency]
        self.response["from"] = self.from_currency
        self.response["to"] = self.to_currency
        self.response["amount"] = 0
        self.response["info"] = self.create_info(data["date"])
        self.response["disclaimer"] = self.mount_url()
        self.response["provider"] = 0
        return self.response

class Google(Providers):
    def mount_url(self):
        return f'{self.GOOGLE_BASE_URL}+{self.from_currency_value}+{self.from_currency}+to+{self.to_currency}{BASE_URL_LANG_PREFIX}'

    def serializer(self, data: bytes):
        data = data.decode('utf-8', errors="replace")
        try:
            results = re.findall(f'[\d*\,]*\.\d* {CODES[self.to_currency]["name"]}', data)
            if results.__len__() > 0:
                converted_amount_str = results[0]
                converted_currency = re.findall('[\d*\,]*\.\d*', converted_amount_str)[0]
                return self.default_response({
                    "amount": converted_currency,
                    "converted": True,
                })
            else:
                raise Exception(_("Unable to convert currency, failed to fetch results from Google."))
        except Exception as error:
            print(error)
            return self.default_response

    def default_response(self, data: Dict[str, str]):
        url = self.mount_url()
        current_date = GLib.DateTime.new_now_local()
        time = current_date.format("%H:%M:%S")
        self.response["base"] = float(data['amount'])
        self.response["from"] = self.from_currency
        self.response["to"] = self.to_currency
        self.response["amount"] = 0
        self.response['info'] = self.create_info(current_date.format("%F"), time)
        self.response['disclaimer'] = url
        self.response["provider"] = 1
        return self.response

class MI(Providers):
    def mount_url(self):
        return self.MI_BASE_URL

    def serializer(self, data: bytes) -> Dict[str, Union[str, int]]:
        return self.default_response(json.loads(data))

    def default_response(self, data: Dict[str, str]):
        date_time = datetime.fromisoformat(data["lastupdate"])
        self.response["base"] = data["rates"][self.to_currency]/data["rates"][self.from_currency]
        self.response["from"] = self.from_currency
        self.response["to"] = self.to_currency
        self.response["amount"] = 0
        self.response["info"] = self.create_info(f'{date_time.date()}', f'{date_time.time()}')
        self.response["disclaimer"] = self.mount_url()
        self.response["provider"] = 2
        return self.response

providers = {
    0 : ECB,
    1 : Google,
    2 : MI,
}

class SoupSession(Soup.Session):
    def __init__(self):
        Soup.Session.__init__(self)

    def create_request(self, method: str, url: str, headers: dict = {}) -> Soup.Message:
        """ Helper for creating Soup.Message """
        message = Soup.Message.new(method, url)
        if headers:
            for name, value in headers.items():
                message.get_request_headers().append(name, value)
        if 'User-Agent' not in headers:
            message.get_request_headers().append('User-Agent', 'Currency Converter')
        return message

    def get_response(self, message: Soup.Message):
        response = None
        try:
            response = self.send_and_read(message, None)
            data = response.get_data()
            return data
        except GLib.GError as error:
             raise error from error

class Requests:
    HEADERS: Dict[str, str] = {
        'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Referer': 'https://www.google.com',
    }
    def __init__(self, provider: int, from_currency: str, to_currency: str, from_currency_value: int):
        self.__provider = providers[provider](from_currency, to_currency, from_currency_value)
        self.__url = self.__provider.mount_url()
    def get(self):
        session = SoupSession();
        message = session.create_request("GET", self.__url, self.HEADERS)
        try:
            return self.__provider.serializer(session.get_response(message))
        except Exception as error:
            return error.message
