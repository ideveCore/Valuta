# gir.py
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

from functools import cached_property
import typing as T
import os, sys

import gi # type: ignore
gi.require_version("GIRepository", "2.0")
from gi.repository import GIRepository # type: ignore

from .errors import CompileError, CompilerBugError
from . import typelib, xml_reader

_namespace_cache: T.Dict[str, "Namespace"] = {}
_xml_cache = {}


def get_namespace(namespace, version) -> "Namespace":
    search_paths = GIRepository.Repository.get_search_path()

    filename = f"{namespace}-{version}.typelib"

    if filename not in _namespace_cache:
        for search_path in search_paths:
            path = os.path.join(search_path, filename)

            if os.path.exists(path) and os.path.isfile(path):
                tl = typelib.load_typelib(path)
                repository = Repository(tl)

                _namespace_cache[filename] = repository.namespace
                break

        if filename not in _namespace_cache:
            raise CompileError(
                f"Namespace {namespace}-{version} could not be found",
                hints=["search path: " + os.pathsep.join(search_paths)],
            )

    return _namespace_cache[filename]


def get_xml(namespace, version):
    from .main import VERSION
    from xml.etree import ElementTree
    search_paths = []

    if data_paths := os.environ.get("XDG_DATA_DIRS"):
        search_paths += [os.path.join(path, "gir-1.0") for path in data_paths.split(os.pathsep)]

    filename = f"{namespace}-{version}.gir"

    if filename not in _xml_cache:
        for search_path in search_paths:
            path = os.path.join(search_path, filename)

            if os.path.exists(path) and os.path.isfile(path):
                _xml_cache[filename] = xml_reader.parse(path)
                break

        if filename not in _xml_cache:
            raise CompileError(
                f"GObject introspection file '{namespace}-{version}.gir' could not be found",
                hints=["search path: " + os.pathsep.join(search_paths)],
            )

    return _xml_cache[filename]


class GirType:
    @property
    def doc(self):
        return None

    def assignable_to(self, other) -> bool:
        raise NotImplementedError()

    @property
    def full_name(self) -> str:
        raise NotImplementedError()


class BasicType(GirType):
    name: str = "unknown type"

    @property
    def full_name(self) -> str:
        return self.name

class BoolType(BasicType):
    name = "bool"
    def assignable_to(self, other) -> bool:
        return isinstance(other, BoolType)

class IntType(BasicType):
    name = "int"
    def assignable_to(self, other) -> bool:
        return isinstance(other, IntType) or isinstance(other, UIntType) or isinstance(other, FloatType)

class UIntType(BasicType):
    name = "uint"
    def assignable_to(self, other) -> bool:
        return isinstance(other, IntType) or isinstance(other, UIntType) or isinstance(other, FloatType)

class FloatType(BasicType):
    name = "float"
    def assignable_to(self, other) -> bool:
        return isinstance(other, FloatType)

class StringType(BasicType):
    name = "string"
    def assignable_to(self, other) -> bool:
        return isinstance(other, StringType)

class TypeType(BasicType):
    name = "GType"
    def assignable_to(self, other) -> bool:
        return isinstance(other, TypeType)

_BASIC_TYPES = {
    "gboolean": BoolType,
    "int": IntType,
    "gint": IntType,
    "gint64": IntType,
    "guint": UIntType,
    "guint64": UIntType,
    "gfloat": FloatType,
    "gdouble": FloatType,
    "float": FloatType,
    "double": FloatType,
    "utf8": StringType,
    "gtype": TypeType,
    "type": TypeType,
}

