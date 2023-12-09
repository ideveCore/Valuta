/* panel-frame-header-bar.c
 *
 * Copyright 2021 Christian Hergert <chergert@redhat.com>
 *
 * This file is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * This file is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "config.h"

#include <glib/gi18n.h>

#include <adwaita.h>

#include "panel-dock-private.h"
#include "panel-frame-private.h"
#include "panel-frame-header.h"
#include "panel-frame-header-bar.h"
#include "panel-frame-header-bar-row-private.h"
#include "panel-joined-menu-private.h"
#include "panel-scaler-private.h"
#include "panel-widget.h"

/**
 * PanelFrameHeaderBar:
 *
 * A header bar for #PanelFrame. It can optionally show an icon, it
 * can have a popover to be displace, and it can also have prefix and
 * suffix widgets.
 *
 * It is an implementation of #PanelFrameHeader
 */
struct _PanelFrameHeaderBar
{
  GtkWidget          parent_instance;

  GBindingGroup     *bindings;
  PanelFrame        *frame;
  GMenuModel        *menu_model;
  PanelWidget       *visible_child;
  PanelJoinedMenu   *joined_menu;

  GMenuModel        *frame_menu;
  GtkBox            *box;
  GtkBox            *start_area;
  GtkBox            *end_area;
  GtkBox            *controls;
  GtkMenuButton     *menu_button;
  GtkPopover        *pages_popover;
  GtkListView       *list_view;
  GtkMenuButton     *title_button;
  GtkLabel          *title;
  GtkLabel          *modified;
  GtkImage          *image;
  GtkButton         *drag_button;

  PanelWidget       *drag_panel;
  GtkWidget         *drag_dock;

  guint              show_icon : 1;
};

static void frame_header_iface_init (PanelFrameHeaderInterface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelFrameHeaderBar, panel_frame_header_bar, GTK_TYPE_WIDGET,
                         G_IMPLEMENT_INTERFACE (PANEL_TYPE_FRAME_HEADER, frame_header_iface_init))

enum {
  PROP_0,
  PROP_SHOW_ICON,
  N_PROPS,

  PROP_FRAME,
};

static GParamSpec *properties [N_PROPS];

/**
 * panel_frame_header_bar_new:
 *
 * Create a new #PanelFrameHeaderBar.
 *
 * Returns: a newly created #PanelFrameHeaderBar
 */
GtkWidget *
panel_frame_header_bar_new (void)
{
  return g_object_new (PANEL_TYPE_FRAME_HEADER_BAR, NULL);
}

static gboolean
boolean_to_modified (GBinding     *binding,
                     const GValue *from_value,
                     GValue       *to_value,
                     gpointer      user_data)
{
  if (g_value_get_boolean (from_value))
    g_value_set_static_string (to_value, "•");
  else
    g_value_set_static_string (to_value, "");

  return TRUE;
}

static void
setup_row_cb (GtkSignalListItemFactory *factory,
              GtkListItem              *list_item,
              PanelFrameHeaderBar      *self)
{
  GtkWidget *child;

  g_assert (GTK_IS_SIGNAL_LIST_ITEM_FACTORY (factory));
  g_assert (GTK_IS_LIST_ITEM (list_item));
  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));

  child = panel_frame_header_bar_row_new ();

  gtk_list_item_set_child (list_item, child);
}


static void
bind_row_cb (GtkSignalListItemFactory *factory,
             GtkListItem              *list_item,
             PanelFrameHeaderBar      *self)
{
  AdwTabPage *item;
  GtkWidget *row;

  g_assert (GTK_IS_SIGNAL_LIST_ITEM_FACTORY (factory));
  g_assert (GTK_IS_LIST_ITEM (list_item));
  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));

  item = gtk_list_item_get_item (list_item);
  row = gtk_list_item_get_child (list_item);

  g_assert (ADW_IS_TAB_PAGE (item));
  g_assert (PANEL_IS_FRAME_HEADER_BAR_ROW (row));

  panel_frame_header_bar_row_set_page (PANEL_FRAME_HEADER_BAR_ROW (row), item);
}

