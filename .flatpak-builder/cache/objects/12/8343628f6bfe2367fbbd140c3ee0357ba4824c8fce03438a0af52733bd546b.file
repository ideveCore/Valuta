# types.py
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


import typing as T
from .common import *
from ..gir import Class, Interface


class TypeName(AstNode):
    grammar = AnyOf(
        [
            UseIdent("namespace"),
            ".",
            UseIdent("class_name"),
        ],
        [
            ".",
            UseIdent("class_name"),
            UseLiteral("ignore_gir", True),
        ],
        UseIdent("class_name"),
    )

    @validate("class_name")
    def type_exists(self):
        if not self.tokens["ignore_gir"] and self.gir_ns is not None:
            self.root.gir.validate_type(self.tokens["class_name"], self.tokens["namespace"])

    @validate("namespace")
    def gir_ns_exists(self):
        if not self.tokens["ignore_gir"]:
            self.root.gir.validate_ns(self.tokens["namespace"])

    @property
    def gir_ns(self):
        if not self.tokens["ignore_gir"]:
            return self.root.gir.namespaces.get(self.tokens["namespace"] or "Gtk")

    @property
    def gir_type(self) -> T.Optional[gir.Class]:
        if self.tokens["class_name"] and not self.tokens["ignore_gir"]:
            return self.root.gir.get_type(self.tokens["class_name"], self.tokens["namespace"])
        return None

    @property
    def glib_type_name(self) -> str:
        if gir_type := self.gir_type:
            return gir_type.glib_type_name
        else:
            return self.tokens["class_name"]

    @docs("namespace")
    def namespace_docs(self):
        if ns := self.root.gir.namespaces.get(self.tokens["namespace"]):
            return ns.doc

    @docs("class_name")
    def class_docs(self):
        if self.gir_type:
            return self.gir_type.doc


class ClassName(TypeName):
    @validate("namespace", "class_name")
    def gir_class_exists(self):
        if self.gir_type is not None and not isinstance(self.gir_type, Class):
            if isinstance(self.gir_type, Interface):
                raise CompileError(f"{self.gir_type.full_name} is an interface, not a class")
            else:
                raise CompileError(f"{self.gir_type.full_name} is not a class")


class ConcreteClassName(ClassName):
    @validate("namespace", "class_name")
    def not_abstract(self):
        if isinstance(self.gir_type, Class) and self.gir_type.abstract:
            raise CompileError(
                f"{self.gir_type.full_name} can't be instantiated because it's abstract",
                hints=[f"did you mean to use a subclass of {self.gir_type.full_name}?"]
            )