class GirNode:
    def __init__(self, container, tl):
        self.container = container
        self.tl = tl

    def get_containing(self, container_type):
        if self.container is None:
            return None
        elif isinstance(self.container, container_type):
            return self.container
        else:
            return self.container.get_containing(container_type)

    @cached_property
    def xml(self):
        for el in self.container.xml.children:
            if el.attrs.get("name") == self.name:
                return el

    @cached_property
    def glib_type_name(self):
        return self.tl.OBJ_GTYPE_NAME

    @cached_property
    def full_name(self):
        if self.container is None:
            return self.name
        else:
            return f"{self.container.name}.{self.name}"

    @cached_property
    def name(self) -> str:
        return self.tl.BLOB_NAME

    @cached_property
    def cname(self) -> str:
        return self.tl.OBJ_GTYPE_NAME

    @cached_property
    def available_in(self) -> str:
        return self.xml.get("version")

    @cached_property
    def doc(self) -> T.Optional[str]:
        sections = []

        if self.signature:
            sections.append("```\n" + self.signature + "\n```")

        try:
            el = self.xml.get_elements("doc")
            if len(el) == 1:
                sections.append(el[0].cdata.strip())
        except:
            # Not a huge deal, but if you want docs in the language server you
            # should ensure .gir files are installed
            pass

        return "\n\n---\n\n".join(sections)

    @property
    def signature(self) -> T.Optional[str]:
        return None

    @property
    def type_name(self):
        return self.type.name

    @property
    def type(self):
        raise NotImplementedError()


class Property(GirNode):
    def __init__(self, klass, tl: typelib.Typelib):
        super().__init__(klass, tl)

    @cached_property
    def name(self):
        return self.tl.PROP_NAME

    @cached_property
    def type(self):
        return self.get_containing(Repository)._resolve_type_id(self.tl.PROP_TYPE)

    @cached_property
    def signature(self):
        return f"{self.type_name} {self.container.name}.{self.name}"

    @property
    def writable(self):
        return self.tl.PROP_WRITABLE == 1

    @property
    def construct_only(self):
        return self.tl.PROP_CONSTRUCT_ONLY == 1


class Parameter(GirNode):
    def __init__(self, container: GirNode, tl: typelib.Typelib):
        super().__init__(container, tl)


class Signal(GirNode):
    def __init__(self, klass, tl: typelib.Typelib):
        super().__init__(klass, tl)
        # if parameters := xml.get_elements('parameters'):
        #     self.params = [Parameter(self, child) for child in parameters[0].get_elements('parameter')]
        # else:
        #     self.params = []

    @property
    def signature(self):
        # TODO: fix
        # args = ", ".join([f"{p.type_name} {p.name}" for p in self.params])
        args = ""
        return f"signal {self.container.name}.{self.name} ({args})"


class Interface(GirNode, GirType):
    def __init__(self, ns, tl: typelib.Typelib):
        super().__init__(ns, tl)

    @cached_property
    def properties(self):
        n_prerequisites = self.tl.INTERFACE_N_PREREQUISITES
        offset = self.tl.header.HEADER_INTERFACE_BLOB_SIZE
        offset += (n_prerequisites + n_prerequisites % 2) * 2
        n_properties = self.tl.INTERFACE_N_PROPERTIES
        property_size = self.tl.header.HEADER_PROPERTY_BLOB_SIZE
        result = {}
        for i in range(n_properties):
            property = Property(self, self.tl[offset + i * property_size])
            result[property.name] = property
        return result

    @cached_property
    def signals(self):
        n_prerequisites = self.tl.INTERFACE_N_PREREQUISITES
        offset = self.tl.header.HEADER_INTERFACE_BLOB_SIZE
        offset += (n_prerequisites + n_prerequisites % 2) * 2
        offset += self.tl.INTERFACE_N_PROPERTIES * self.tl.header.HEADER_PROPERTY_BLOB_SIZE
        offset += self.tl.INTERFACE_N_METHODS * self.tl.header.HEADER_FUNCTION_BLOB_SIZE
        n_signals = self.tl.INTERFACE_N_SIGNALS
        property_size = self.tl.header.HEADER_SIGNAL_BLOB_SIZE
        result = {}
        for i in range(n_signals):
            signal = Signal(self, self.tl[offset + i * property_size])
            result[signal.name] = signal
        return result

    @cached_property
    def prerequisites(self):
        n_prerequisites = self.tl.INTERFACE_N_PREREQUISITES
        result = []
        for i in range(n_prerequisites):
            entry = self.tl.INTERFACE_PREREQUISITES[i * 2].AS_DIR_ENTRY
            result.append(self.get_containing(Repository)._resolve_dir_entry(entry))
        return result

    def assignable_to(self, other) -> bool:
        if self == other:
            return True
        for pre in self.prerequisites:
            if pre.assignable_to(other):
                return True
        return False


