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
from datetime import datetime, UTC, timedelta
import gi, json, re
gi.require_version('Soup', '3.0')
from gi.repository import Soup, GLib
from .define import BASE_URL_LANG_PREFIX, CODES

class Providers:
  response = {
    "from": "",
    "to": "",
    "amount": "",
    "converted": False,
    "info": "",
    "disclaimer": "",
    "warning": "",
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

class ECB(Providers):
  ECB_BASE_URL: str = 'https://api.frankfurter.app/latest'
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
    self.response["warning"] = ""
    self.response["provider"] = 0
    return self.response

  def create_info(self, date: str, time: str = "00:00:00"):
    date = date.split("-")
    time = time.split(":")
    date_time = GLib.DateTime.new_local(float(date[0]), float(date[1]), float(date[2]), float(time[0]), float(time[1]), float(time[2]))
    return date_time.format("%B%e, %Y")

class InforEuro(Providers):
  INFORMEURO_BASE_URL: str = (
    "https://ec.europa.eu/budg/inforeuro/api/public"
  )

  def mount_url(self):
    now = datetime.now(UTC)

    return (
      f"{self.INFORMEURO_BASE_URL}/monthly-rates"
      f"?year={now.year}&month={now.month}"
    )

  def serializer(self, data: bytes):
    return self.default_response(json.loads(data))

  def get_rate(self, data, currency):
    """
    InforEuro rates are quoted as:
    1 EUR = value * currency
    """

    if currency == "EUR":
        return 1.0

    for item in data:
      if item["isoA3Code"] == currency:
        return float(item["value"])

    raise ValueError(f"Currency '{currency}' not found")

  def default_response(self, data):
    from_rate = self.get_rate(data, self.from_currency)
    to_rate = self.get_rate(data, self.to_currency)

    # EUR pivot conversion
    eur_amount = float(self.from_currency_value) / from_rate
    converted_amount = eur_amount * to_rate

    self.response["base"] = converted_amount
    self.response["from"] = self.from_currency
    self.response["to"] = self.to_currency
    self.response["amount"] = self.from_currency_value
    self.response["converted"] = True

    now = datetime.now(UTC)

    self.response["info"] = now.strftime("%B %Y")
    self.response["disclaimer"] = self.mount_url()
    self.response["warning"] = "InforEuro rates are updated monthly."
    self.response["provider"] = 1

    return self.response

providers = {
  0 : ECB,
  1 : InforEuro
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

class HistoryRequest:
  HEADERS: Dict[str, str] = {
      'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0',
  }
  def __init__(self, provider: int, from_currency: str, to_currency: str, days: int = 30):
    self.provider = provider
    self.from_currency = from_currency
    self.to_currency = to_currency
    self.days = days

  def get(self) -> Dict[str, Any]:
    if self.provider != 0:
      return {"supported": False, "error": "Provider not supported for history"}

    if self.from_currency == self.to_currency:
      now_str = datetime.now(UTC).strftime("%Y-%m-%d")
      points = [{"date": now_str, "rate": 1.0}]
      return {
        "supported": True,
        "from": self.from_currency,
        "to": self.to_currency,
        "points": points,
        "latest": 1.0,
        "first": 1.0,
        "change": 0.0,
        "change_pct": 0.0,
        "min": 1.0,
        "max": 1.0,
        "avg": 1.0,
      }

    start_date = (datetime.now(UTC) - timedelta(days=self.days)).strftime("%Y-%m-%d")
    url = f"https://api.frankfurter.app/{start_date}..?from={self.from_currency}&to={self.to_currency}"

    session = SoupSession()
    message = session.create_request("GET", url, self.HEADERS)
    try:
      raw_data = session.get_response(message)
      data = json.loads(raw_data)
      rates = data.get("rates", {})
      points = []
      for d_str in sorted(rates.keys()):
        r_map = rates[d_str]
        if self.to_currency in r_map:
          points.append({"date": d_str, "rate": float(r_map[self.to_currency])})

      if not points:
        return {"supported": True, "error": "No historical data found"}

      first = points[0]["rate"]
      latest = points[-1]["rate"]
      change = latest - first
      change_pct = (change / first * 100) if first != 0 else 0
      vals = [p["rate"] for p in points]

      return {
        "supported": True,
        "from": self.from_currency,
        "to": self.to_currency,
        "points": points,
        "latest": latest,
        "first": first,
        "change": change,
        "change_pct": change_pct,
        "min": min(vals),
        "max": max(vals),
        "avg": sum(vals) / len(vals),
      }
    except Exception as error:
      return {"supported": True, "error": str(error)}

