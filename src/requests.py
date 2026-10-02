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
    ECB_BASE_URL: str = 'https://api.frankfurter.app/latest'
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
        date_time = GLib.DateTime.new_local(float(date[0]), float(date[1]), float(date[2]), float(time[0]), float(time[1]), float(time[2]))
        return date_time.format("%B %e, %Y")

class ECB(Providers):
    # Currencies the ECB/Frankfurter feed does not quote, but which are
    # officially pegged to a currency it does quote. Each entry maps a
    # currency to (api_currency, units_of_currency_per_api_currency).
    # The Nepalese rupee has been pegged to the Indian rupee at
    # 1 INR = 1.6 NPR since 1993.
    PEGGED = {
        "NPR": ("INR", 1.6),
    }

    def _api_currency(self, code: str) -> str:
        return self.PEGGED[code][0] if code in self.PEGGED else code

    def _peg_factor(self, code: str) -> float:
        """Units of ``code`` per 1 unit of its underlying API currency."""
        return self.PEGGED[code][1] if code in self.PEGGED else 1.0

    def mount_url(self):
        return f'{self.ECB_BASE_URL}?amount={self.from_currency_value}&from={self._api_currency(self.from_currency)}&to={self._api_currency(self.to_currency)}'

    def serializer(self, data: bytes) -> Dict[str, Union[str, int]]:
        return self.default_response(json.loads(data))

    def default_response(self, data: Dict[str, str]):
        api_from = self._api_currency(self.from_currency)
        api_to = self._api_currency(self.to_currency)
        if api_from == api_to:
            # e.g. NPR <-> INR: both resolve to the same API currency, so the
            # feed can't quote the pair. The rate is purely the peg ratio.
            api_rate = 1.0
            info_date = data.get("date") if isinstance(data, dict) else None
        else:
            api_rate = data["rates"][api_to]
            info_date = data["date"]
        self.response["base"] = api_rate * self._peg_factor(self.to_currency) / self._peg_factor(self.from_currency)
        self.response["from"] = self.from_currency
        self.response["to"] = self.to_currency
        self.response["amount"] = 0
        self.response["info"] = self.create_info(info_date or datetime.now().strftime("%Y-%m-%d"))
        self.response["disclaimer"] = self.mount_url()
        self.response["provider"] = 0
        return self.response

providers = {
    0 : ECB,
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