static void
unbind_row_cb (GtkSignalListItemFactory *factory,
               GtkListItem              *list_item,
               PanelFrameHeaderBar      *self)
{
  GtkWidget *row;

  g_assert (GTK_IS_SIGNAL_LIST_ITEM_FACTORY (factory));
  g_assert (GTK_IS_LIST_ITEM (list_item));
  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));

  row = gtk_list_item_get_child (list_item);
  panel_frame_header_bar_row_set_page (PANEL_FRAME_HEADER_BAR_ROW (row), NULL);
}

static void
panel_frame_header_bar_set_frame (PanelFrameHeaderBar *self,
                                  PanelFrame          *frame)
{
  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));
  g_assert (!frame || PANEL_IS_FRAME (frame));

  if (self->frame == frame)
    return;

  if (self->frame)
    {
      gtk_list_view_set_model (self->list_view, NULL);
      g_clear_object (&self->frame);
    }

  g_set_object (&self->frame, frame);

  if (self->frame)
    {
      GtkSelectionModel *pages = panel_frame_get_pages (self->frame);
      gtk_list_view_set_model (self->list_view, pages);
      g_clear_object (&pages);
    }

  g_object_notify (G_OBJECT (self), "frame");
}

static void
menu_clicked_cb (GtkGesture          *gesture,
                 int                  n_press,
                 double               x,
                 double               y,
                 PanelFrameHeaderBar *self)
{
  g_assert (GTK_IS_GESTURE_CLICK (gesture));
  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));

  if (self->frame)
    {
      GMenuModel *menu_model = _panel_frame_get_tab_menu (self->frame);
      gtk_menu_button_set_menu_model (self->menu_button, menu_model);
    }
}

#define MAX_WIDTH  250.0
#define MAX_HEIGHT 250.0

static GdkContentProvider *
drag_prepare_cb (PanelFrameHeaderBar *self,
                 double               x,
                 double               y,
                 GtkDragSource       *drag_source)
{
  PanelWidget *visible_child;

  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));
  g_assert (GTK_IS_DRAG_SOURCE (drag_source));

  if (self->frame == NULL ||
      !(visible_child = panel_frame_get_visible_child (self->frame)) ||
      !PANEL_IS_WIDGET (visible_child) ||
      !panel_widget_get_reorderable (visible_child))
    return NULL;

  self->drag_panel = visible_child;

  return gdk_content_provider_new_typed (PANEL_TYPE_WIDGET, visible_child);
}

static void
drag_begin_cb (PanelFrameHeaderBar *self,
               GdkDrag             *drag,
               GtkDragSource       *drag_source)
{
  GdkPaintable *paintable = NULL;
  GtkWidget *dock;

  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));
  g_assert (GDK_IS_DRAG (drag));
  g_assert (GTK_IS_DRAG_SOURCE (drag_source));

  if ((paintable = gtk_widget_paintable_new (GTK_WIDGET (self->drag_panel))))
    {
      int width = gdk_paintable_get_intrinsic_width (paintable);
      int height = gdk_paintable_get_intrinsic_height (paintable);
      double ratio;

      if (width <= MAX_WIDTH && height <= MAX_HEIGHT)
        ratio = 1.0;
      else if (width > height)
        ratio = width / MAX_WIDTH;
      else
        ratio = height / MAX_HEIGHT;

      if (ratio != 1.0)
        {
          GdkPaintable *tmp = paintable;
          paintable = panel_scaler_new (paintable, ratio);
          g_clear_object (&tmp);
        }
    }
  else
    {
      GtkIconTheme *icon_theme;
      const char *icon_name;
      int scale;

      icon_theme = gtk_icon_theme_get_for_display (gtk_widget_get_display (GTK_WIDGET (self)));
      icon_name = panel_widget_get_icon_name (PANEL_WIDGET (self->drag_panel));
      scale = gtk_widget_get_scale_factor (GTK_WIDGET (self));

      if (icon_name)
        paintable = GDK_PAINTABLE (gtk_icon_theme_lookup_icon (icon_theme, icon_name, NULL, 32, scale, GTK_TEXT_DIR_NONE,  0));
    }

  if (paintable != NULL)
    gtk_drag_source_set_icon (drag_source, paintable, 0, 0);

  if ((dock = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_DOCK)))
    {
      _panel_dock_begin_drag (PANEL_DOCK (dock), PANEL_WIDGET (self->drag_panel));
      g_set_weak_pointer (&self->drag_dock, dock);
    }

  g_clear_object (&paintable);
}

