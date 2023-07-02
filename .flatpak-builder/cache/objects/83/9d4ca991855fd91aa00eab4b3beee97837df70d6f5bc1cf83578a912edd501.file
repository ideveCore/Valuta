import typing as T

from .. import OutputFormat
from ...language import *
from .xml_emitter import XmlEmitter


class XmlOutput(OutputFormat):
    def emit(self, ui: UI) -> str:
        xml = XmlEmitter()
        self._emit_ui(ui, xml)
        return xml.result

    def _emit_ui(self, ui: UI, xml: XmlEmitter):
        xml.start_tag("interface")

        for x in ui.children:
            if isinstance(x, GtkDirective):
                self._emit_gtk_directive(x, xml)
            elif isinstance(x, Import):
                pass
            elif isinstance(x, Template):
                self._emit_template(x, xml)
            elif isinstance(x, Object):
                self._emit_object(x, xml)
            elif isinstance(x, Menu):
                self._emit_menu(x, xml)
            else:
                raise CompilerBugError()

        xml.end_tag()

    def _emit_gtk_directive(self, gtk: GtkDirective, xml: XmlEmitter):
        xml.put_self_closing("requires", lib="gtk", version=gtk.gir_namespace.version)

    def _emit_template(self, template: Template, xml: XmlEmitter):
        xml.start_tag("template", **{"class": template.id}, parent=template.class_name)
        self._emit_object_or_template(template, xml)
        xml.end_tag()

    def _emit_object(self, obj: Object, xml: XmlEmitter):
        xml.start_tag(
            "object",
            **{"class": obj.class_name},
            id=obj.id,
        )
        self._emit_object_or_template(obj, xml)
        xml.end_tag()

    def _emit_object_or_template(self, obj: T.Union[Object, Template], xml: XmlEmitter):
        for child in obj.content.children:
            if isinstance(child, Property):
                self._emit_property(child, xml)
            elif isinstance(child, Signal):
                self._emit_signal(child, xml)
            elif isinstance(child, Child):
                self._emit_child(child, xml)
            else:
                self._emit_extensions(child, xml)

        # List action widgets
        action_widgets = obj.action_widgets
        if action_widgets:
            xml.start_tag("action-widgets")
            for action_widget in action_widgets:
                xml.start_tag(
                    "action-widget",
                    response=action_widget.response_id,
                    default=action_widget.is_default or None,
                )
                xml.put_text(action_widget.widget_id)
                xml.end_tag()
            xml.end_tag()

    def _emit_menu(self, menu: Menu, xml: XmlEmitter):
        xml.start_tag(menu.tag, id=menu.id)
        for child in menu.children:
            if isinstance(child, Menu):
                self._emit_menu(child, xml)
            elif isinstance(child, MenuAttribute):
                self._emit_attribute("attribute", "name", child.name, child.value, xml)
            else:
                raise CompilerBugError()
        xml.end_tag()

    def _emit_property(self, property: Property, xml: XmlEmitter):
        values = property.children[Value]
        value = values[0] if len(values) == 1 else None

        bind_flags = []
        if property.tokens["bind_source"] and not property.tokens["no_sync_create"]:
            bind_flags.append("sync-create")
        if property.tokens["inverted"]:
            bind_flags.append("invert-boolean")
        if property.tokens["bidirectional"]:
            bind_flags.append("bidirectional")
        bind_flags_str = "|".join(bind_flags) or None

        props = {
            "name": property.tokens["name"],
            "bind-source": property.tokens["bind_source"],
            "bind-property": property.tokens["bind_property"],
            "bind-flags": bind_flags_str,
        }

        if isinstance(value, TranslatedStringValue):
            xml.start_tag("property", **props, **self._translated_string_attrs(value))
            xml.put_text(value.string)
            xml.end_tag()
        elif len(property.children[Object]) == 1:
            xml.start_tag("property", **props)
            self._emit_object(property.children[Object][0], xml)
            xml.end_tag()
        elif value is None:
            if property.tokens["binding"]:
                xml.start_tag("binding", **props)
                self._emit_expression(property.children[Expr][0], xml)
                xml.end_tag()
            else:
                xml.put_self_closing("property", **props)
        else:
            xml.start_tag("property", **props)
            self._emit_value(value, xml)
            xml.end_tag()

    def _translated_string_attrs(
        self, translated: TranslatedStringValue
    ) -> T.Dict[str, T.Optional[str]]:
        return {
            "translatable": "true",
            "context": translated.context,
        }

    def _emit_signal(self, signal: Signal, xml: XmlEmitter):
        name = signal.name
        if signal.detail_name:
            name += "::" + signal.detail_name
        xml.put_self_closing(
            "signal",
            name=name,
            handler=signal.handler,
            swapped=signal.is_swapped or None,
            object=signal.object_id,
        )

    def _emit_child(self, child: Child, xml: XmlEmitter):
        child_type = internal_child = None

        if child.tokens["internal_child"]:
            internal_child = child.tokens["child_type"]
        else:
            child_type = child.tokens["child_type"]

        xml.start_tag("child", type=child_type, internal_child=internal_child)
        self._emit_object(child.object, xml)
        xml.end_tag()

    def _emit_value(self, value: Value, xml: XmlEmitter):
        if isinstance(value, IdentValue):
            if isinstance(value.parent.value_type, gir.Enumeration):
                xml.put_text(
                    value.parent.value_type.members[value.tokens["value"]].nick
                )
            else:
                xml.put_text(value.tokens["value"])
        elif isinstance(value, QuotedValue) or isinstance(value, NumberValue):
            xml.put_text(value.value)
        elif isinstance(value, FlagsValue):
            xml.put_text("|".join([flag.tokens["value"] for flag in value.children]))
        elif isinstance(value, TranslatedStringValue):
            raise CompilerBugError("translated values must be handled in the parent")
        elif isinstance(value, TypeValue):
            xml.put_text(value.type_name.glib_type_name)
        else:
            raise CompilerBugError()

    def _emit_expression(self, expression: Expr, xml: XmlEmitter):
        self._emit_expression_part(expression.children[-1], xml)

    def _emit_expression_part(self, expression, xml: XmlEmitter):
        if isinstance(expression, IdentExpr):
            self._emit_ident_expr(expression, xml)
        elif isinstance(expression, LookupOp):
            self._emit_lookup_op(expression, xml)
        elif isinstance(expression, Expr):
            self._emit_expression(expression, xml)
        else:
            raise CompilerBugError()

    def _emit_ident_expr(self, expr: IdentExpr, xml: XmlEmitter):
        xml.start_tag("constant")
        xml.put_text(expr.ident)
        xml.end_tag()

    def _emit_lookup_op(self, expr: LookupOp, xml: XmlEmitter):
        xml.start_tag("lookup", name=expr.property_name)
        self._emit_expression_part(expr.lhs, xml)
        xml.end_tag()

    def _emit_attribute(
        self, tag: str, attr: str, name: str, value: Value, xml: XmlEmitter
    ):
        attrs = {attr: name}

        if isinstance(value, TranslatedStringValue):
            xml.start_tag(tag, **attrs, **self._translated_string_attrs(value))
            xml.put_text(value.string)
            xml.end_tag()
        else:
            xml.start_tag(tag, **attrs)
            self._emit_value(value, xml)
            xml.end_tag()

    def _emit_extensions(self, extension, xml: XmlEmitter):
        if isinstance(extension, A11y):
            xml.start_tag("accessibility")
            for child in extension.children:
                self._emit_attribute(
                    child.tag_name, "name", child.name, child.children[Value][0], xml
                )
            xml.end_tag()

        elif isinstance(extension, Filters):
            xml.start_tag(extension.tokens["tag_name"])
            for child in extension.children:
                xml.start_tag(child.tokens["tag_name"])
                xml.put_text(child.tokens["name"])
                xml.end_tag()
            xml.end_tag()

        elif isinstance(extension, Items):
            xml.start_tag("items")
            for child in extension.children:
                self._emit_attribute(
                    "item", "id", child.name, child.children[Value][0], xml
                )
            xml.end_tag()

        elif isinstance(extension, Layout):
            xml.start_tag("layout")
            for child in extension.children:
                self._emit_attribute(
                    "property", "name", child.name, child.children[Value][0], xml
                )
            xml.end_tag()

        elif isinstance(extension, Strings):
            xml.start_tag("items")
            for child in extension.children:
                value = child.children[Value][0]
                if isinstance(value, TranslatedStringValue):
                    xml.start_tag("item", **self._translated_string_attrs(value))
                    xml.put_text(value.string)
                    xml.end_tag()
                else:
                    xml.start_tag("item")
                    self._emit_value(value, xml)
                    xml.end_tag()
            xml.end_tag()

        elif isinstance(extension, Styles):
            xml.start_tag("style")
            for child in extension.children:
                xml.put_self_closing("class", name=child.tokens["name"])
            xml.end_tag()

        elif isinstance(extension, Widgets):
            xml.start_tag("widgets")
            for child in extension.children:
                xml.put_self_closing("widget", name=child.tokens["name"])
            xml.end_tag()

        else:
            raise CompilerBugError()
