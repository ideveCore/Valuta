# convertion.py
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

import gi
from typing import Union, Any, Dict

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gtk
from ...components import CurrencySelector
from ...utils import CurrenciesListModel
from ...define import RES_PATH, CODES

resource = f"{RES_PATH}/pages/convertion/index.ui"

def convertion_page(application: Adw.Application):
    builder = Gtk.Builder.new_from_resource(resource)
    settings = application.utils.settings
    page = builder.get_object("page")
    from_currency_selector: CurrencySelector = builder.get_object("from_currency_selector")
    to_currency_selector: CurrencySelector = builder.get_object("to_currency_selector")

    def currency_names_func(code):
        name = gettext(CODES.get(code, '')['name'])
        return name if name else None

    from_currency_model = CurrenciesListModel(currency_names_func)
    to_currency_model = CurrenciesListModel(currency_names_func)
    # dest_currency_selector: CurrencySelector = Gtk.Template.Child()

    from_currency_selector.bind_models(from_currency_model)
    from_currency_model.set_currencies(CODES)
    to_currency_selector.bind_models(to_currency_model)
    to_currency_model.set_currencies(CODES)

    from_currency_selector.set_selected(settings.get_string('src-currency'))
    to_currency_selector.set_selected(settings.get_string('dest-currency'))
    # self.dest_currency_selector.set_selected(self.dest_currency)
    return page
