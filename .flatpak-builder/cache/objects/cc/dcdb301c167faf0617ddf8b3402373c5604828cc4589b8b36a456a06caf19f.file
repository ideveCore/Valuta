from .attributes import BaseAttribute, BaseTypedAttribute
from .expression import IdentExpr, LookupOp, Expr
from .gobject_object import Object, ObjectContent
from .gobject_property import Property
from .gobject_signal import Signal
from .gtk_a11y import A11y
from .gtk_combo_box_text import Items
from .gtk_file_filter import mime_types, patterns, suffixes, Filters
from .gtk_layout import Layout
from .gtk_menu import menu, Menu, MenuAttribute
from .gtk_size_group import Widgets
from .gtk_string_list import Strings
from .gtk_styles import Styles
from .gtkbuilder_child import Child
from .gtkbuilder_template import Template
from .imports import GtkDirective, Import
from .ui import UI
from .types import ClassName
from .values import TypeValue, IdentValue, TranslatedStringValue, FlagsValue, Flag, QuotedValue, NumberValue, Value

from .common import *

OBJECT_CONTENT_HOOKS.children = [
    Signal,
    Property,
    A11y,
    Styles,
    Layout,
    mime_types,
    patterns,
    suffixes,
    Widgets,
    Items,
    Strings,
    Child,
]

VALUE_HOOKS.children = [
    TypeValue,
    TranslatedStringValue,
    FlagsValue,
    IdentValue,
    QuotedValue,
    NumberValue,
]
