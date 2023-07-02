# common.py
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
from ..ast_utils import AstNode, validate, docs
from ..errors import CompileError, MultipleErrors
from ..completions_utils import *
from .. import decompiler as decompile
from ..decompiler import DecompileCtx, decompiler
from ..gir import StringType, BoolType, IntType, FloatType, GirType, Enumeration
from ..lsp_utils import Completion, CompletionItemKind, SemanticToken, SemanticTokenType
from ..parse_tree import *


OBJECT_CONTENT_HOOKS = AnyOf()
VALUE_HOOKS = AnyOf()
