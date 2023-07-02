# gtk_layout.py
#
# Copyright 2021 James Westman <james@jwestman.net>
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


from .attributes import BaseAttribute
from .gobject_object import ObjectContent, validate_parent_type
from .common import *


class LayoutProperty(BaseAttribute):
    tag_name = "property"

    @property
    def value_type(self):
        # there isn't really a way to validate these
        return None

    @validate("name")
    def unique_in_parent(self):
        self.validate_unique_in_parent(
            f"Duplicate layout property '{self.name}'",
            check=lambda child: child.name == self.name,
        )


layout_prop = Group(
    LayoutProperty,
    Statement(
        UseIdent("name"),
        ":",
        VALUE_HOOKS.expected("a value"),
    )
)


class Layout(AstNode):
    grammar = Sequence(
        Keyword("layout"),
        "{",
        Until(layout_prop, "}"),
    )

    @validate("layout")
    def container_is_widget(self):
        validate_parent_type(self, "Gtk", "Widget", "layout properties")

    @validate("layout")
    def unique_in_parent(self):
        self.validate_unique_in_parent("Duplicate layout block")


@completer(
    applies_in=[ObjectContent],
    applies_in_subclass=("Gtk", "Widget"),
    matches=new_statement_patterns,
)
def layout_completer(ast_node, match_variables):
    yield Completion(
        "layout", CompletionItemKind.Snippet,
        snippet="layout {\n  $0\n}"
    )


@decompiler("layout")
def decompile_layout(ctx, gir):
    ctx.print("layout {")