class Class(GirNode, GirType):
    def __init__(self, ns, tl: typelib.Typelib):
        super().__init__(ns, tl)

    @property
    def abstract(self):
        return self.tl.OBJ_ABSTRACT == 1

    @cached_property
    def implements(self):
        n_interfaces = self.tl.OBJ_N_INTERFACES
        result = []
        for i in range(n_interfaces):
            entry = self.tl[self.tl.header.HEADER_OBJECT_BLOB_SIZE + i * 2].AS_DIR_ENTRY
            result.append(self.get_containing(Repository)._resolve_dir_entry(entry))
        return result

    @cached_property
    def own_properties(self):
        n_interfaces = self.tl.OBJ_N_INTERFACES
        offset = self.tl.header.HEADER_OBJECT_BLOB_SIZE
        offset += (n_interfaces + n_interfaces % 2) * 2
        offset += self.tl.OBJ_N_FIELDS * self.tl.header.HEADER_FIELD_BLOB_SIZE
        offset += self.tl.OBJ_N_FIELD_CALLBACKS * self.tl.header.HEADER_CALLBACK_BLOB_SIZE
        n_properties = self.tl.OBJ_N_PROPERTIES
        property_size = self.tl.header.HEADER_PROPERTY_BLOB_SIZE
        result = {}
        for i in range(n_properties):
            property = Property(self, self.tl[offset + i * property_size])
            result[property.name] = property
        return result

    @cached_property
    def own_signals(self):
        n_interfaces = self.tl.OBJ_N_INTERFACES
        offset = self.tl.header.HEADER_OBJECT_BLOB_SIZE
        offset += (n_interfaces + n_interfaces % 2) * 2
        offset += self.tl.OBJ_N_FIELDS * self.tl.header.HEADER_FIELD_BLOB_SIZE
        offset += self.tl.OBJ_N_FIELD_CALLBACKS * self.tl.header.HEADER_CALLBACK_BLOB_SIZE
        offset += self.tl.OBJ_N_PROPERTIES * self.tl.header.HEADER_PROPERTY_BLOB_SIZE
        offset += self.tl.OBJ_N_METHODS * self.tl.header.HEADER_FUNCTION_BLOB_SIZE
        n_signals = self.tl.OBJ_N_SIGNALS
        signal_size = self.tl.header.HEADER_SIGNAL_BLOB_SIZE
        result = {}
        for i in range(n_signals):
            signal = Signal(self, self.tl[offset][i * signal_size])
            result[signal.name] = signal
        return result

    @cached_property
    def parent(self):
        if entry := self.tl.OBJ_PARENT:
            return self.get_containing(Repository)._resolve_dir_entry(entry)
        else:
            return None

    @cached_property
    def signature(self):
        result = f"class {self.container.name}.{self.name}"
        if self.parent is not None:
            result += f" : {self.parent.container.name}.{self.parent.name}"
        if len(self.implements):
            result += " implements " + ", ".join([impl.full_name for impl in self.implements])
        return result

    @cached_property
    def properties(self):
        return { p.name: p for p in self._enum_properties() }

    @cached_property
    def signals(self):
        return { s.name: s for s in self._enum_signals() }

    def assignable_to(self, other) -> bool:
        if self == other:
            return True
        elif self.parent and self.parent.assignable_to(other):
            return True
        else:
            for iface in self.implements:
                if iface.assignable_to(other):
                    return True

            return False

    def _enum_properties(self):
        yield from self.own_properties.values()

        if self.parent is not None:
            yield from self.parent.properties.values()

        for impl in self.implements:
            yield from impl.properties.values()

    def _enum_signals(self):
        yield from self.own_signals.values()

        if self.parent is not None:
            yield from self.parent.signals.values()

        for impl in self.implements:
            yield from impl.signals.values()


