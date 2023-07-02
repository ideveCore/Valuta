# ui.py
#
# Copyright 2022 James Westman <james@jwestman.net>
#
# This file is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# This file is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: LGPL-3.0-or-later


from .. import gir
from .imports import GtkDirective, Import
from .gtkbuilder_template import Template
from .gobject_object import Object
from .gtk_menu import menu
from .common import *


class UI(AstNode):
    """ The AST node for the entire file """

    grammar = [
        GtkDirective,
        ZeroOrMore(Import),
        Until(AnyOf(
            Template,
            menu,
            Object,
        ), Eof()),
    ]

    @property
    def gir(self):
        gir_ctx = gir.GirContext()
        self._gir_errors = []

        try:
            if gtk := self.children[GtkDirective][0].gir_namespace:
                gir_ctx.add_namespace(gtk)
        except CompileError as e:
            self._gir_errors.append(e)

        for i in self.children[Import]:
            try:
                if i.gir_namespace is not None:
                    gir_ctx.add_namespace(i.gir_namespace)
            except CompileError as e:
                e.start = i.group.tokens["namespace"].start
                e.end = i.group.tokens["version"].end
                self._gir_errors.append(e)

        return gir_ctx


    @property
    def objects_by_id(self):
        return { obj.tokens["id"]: obj for obj in self.iterate_children_recursive() if obj.tokens["id"] is not None }


    @validate()
    def gir_errors(self):
        # make sure gir is loaded
        self.gir
        if len(self._gir_errors):
            raise MultipleErrors(self._gir_errors)


    @validate()
    def unique_ids(self):
        passed = {}
        for obj in self.iterate_children_recursive():
            if obj.tokens["id"] is None:
                continue

            if obj.tokens["id"] in passed:
                token = obj.group.tokens["id"]
                raise CompileError(f"Duplicate object ID '{obj.tokens['id']}'", token.start, token.end)
            passed[obj.tokens["id"]] = obj