static void
drag_end_cb (PanelFrameHeaderBar *self,
             GdkDrag             *drag,
             gboolean             delete_data,
             GtkDragSource       *drag_source)
{
  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));
  g_assert (GDK_IS_DRAG (drag));
  g_assert (GTK_IS_DRAG_SOURCE (drag_source));

  if (self->drag_dock)
    _panel_dock_end_drag (PANEL_DOCK (self->drag_dock), PANEL_WIDGET (self->drag_panel));

  self->drag_panel = NULL;
  g_clear_weak_pointer (&self->drag_dock);
}

static void
panel_frame_header_bar_dispose (GObject *object)
{
  PanelFrameHeaderBar *self = (PanelFrameHeaderBar *)object;

  panel_frame_header_bar_set_frame (self, NULL);

  g_clear_pointer ((GtkWidget **)&self->box, gtk_widget_unparent);

  g_clear_object (&self->visible_child);
  g_clear_object (&self->frame);
  g_clear_object (&self->menu_model);
  g_clear_object (&self->bindings);
  g_clear_object (&self->joined_menu);

  G_OBJECT_CLASS (panel_frame_header_bar_parent_class)->dispose (object);
}

static void
panel_frame_header_bar_get_property (GObject    *object,
                                     guint       prop_id,
                                     GValue     *value,
                                     GParamSpec *pspec)
{
  PanelFrameHeaderBar *self = PANEL_FRAME_HEADER_BAR (object);

  switch (prop_id)
    {
    case PROP_FRAME:
      g_value_set_object (value, self->frame);
      break;

    case PROP_SHOW_ICON:
      g_value_set_boolean (value, panel_frame_header_bar_get_show_icon (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_frame_header_bar_set_property (GObject      *object,
                                     guint         prop_id,
                                     const GValue *value,
                                     GParamSpec   *pspec)
{
  PanelFrameHeaderBar *self = PANEL_FRAME_HEADER_BAR (object);

  switch (prop_id)
    {
    case PROP_FRAME:
      panel_frame_header_bar_set_frame (self, g_value_get_object (value));
      break;

    case PROP_SHOW_ICON:
      panel_frame_header_bar_set_show_icon (self, g_value_get_boolean (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_frame_header_bar_class_init (PanelFrameHeaderBarClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_frame_header_bar_dispose;
  object_class->get_property = panel_frame_header_bar_get_property;
  object_class->set_property = panel_frame_header_bar_set_property;

  /**
   * PanelFrameHeaderBar:show-icon:
   *
   * Whether to show the icon or not.
   */
  properties [PROP_SHOW_ICON] =
    g_param_spec_boolean ("show-icon",
                          "Show Icon",
                          "Show Icon",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_override_property (object_class, PROP_FRAME, "frame");
  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_template_from_resource (widget_class, "/org/gnome/libpanel/panel-frame-header-bar.ui");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
  gtk_widget_class_set_css_name (widget_class, "panelframeheaderbar");
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, box);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, controls);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, drag_button);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, end_area);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, list_view);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, menu_button);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, pages_popover);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, start_area);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBar, title_button);
  gtk_widget_class_bind_template_callback (widget_class, setup_row_cb);
  gtk_widget_class_bind_template_callback (widget_class, bind_row_cb);
  gtk_widget_class_bind_template_callback (widget_class, unbind_row_cb);
  gtk_widget_class_bind_template_callback (widget_class, menu_clicked_cb);
  gtk_widget_class_bind_template_callback (widget_class, drag_begin_cb);
  gtk_widget_class_bind_template_callback (widget_class, drag_end_cb);
  gtk_widget_class_bind_template_callback (widget_class, drag_prepare_cb);
}

