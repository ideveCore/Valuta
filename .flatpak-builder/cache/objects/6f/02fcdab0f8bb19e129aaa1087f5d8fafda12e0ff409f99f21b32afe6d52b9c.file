# parser.py
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


from .errors import MultipleErrors, PrintableError
from .parse_tree import *
from .tokenizer import TokenType
from .language import OBJECT_CONTENT_HOOKS, VALUE_HOOKS, Template, UI


def parse(tokens) -> T.Tuple[UI, T.Optional[MultipleErrors], T.List[PrintableError]]:
    """ Parses a list of tokens into an abstract syntax tree. """

    ctx = ParseContext(tokens)
    AnyOf(UI).parse(ctx)

    ast_node = ctx.last_group.to_ast() if ctx.last_group else None
    errors = MultipleErrors(ctx.errors) if len(ctx.errors) else None
    warnings = ctx.warnings

    return (ast_node, errors, warnings)
