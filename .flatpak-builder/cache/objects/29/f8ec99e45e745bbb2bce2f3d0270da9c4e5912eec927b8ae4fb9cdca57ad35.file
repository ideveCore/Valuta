# gobject_property.py
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


from .expression import Expr
from .gobject_object import Object
from .gtkbuilder_template import Template
from .values import Value, TranslatedStringValue
from .common import *


class Property(AstNode):
    grammar = AnyOf(
        [
            UseIdent("name"),
            ":",
            Keyword("bind"),
            UseIdent("bind_source"),
            ".",
            UseIdent("bind_property"),
            ZeroOrMore(AnyOf(
                ["no-sync-create", UseLiteral("no_sync_create", True)],
                ["inverted", UseLiteral("inverted", True)],
                ["bidirectional", UseLiteral("bidirectional", True)],
                Match("sync-create").warn("sync-create is deprecated in favor of no-sync-create"),
            )),
            ";",
        ],
        Statement(
            UseIdent("name"),
            UseLiteral("binding", True),
            ":",
            "bind",
            Expr,
        ),
        Statement(
            UseIdent("name"),
            ":",
            AnyOf(
                Object,
                VALUE_HOOKS,
            ).expected("a value"),
        ),
    )

    @property
    def gir_class(self):
        return self.parent.parent.gir_class


    @property
    def gir_property(self):
        if self.gir_class is not None:
            return self.gir_class.properties.get(self.tokens["name"])


    @property
    def value_type(self):
        if self.gir_property is not None:
            return self.gir_property.type


    @validate("name")
    def property_exists(self):
        if self.gir_class is None:
            # Objects that we have no gir data on should not be validated
            # This happens for classes defined by the app itself
            return

        if isinstance(self.parent.parent, Template):
            # If the property is part of a template, it might be defined by
            # the application and thus not in gir
            return

        if self.gir_property is None:
            raise CompileError(
                f"Class {self.gir_class.full_name} does not contain a property called {self.tokens['name']}",
                did_you_mean=(self.tokens["name"], self.gir_class.properties.keys())
            )

    @validate("bind")
    def property_bindable(self):
        if self.tokens["bind"] and self.gir_property is not None and self.gir_property.construct_only:
            raise CompileError(
                f"{self.gir_property.full_name} can't be bound because it is construct-only",
                hints=["construct-only properties may only be set to a static value"]
            )

    @validate("name")
    def property_writable(self):
        if self.gir_property is not None and not self.gir_property.writable:
            raise CompileError(f"{self.gir_property.full_name} is not writable")


    @validate()
    def obj_property_type(self):
        if len(self.children[Object]) == 0:
            return

        object = self.children[Object][0]
        type = self.value_type
        if object and type and object.gir_class and not object.gir_class.assignable_to(type):
            raise CompileError(
                f"Cannot assign {object.gir_class.full_name} to {type.full_name}"
            )


    @validate("name")
    def unique_in_parent(self):
        self.validate_unique_in_parent(
            f"Duplicate property '{self.tokens['name']}'",
            check=lambda child: child.tokens["name"] == self.tokens["name"]
        )


    @docs("name")
    def property_docs(self):
        if self.gir_property is not None:
            return self.gir_property.doc