class EnumMember(GirNode):
    def __init__(self, ns, tl: typelib.Typelib):
        super().__init__(ns, tl)

    @property
    def value(self):
        return self.tl.VALUE_VALUE

    @cached_property
    def name(self):
        return self.tl.VALUE_NAME

    @cached_property
    def nick(self):
        return self.name.replace("_", "-")

    @property
    def c_ident(self):
        return self.tl.attr("c:identifier")

    @property
    def signature(self):
        return f"enum member {self.full_name} = {self.value}"


class Enumeration(GirNode, GirType):
    def __init__(self, ns, tl: typelib.Typelib):
        super().__init__(ns, tl)

    @cached_property
    def members(self):
        members = {}
        n_values = self.tl.ENUM_N_VALUES
        values = self.tl.ENUM_VALUES
        value_size = self.tl.header.HEADER_VALUE_BLOB_SIZE
        for i in range(n_values):
            member = EnumMember(self, values[i * value_size])
            members[member.name] = member
        return members

    @property
    def signature(self):
        return f"enum {self.full_name}"

    def assignable_to(self, type):
        return type == self


class Boxed(GirNode, GirType):
    def __init__(self, ns, tl: typelib.Typelib):
        super().__init__(ns, tl)

    @property
    def signature(self):
        return f"boxed {self.full_name}"

    def assignable_to(self, type):
        return type == self


class Bitfield(Enumeration):
    def __init__(self, ns, tl: typelib.Typelib):
        super().__init__(ns, tl)


class Namespace(GirNode):
    def __init__(self, repo, tl: typelib.Typelib):
        super().__init__(repo, tl)

        self.entries: T.Dict[str, GirNode] = {}

        n_local_entries = tl.HEADER_N_ENTRIES
        directory = tl.HEADER_DIRECTORY
        for i in range(n_local_entries):
            entry = directory[i * tl.HEADER_ENTRY_BLOB_SIZE]
            entry_name = entry.DIR_ENTRY_NAME
            entry_type = entry.DIR_ENTRY_BLOB_TYPE
            entry_blob = entry.DIR_ENTRY_OFFSET

            if entry_type == typelib.BLOB_TYPE_ENUM:
                self.entries[entry_name] = Enumeration(self, entry_blob)
            elif entry_type == typelib.BLOB_TYPE_FLAGS:
                self.entries[entry_name] = Bitfield(self, entry_blob)
            elif entry_type == typelib.BLOB_TYPE_OBJECT:
                self.entries[entry_name] = Class(self, entry_blob)
            elif entry_type == typelib.BLOB_TYPE_INTERFACE:
                 self.entries[entry_name] = Interface(self, entry_blob)
            elif entry_type == typelib.BLOB_TYPE_BOXED or entry_type == typelib.BLOB_TYPE_STRUCT:
                 self.entries[entry_name] = Boxed(self, entry_blob)

    @cached_property
    def xml(self):
        return get_xml(self.name, self.version).get_elements("namespace")[0]

    @cached_property
    def name(self) -> str:
        return self.tl.HEADER_NAMESPACE

    @cached_property
    def version(self) -> str:
        return self.tl.HEADER_NSVERSION

    @property
    def signature(self):
        return f"namespace {self.name} {self.version}"

    @cached_property
    def classes(self):
        return { name: entry for name, entry in self.entries.items() if isinstance(entry, Class) }

    @cached_property
    def interfaces(self):
        return { name: entry for name, entry in self.entries.items() if isinstance(entry, Interface) }

    def get_type(self, name):
        """ Gets a type (class, interface, enum, etc.) from this namespace. """
        return self.entries.get(name)

    def get_type_by_cname(self, cname: str):
        """ Gets a type from this namespace by its C name. """
        for item in self.entries.values():
            if hasattr(item, "cname") and item.cname == cname:
                return item

    def lookup_type(self, type_name: str):
        """ Looks up a type in the scope of this namespace (including in the
        namespace's dependencies). """

        if type_name in _BASIC_TYPES:
            return _BASIC_TYPES[type_name]()
        elif "." in type_name:
            ns, name = type_name.split(".", 1)
            return self.get_containing(Repository).get_type(name, ns)
        else:
            return self.get_type(type_name)


