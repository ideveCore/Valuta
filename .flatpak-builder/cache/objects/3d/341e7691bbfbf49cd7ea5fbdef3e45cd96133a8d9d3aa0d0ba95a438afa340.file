# values.py
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
from .types import TypeName


class Value(AstNode):
    pass


class TranslatedStringValue(Value):
    grammar = AnyOf(
        [
            "_",
            "(",
            UseQuoted("value").expected("a quoted string"),
            Match(")").expected(),
        ],
        [
            "C_",
            "(",
            UseQuoted("context").expected("a quoted string"),
            ",",
            UseQuoted("value").expected("a quoted string"),
            Optional(","),
            Match(")").expected(),
        ],
    )

    @property
    def string(self) -> str:
        return self.tokens["value"]

    @property
    def context(self) -> T.Optional[str]:
        return self.tokens["context"]


class TypeValue(Value):
    grammar = [
        "typeof",
        "(",
        to_parse_node(TypeName).expected("type name"),
        Match(")").expected(),
    ]

    @property
    def type_name(self):
        return self.children[TypeName][0]

    @validate()
    def validate_for_type(self):
        type = self.parent.value_type
        if type is not None and not isinstance(type, gir.TypeType):
            raise CompileError(f"Cannot convert GType to {type.full_name}")


class QuotedValue(Value):
    grammar = UseQuoted("value")

    @property
    def value(self) -> str:
        return self.tokens["value"]

    @validate()
    def validate_for_type(self):
        type = self.parent.value_type
        if isinstance(type, gir.IntType) or isinstance(type, gir.UIntType) or isinstance(type, gir.FloatType):
            raise CompileError(f"Cannot convert string to number")

        elif isinstance(type, gir.StringType):
            pass

        elif isinstance(type, gir.Class) or isinstance(type, gir.Interface) or isinstance(type, gir.Boxed):
            parseable_types = [
                "Gdk.Paintable",
                "Gdk.Texture",
                "Gdk.Pixbuf",
                "GLib.File",
                "Gtk.ShortcutTrigger",
                "Gtk.ShortcutAction",
                "Gdk.RGBA",
                "Gdk.ContentFormats",
                "Gsk.Transform",
                "GLib.Variant",
            ]
            if type.full_name not in parseable_types:
                hints = []
                if isinstance(type, gir.TypeType):
                    hints.append(f"use the typeof operator: 'typeof({self.tokens('value')})'")
                raise CompileError(f"Cannot convert string to {type.full_name}", hints=hints)

        elif type is not None:
            raise CompileError(f"Cannot convert string to {type.full_name}")


class NumberValue(Value):
    grammar = UseNumber("value")

    @property
    def value(self) -> T.Union[int, float]:
        return self.tokens["value"]

    @validate()
    def validate_for_type(self):
        type = self.parent.value_type
        if isinstance(type, gir.IntType):
            try:
                int(self.tokens["value"])
            except:
                raise CompileError(f"Cannot convert {self.group.tokens['value']} to integer")

        elif isinstance(type, gir.UIntType):
            try:
                int(self.tokens["value"])
                if int(self.tokens["value"]) < 0:
                    raise Exception()
            except:
                raise CompileError(f"Cannot convert {self.group.tokens['value']} to unsigned integer")

        elif isinstance(type, gir.FloatType):
            try:
                float(self.tokens["value"])
            except:
                raise CompileError(f"Cannot convert {self.group.tokens['value']} to float")

        elif type is not None:
            raise CompileError(f"Cannot convert number to {type.full_name}")


class Flag(AstNode):
    grammar = UseIdent("value")

    @docs()
    def docs(self):
        type = self.parent.parent.value_type
        if not isinstance(type, Enumeration):
            return
        if member := type.members.get(self.tokens["value"]):
            return member.doc

    @validate()
    def validate_for_type(self):
        type = self.parent.parent.value_type
        if isinstance(type, gir.Bitfield) and self.tokens["value"] not in type.members:
            raise CompileError(
                f"{self.tokens['value']} is not a member of {type.full_name}",
                did_you_mean=(self.tokens['value'], type.members.keys()),
            )


class FlagsValue(Value):
    grammar = [Flag, "|", Delimited(Flag, "|")]

    @validate()
    def parent_is_bitfield(self):
        type = self.parent.value_type
        if type is not None and not isinstance(type, gir.Bitfield):
            raise CompileError(f"{type.full_name} is not a bitfield type")


class IdentValue(Value):
    grammar = UseIdent("value")

    @validate()
    def validate_for_type(self):
        type = self.parent.value_type

        if isinstance(type, gir.Enumeration):
            if self.tokens["value"] not in type.members:
                raise CompileError(
                    f"{self.tokens['value']} is not a member of {type.full_name}",
                    did_you_mean=(self.tokens['value'], type.members.keys()),
                )

        elif isinstance(type, gir.BoolType):
            if self.tokens["value"] not in ["true", "false"]:
                raise CompileError(
                    f"Expected 'true' or 'false' for boolean value",
                    did_you_mean=(self.tokens['value'], ["true", "false"]),
                )

        elif type is not None:
            object = self.root.objects_by_id.get(self.tokens["value"])
            if object is None:
                raise CompileError(
                    f"Could not find object with ID {self.tokens['value']}",
                    did_you_mean=(self.tokens['value'], self.root.objects_by_id.keys()),
                )
            elif object.gir_class and not object.gir_class.assignable_to(type):
                raise CompileError(
                    f"Cannot assign {object.gir_class.full_name} to {type.full_name}"
                )


    @docs()
    def docs(self):
        type = self.parent.value_type
        if isinstance(type, gir.Enumeration):
            if member := type.members.get(self.tokens["value"]):
                return member.doc
            else:
                return type.doc
        elif isinstance(type, gir.GirNode):
            return type.doc


    def get_semantic_tokens(self) -> T.Iterator[SemanticToken]:
        if isinstance(self.parent.value_type, gir.Enumeration):
            token = self.group.tokens["value"]
            yield SemanticToken(token.start, token.end, SemanticTokenType.EnumMember)