static void
panel_frame_header_bar_init (PanelFrameHeaderBar *self)
{
  GtkWidget *button;
  GtkWidget *box;

  gtk_widget_init_template (GTK_WIDGET (self));

  gtk_widget_set_cursor_from_name (GTK_WIDGET (self->drag_button), "grab");

  /* Because GtkMenuButton does not allow us to specify children within
   * the label, we have to dive into it and modify it directly.
   */
  box = gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 6);
  gtk_widget_set_halign (box, GTK_ALIGN_START);
  self->modified = g_object_new (GTK_TYPE_LABEL,
                                 "valign", GTK_ALIGN_BASELINE,
                                 "xalign", 0.0f,
                                 "single-line-mode", TRUE,
                                 "width-chars", 1,
                                 "max-width-chars", 1,
                                 NULL);
  self->image = GTK_IMAGE (gtk_image_new ());
  gtk_widget_set_valign (GTK_WIDGET (self->image), GTK_ALIGN_BASELINE);
  g_object_bind_property (self, "show-icon", self->image, "visible", G_BINDING_SYNC_CREATE);
  self->title = g_object_new (GTK_TYPE_LABEL,
                              "valign", GTK_ALIGN_BASELINE,
                              "xalign", 0.0f,
                              "ellipsize", PANGO_ELLIPSIZE_MIDDLE,
                              "width-chars", 5,
                              NULL);
  gtk_box_append (GTK_BOX (box), GTK_WIDGET (self->image));
  gtk_box_append (GTK_BOX (box), GTK_WIDGET (self->title));
  gtk_box_append (GTK_BOX (box), GTK_WIDGET (self->modified));
  button = gtk_widget_get_first_child (GTK_WIDGET (self->title_button));
  gtk_button_set_child (GTK_BUTTON (button), box);

  self->bindings = g_binding_group_new ();
  g_binding_group_bind (self->bindings, "title", self->title, "label", 0);
  g_binding_group_bind (self->bindings, "tooltip", self->title_button, "tooltip-text", 0);
  g_binding_group_bind_full (self->bindings, "modified",
                             self->modified, "label",
                             0, boolean_to_modified, NULL, NULL, NULL);
  g_binding_group_bind (self->bindings, "icon", self->image, "gicon", 0);
}

static gboolean
panel_frame_header_bar_can_drop (PanelFrameHeader *header,
                                 PanelWidget      *widget)
{
  const char *kind;

  g_assert (PANEL_IS_FRAME_HEADER_BAR (header));
  g_assert (PANEL_IS_WIDGET (widget));

  kind = panel_widget_get_kind (widget);

  return g_strcmp0 (kind, PANEL_WIDGET_KIND_DOCUMENT) == 0;
}

static void
panel_frame_header_bar_page_changed (PanelFrameHeader *header,
                                     PanelWidget      *page)
{
  PanelFrameHeaderBar *self = (PanelFrameHeaderBar *)header;

  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));
  g_assert (!page || PANEL_IS_WIDGET (page));

  if (page == NULL)
    {
      gtk_label_set_label (self->title, NULL);
      gtk_widget_set_tooltip_text (GTK_WIDGET (self->title_button), NULL);
      gtk_label_set_attributes (self->title, NULL);
      gtk_widget_hide (GTK_WIDGET (self->modified));
      gtk_image_clear (self->image);
      gtk_menu_button_popdown (self->title_button);
    }

  gtk_widget_set_sensitive (GTK_WIDGET (self->menu_button), page != NULL);
  gtk_widget_set_sensitive (GTK_WIDGET (self->drag_button), page != NULL);

  g_binding_group_set_source (self->bindings, page);

  gtk_widget_set_sensitive (GTK_WIDGET (self->title_button), page != NULL);

  if (self->frame)
    {
      GMenuModel *menu_model = _panel_frame_get_tab_menu (self->frame);
      gtk_menu_button_set_menu_model (self->menu_button, menu_model);
    }
}