class Repository(GirNode):
    def __init__(self, tl: typelib.Typelib):
        super().__init__(None, tl)

        self.namespace = Namespace(self, tl)

        if dependencies := tl[0x24].string:
            deps = [tuple(dep.split("-", 1)) for dep in dependencies.split("|")]
            try:
                self.includes = { name: get_namespace(name, version) for name, version in deps }
            except:
                raise CompilerBugError(f"Failed to load dependencies.")
        else:
            self.includes = {}

    def get_type(self, name: str, ns: str) -> T.Optional[GirNode]:
        return self.lookup_namespace(ns).get_type(name)


    def get_type_by_cname(self, name: str) -> T.Optional[GirNode]:
        for ns in [self.namespace, *self.includes.values()]:
            if type := ns.get_type_by_cname(name):
                return type
        return None


    def lookup_namespace(self, ns: str):
        """ Finds a namespace among this namespace's dependencies. """
        if ns == self.namespace.name:
            return self.namespace
        else:
            for include in self.includes.values():
                if namespace := include.get_containing(Repository).lookup_namespace(ns):
                    return namespace

    def _resolve_dir_entry(self, dir_entry: typelib.Typelib):
        if dir_entry.DIR_ENTRY_LOCAL:
            return self.namespace.get_type(dir_entry.DIR_ENTRY_NAME)
        else:
            ns = dir_entry.DIR_ENTRY_NAMESPACE
            return self.lookup_namespace(ns).get_type(dir_entry.DIR_ENTRY_NAME)

    def _resolve_type_id(self, type_id: int):
        if type_id & 0xFFFFFF == 0:
            type_id = (type_id >> 27) & 0x1F
            # simple type
            if type_id == typelib.TYPE_BOOLEAN:
                return BoolType()
            elif type_id in [typelib.TYPE_FLOAT, typelib.TYPE_DOUBLE]:
                return FloatType()
            elif type_id in [typelib.TYPE_INT8, typelib.TYPE_INT16, typelib.TYPE_INT32, typelib.TYPE_INT64]:
                return IntType()
            elif type_id in [typelib.TYPE_UINT8, typelib.TYPE_UINT16, typelib.TYPE_UINT32, typelib.TYPE_UINT64]:
                return UIntType()
            elif type_id == typelib.TYPE_UTF8:
                return StringType()
            elif type_id == typelib.TYPE_GTYPE:
                return TypeType()
            else:
                raise CompilerBugError("Unknown type ID", type_id)
        else:
            return self._resolve_dir_entry(self.tl.header[type_id].INTERFACE_TYPE_INTERFACE)



class GirContext:
    def __init__(self):
        self.namespaces = {}


    def add_namespace(self, namespace: Namespace):
        other = self.namespaces.get(namespace.name)
        if other is not None and other.version != namespace.version:
            raise CompileError(f"Namespace {namespace.name}-{namespace.version} can't be imported because version {other.version} was imported earlier")

        self.namespaces[namespace.name] = namespace


    def get_type_by_cname(self, name: str) -> T.Optional[GirNode]:
        for ns in self.namespaces.values():
            if type := ns.get_type_by_cname(name):
                return type
        return None


    def get_type(self, name: str, ns: str) -> T.Optional[GirNode]:
        ns = ns or "Gtk"

        if ns not in self.namespaces:
            return None

        return self.namespaces[ns].get_type(name)


    def get_class(self, name: str, ns: str) -> T.Optional[Class]:
        type = self.get_type(name, ns)
        if isinstance(type, Class):
            return type
        else:
            return None


    def validate_ns(self, ns: str):
        """ Raises an exception if there is a problem looking up the given
        namespace. """

        ns = ns or "Gtk"

        if ns not in self.namespaces:
            raise CompileError(
                f"Namespace {ns} was not imported",
                did_you_mean=(ns, self.namespaces.keys()),
            )

    def validate_type(self, name: str, ns: str):
        """ Raises an exception if there is a problem looking up the given type. """

        self.validate_ns(ns)

        type = self.get_type(name, ns)

        ns = ns or "Gtk"

        if type is None:
            raise CompileError(
                f"Namespace {ns} does not contain a type called {name}",
                did_you_mean=(name, self.namespaces[ns].classes.keys()),
            )
