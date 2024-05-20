# main.py
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

from gi.repository import Adw, Gtk, Gio, Gdk, GObject
from valuta.define import RES_PATH

resource = f'{RES_PATH}/components/currencies/index.ui'

def currencies(application: Adw.Application):
  builder = Gtk.Builder.new_from_resource(resource)
  component = builder.get_object('component')
  list_box_editable = builder.get_object('list_box_editable')
  search_button = builder.get_object("search_button")
  search_bar = builder.get_object("search_bar")
  search_entry = builder.get_object("search_entry")
  currencies_list = {}
  currencies_code_list = []

  def substituir_numeros(lista, mapeamento):
    return [mapeamento[numero] if numero in mapeamento else numero for numero in lista]

  def open_uri(link: str):
    Gtk.show_uri(
      application.get_active_window(),
      link,
      Gdk.CURRENT_TIME
    );

  for currency in application.utils.currencies:
    key = currency
    currencies_code_list.append(f"{currency} – {application.utils.currencies[currency]['name'].replace('&', '&amp;')}")
    providers = application.utils.currencies[currency]["providers"].split(",")
    currencies_list[key] = {
      "name": _(f"{currency} – {application.utils.currencies[currency]['name'].replace('&', '&amp;')}"),
      "providers": ', '.join(substituir_numeros(providers, application.utils.providers)),
      "about_link": application.utils.currencies[currency]["about"]
    }

  model = Gtk.StringList(strings=currencies_code_list)

  # Filter-Model
  search_expression = Gtk.PropertyExpression.new(
      Gtk.StringObject,
      None,
      "string",
  )
  filter = Gtk.StringFilter(
      expression=search_expression,
      ignore_case=True,
      match_mode=Gtk.StringFilterMatchMode.SUBSTRING,
  )
  filter_model = Gtk.FilterListModel(
      model=model,
      filter=filter,
      incremental=True,
  )

  def create_item_for_filter_model(list_item):
      key = list_item.get_string().split("–")[0].strip()
      list_row = Adw.ActionRow(
          title=currencies_list[key]["name"],
          subtitle=currencies_list[key]["providers"],
      )
      if currencies_list[key]["about_link"]:
        about_button = Gtk.Button(
          icon_name="help-about-symbolic",
          tooltip_text=_("About"),
          halign="center",
          valign="center",
        )
        about_button.connect("clicked", lambda user_data: open_uri(currencies_list[key]["about_link"]))
        list_row.add_suffix(about_button)
      return list_row

  list_box_editable.bind_model(filter_model, create_item_for_filter_model)
  component.connect("close-attempt", lambda user_data: component.force_close())
  search_entry.connect(
      "search-changed", lambda _: filter.set_search(search_entry.get_text())
  )
  search_button.connect(
      "toggled", lambda user_data: search_bar.set_search_mode(user_data.get_active())
  )

  return component