#define GET_PRIORITY(w)   GPOINTER_TO_INT(g_object_get_data(G_OBJECT(w),"PRIORITY"))
#define SET_PRIORITY(w,i) g_object_set_data(G_OBJECT(w),"PRIORITY",GINT_TO_POINTER(i))

static void
panel_frame_header_bar_add_prefix (PanelFrameHeader *header,
                                   int               priority,
                                   GtkWidget        *widget)
{
  PanelFrameHeaderBar *self = (PanelFrameHeaderBar *)header;
  GtkWidget *sibling = NULL;

  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));

  SET_PRIORITY (widget, priority);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self->start_area));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (priority < GET_PRIORITY(child))
        break;
      sibling = child;
    }

  gtk_box_insert_child_after (self->start_area, widget, sibling);
}

static void
panel_frame_header_bar_add_suffix (PanelFrameHeader *header,
                                   int               priority,
                                   GtkWidget        *widget)
{
  PanelFrameHeaderBar *self = (PanelFrameHeaderBar *)header;
  GtkWidget *sibling = NULL;

  g_assert (PANEL_IS_FRAME_HEADER_BAR (self));

  SET_PRIORITY (widget, priority);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self->end_area));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (priority < GET_PRIORITY(child))
        break;
      sibling = child;
    }

  gtk_box_insert_child_after (self->end_area, widget, sibling);
}

static void
frame_header_iface_init (PanelFrameHeaderInterface *iface)
{
  iface->can_drop = panel_frame_header_bar_can_drop;
  iface->page_changed = panel_frame_header_bar_page_changed;
  iface->add_prefix = panel_frame_header_bar_add_prefix;
  iface->add_suffix = panel_frame_header_bar_add_suffix;
}

/**
 * panel_frame_header_bar_get_menu_popover:
 * @self: a #PanelFrameHeaderBar
 *
 * Gets the menu popover attached to this menubar.
 *
 * Returns: (transfer none): a #GtkPopoverMenu
 */
GtkPopoverMenu *
panel_frame_header_bar_get_menu_popover (PanelFrameHeaderBar *self)
{
  g_return_val_if_fail (PANEL_IS_FRAME_HEADER_BAR (self), NULL);

  return GTK_POPOVER_MENU (gtk_menu_button_get_popover (self->menu_button));
}

/**
 * panel_frame_header_bar_get_show_icon:
 * @self: a #PanelFrameHeaderBar
 *
 * Tell whether it show the icon or not.
 *
 * Returns: whether to show the icon.
 */
gboolean
panel_frame_header_bar_get_show_icon (PanelFrameHeaderBar *self)
{
  g_return_val_if_fail (PANEL_IS_FRAME_HEADER_BAR (self), FALSE);

  return self->show_icon;
}

/**
 * panel_frame_header_bar_set_show_icon:
 * @self: a #PanelFrameHeaderBar
 * @show_icon: whether to show the icon
 *
 * Set whether to show the icon or not.
 */
void
panel_frame_header_bar_set_show_icon (PanelFrameHeaderBar *self,
                                      gboolean             show_icon)
{
  g_return_if_fail (PANEL_IS_FRAME_HEADER_BAR (self));

  show_icon = !!show_icon;

  if (show_icon != self->show_icon)
    {
      self->show_icon = show_icon;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_SHOW_ICON]);
    }
}
