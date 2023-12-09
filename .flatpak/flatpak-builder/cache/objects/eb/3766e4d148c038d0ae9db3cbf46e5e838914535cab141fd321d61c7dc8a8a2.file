/* panel-frame-tab-bar.c
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

#include <adwaita.h>

#include "panel-frame-header.h"
#include "panel-frame-private.h"
#include "panel-frame-switcher.h"
#include "panel-frame-tab-bar.h"
#include "panel-widget.h"

/**
 * PanelFrameTabBar:
 *
 * A #PanelFrameHeader that implements switching between tab views in
 * a #PanelFrame.
 */
struct _PanelFrameTabBar
{
  GtkWidget          parent_instance;

  GtkSelectionModel *pages;
  PanelFrame        *frame;

  GtkOverlay        *overlay;
  AdwTabBar         *tab_bar;
  GtkBox            *start_area;
  GtkBox            *end_area;
  GtkMenuButton     *menu_button;
  GtkButton         *close_button;
};

static void frame_header_iface_init (PanelFrameHeaderInterface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelFrameTabBar, panel_frame_tab_bar, GTK_TYPE_WIDGET,
                         G_IMPLEMENT_INTERFACE (PANEL_TYPE_FRAME_HEADER, frame_header_iface_init))

enum {
  PROP_0,
  PROP_AUTOHIDE,
  PROP_INVERTED,
  PROP_EXPAND_TABS,
  N_PROPS,

  PROP_FRAME,
};

/**
 * panel_frame_tab_bar_new:
 *
 * Create a new #PanelFrameTabBar.
 *
 * Returns: a newly created #PanelFrameTabBar
 */
GtkWidget *
panel_frame_tab_bar_new (void)
{
  return g_object_new (PANEL_TYPE_FRAME_TAB_BAR, NULL);
}

static void
on_notify_closeable_cb (PanelFrameTabBar *self,
                        GParamSpec       *pspec,
                        PanelFrame       *frame)
{
  g_assert (PANEL_IS_FRAME_TAB_BAR (self));
  g_assert (PANEL_IS_FRAME (frame));

  gtk_widget_set_visible (GTK_WIDGET (self->close_button),
                          panel_frame_get_closeable (frame));
}

static void
panel_frame_tab_bar_set_frame (PanelFrameTabBar *self,
                               PanelFrame       *frame)
{
  g_assert (PANEL_IS_FRAME_TAB_BAR (self));
  g_assert (!frame || PANEL_IS_FRAME (frame));

  if (self->frame == frame)
    return;

  if (self->frame)
    {
      g_signal_handlers_disconnect_by_func (self->frame,
                                            G_CALLBACK (on_notify_closeable_cb),
                                            self);
      adw_tab_bar_set_view (self->tab_bar, NULL);
      gtk_menu_button_set_menu_model (self->menu_button, NULL);
      g_clear_object (&self->frame);
    }

  g_set_object (&self->frame, frame);
  g_clear_object (&self->pages);

  if (self->frame)
    {
      AdwTabView *tab_view = _panel_frame_get_tab_view (self->frame);
      GMenuModel *menu_model = _panel_frame_get_tab_menu (self->frame);

      g_signal_connect_object (self->frame,
                               "notify::closeable",
                               G_CALLBACK (on_notify_closeable_cb),
                               self,
                               G_CONNECT_SWAPPED);

      self->pages = adw_tab_view_get_pages (tab_view);
      gtk_menu_button_set_menu_model (self->menu_button, menu_model);
      adw_tab_bar_set_view (self->tab_bar, tab_view);

      on_notify_closeable_cb (self, NULL, self->frame);
    }

  g_object_notify (G_OBJECT (self), "frame");
}

static void
panel_frame_tab_bar_notify_cb (PanelFrameTabBar *self,
                               GParamSpec       *pspec,
                               AdwTabBar        *tab_bar)
{
  GParamSpec *relative;

  g_assert (PANEL_IS_FRAME_TAB_BAR (self));
  g_assert (pspec != NULL);
  g_assert (ADW_IS_TAB_BAR (tab_bar));

  if ((relative = g_object_class_find_property (G_OBJECT_GET_CLASS (self), pspec->name)))
    {
      g_object_notify_by_pspec (G_OBJECT (self), relative);
      return;
    }
}

static void
menu_clicked_cb (GtkGesture       *gesture,
                 int               n_press,
                 double            x,
                 double            y,
                 PanelFrameTabBar *self)
{
  g_assert (GTK_IS_GESTURE_CLICK (gesture));
  g_assert (PANEL_IS_FRAME_TAB_BAR (self));

  if (self->frame)
    {
      GMenuModel *menu_model = _panel_frame_get_tab_menu (self->frame);
      gtk_menu_button_set_menu_model (self->menu_button, menu_model);
    }
}

static void
panel_frame_tab_bar_dispose (GObject *object)
{
  PanelFrameTabBar *self = (PanelFrameTabBar *)object;
  GtkWidget *child;

  panel_frame_tab_bar_set_frame (self, NULL);

  g_assert (self->frame == NULL);
  g_assert (self->pages == NULL);

  self->tab_bar = NULL;
  self->start_area = NULL;
  self->end_area = NULL;

  while ((child = gtk_widget_get_first_child (GTK_WIDGET (self))))
    gtk_widget_unparent (child);

  G_OBJECT_CLASS (panel_frame_tab_bar_parent_class)->dispose (object);
}

static void
panel_frame_tab_bar_get_property (GObject    *object,
                                  guint       prop_id,
                                  GValue     *value,
                                  GParamSpec *pspec)
{
  PanelFrameTabBar *self = PANEL_FRAME_TAB_BAR (object);

  switch (prop_id)
    {
    case PROP_FRAME:
      g_value_set_object (value, self->frame);
      break;

#define WRAP_BOOLEAN_PROPERTY(PROP, name) \
  case PROP: \
    g_value_set_boolean (value, adw_tab_bar_get_##name (self->tab_bar)); \
    break

    /**
     * PanelFrameTabBar:autohide:
     *
     * Whether the tabs automatically hide.
     */
    WRAP_BOOLEAN_PROPERTY (PROP_AUTOHIDE, autohide);
    /**
     * PanelFrameTabBar:expand-tabs:
     *
     * Whether tabs expand to full width.
     */
    WRAP_BOOLEAN_PROPERTY (PROP_EXPAND_TABS, expand_tabs);
    /**
     * PanelFrameTabBar:inverted:
     *
     * Whether tabs use inverted layout.
     */
    WRAP_BOOLEAN_PROPERTY (PROP_INVERTED, inverted);

#undef WRAP_BOOLEAN_PROPERTY

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_frame_tab_bar_set_property (GObject      *object,
                                  guint         prop_id,
                                  const GValue *value,
                                  GParamSpec   *pspec)
{
  PanelFrameTabBar *self = PANEL_FRAME_TAB_BAR (object);

  switch (prop_id)
    {
    case PROP_FRAME:
      panel_frame_tab_bar_set_frame (self, g_value_get_object (value));
      break;

#define WRAP_BOOLEAN_PROPERTY(PROP, name) \
  case PROP: \
    adw_tab_bar_set_##name (self->tab_bar, g_value_get_boolean (value)); \
    break

    WRAP_BOOLEAN_PROPERTY (PROP_AUTOHIDE, autohide);
    WRAP_BOOLEAN_PROPERTY (PROP_EXPAND_TABS, expand_tabs);
    WRAP_BOOLEAN_PROPERTY (PROP_INVERTED, inverted);

#undef WRAP_BOOLEAN_PROPERTY

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_frame_tab_bar_class_init (PanelFrameTabBarClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_frame_tab_bar_dispose;
  object_class->get_property = panel_frame_tab_bar_get_property;
  object_class->set_property = panel_frame_tab_bar_set_property;

#define WRAP_BOOLEAN_PROPERTY(PROP, name, Name, Default) \
  g_object_class_install_property (object_class, \
                                   PROP, \
                                   g_param_spec_boolean (name, \
                                                         Name, \
                                                         Name, \
                                                         Default, \
                                                         (G_PARAM_READWRITE | \
                                                          G_PARAM_STATIC_STRINGS | \
                                                          G_PARAM_EXPLICIT_NOTIFY)))
  WRAP_BOOLEAN_PROPERTY (PROP_AUTOHIDE, "autohide", "Autohide", FALSE);
  WRAP_BOOLEAN_PROPERTY (PROP_EXPAND_TABS, "expand-tabs", "Expand Tabs", TRUE);
  WRAP_BOOLEAN_PROPERTY (PROP_INVERTED, "inverted", "Inverted", FALSE);
#undef WRAP_BOOLEAN_PROPERTY

  g_object_class_override_property (object_class, PROP_FRAME, "frame");

  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
  gtk_widget_class_set_css_name (widget_class, "panelframetabbar");
}

static void
panel_frame_tab_bar_init (PanelFrameTabBar *self)
{
  GtkEventController *controller;
  GtkWidget *box;

  self->overlay = GTK_OVERLAY (gtk_overlay_new ());
  gtk_widget_set_parent (GTK_WIDGET (self->overlay), GTK_WIDGET (self));

  box = gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0);
  gtk_widget_set_valign (box, GTK_ALIGN_START);
  gtk_widget_set_hexpand (box, TRUE);
  gtk_overlay_add_overlay (self->overlay, box);
  gtk_widget_add_css_class (box, "focus-handle");

  self->tab_bar = ADW_TAB_BAR (adw_tab_bar_new ());
  gtk_widget_add_css_class (GTK_WIDGET (self->tab_bar), "inline");
  adw_tab_bar_set_autohide (self->tab_bar, FALSE);
  g_signal_connect_object (self->tab_bar,
                           "notify",
                           G_CALLBACK (panel_frame_tab_bar_notify_cb),
                           self,
                           G_CONNECT_SWAPPED);
  gtk_overlay_set_child (self->overlay, GTK_WIDGET (self->tab_bar));

  self->start_area = GTK_BOX (gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0));
  adw_tab_bar_set_start_action_widget (self->tab_bar, GTK_WIDGET (self->start_area));

  self->end_area = GTK_BOX (gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0));
  adw_tab_bar_set_end_action_widget (self->tab_bar, GTK_WIDGET (self->end_area));

  self->menu_button = g_object_new (GTK_TYPE_MENU_BUTTON,
                                    "css-classes", (const char * const[]) { "flat", NULL },
                                    "icon-name", "pan-down-symbolic",
                                    "valign", GTK_ALIGN_CENTER,
                                    NULL);
  gtk_box_append (self->end_area, GTK_WIDGET (self->menu_button));

  self->close_button = g_object_new (GTK_TYPE_BUTTON,
                                     "action-name", "frame.close",
                                     "css-classes", (const char * const[]) { "flat", "circular", "frame-close-button", NULL },
                                     "icon-name", "window-close-symbolic",
                                     "valign", GTK_ALIGN_CENTER,
                                     NULL);
  gtk_box_append (self->end_area, GTK_WIDGET (self->close_button));

  controller = GTK_EVENT_CONTROLLER (gtk_gesture_click_new ());
  g_signal_connect_object (controller, "pressed",
                           G_CALLBACK (menu_clicked_cb), self, 0);
  gtk_widget_add_controller (GTK_WIDGET (self), controller);
}

static gboolean
panel_frame_tab_bar_can_drop (PanelFrameHeader *header,
                              PanelWidget      *widget)
{
  const char *kind;

  g_assert (PANEL_IS_FRAME_TAB_BAR (header));
  g_assert (PANEL_IS_WIDGET (widget));

  kind = panel_widget_get_kind (widget);

  return g_strcmp0 (kind, PANEL_WIDGET_KIND_DOCUMENT) == 0;
}

#define GET_PRIORITY(w)   GPOINTER_TO_INT(g_object_get_data(G_OBJECT(w),"PRIORITY"))
#define SET_PRIORITY(w,i) g_object_set_data(G_OBJECT(w),"PRIORITY",GINT_TO_POINTER(i))

static void
panel_frame_tab_bar_add_prefix (PanelFrameHeader *header,
                                int               priority,
                                GtkWidget        *widget)
{
  PanelFrameTabBar *self = (PanelFrameTabBar *)header;
  GtkWidget *sibling = NULL;

  g_assert (PANEL_IS_FRAME_TAB_BAR (self));

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
panel_frame_tab_bar_add_suffix (PanelFrameHeader *header,
                                int               priority,
                                GtkWidget        *widget)
{
  PanelFrameTabBar *self = (PanelFrameTabBar *)header;
  GtkWidget *sibling = NULL;

  g_assert (PANEL_IS_FRAME_TAB_BAR (self));

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
  iface->can_drop = panel_frame_tab_bar_can_drop;
  iface->add_prefix = panel_frame_tab_bar_add_prefix;
  iface->add_suffix = panel_frame_tab_bar_add_suffix;
}

#define WRAP_BOOLEAN_PROPERTY(name) \
gboolean panel_frame_tab_bar_get_##name (PanelFrameTabBar *self) \
{ \
  g_return_val_if_fail (PANEL_IS_FRAME_TAB_BAR (self), FALSE); \
  return adw_tab_bar_get_##name (self->tab_bar); \
} \
void panel_frame_tab_bar_set_##name (PanelFrameTabBar *self, \
                                     gboolean          value) \
{ \
  g_return_if_fail (PANEL_IS_FRAME_TAB_BAR (self)); \
  adw_tab_bar_set_##name (self->tab_bar, value); \
}

/**
 * panel_frame_tab_bar_get_autohide:
 * @self: a #PanelFrameTabBar
 *
 * Gets whether the tabs automatically hide.
 *
 * Returns: the value of the autohide property.
 */
/**
 * panel_frame_tab_bar_set_autohide:
 * @self: a #PanelFrameTabBar
 * @autohide: the autohide value
 *
 * Sets whether the tabs automatically hide.
 */
  WRAP_BOOLEAN_PROPERTY (autohide);
/**
 * panel_frame_tab_bar_get_expand_tabs:
 * @self: a #PanelFrameTabBar
 *
 * Gets whether tabs expand to full width.
 *
 * Returns: the value of the expand_tabs property.
 */
/**
 * panel_frame_tab_bar_set_expand_tabs:
 * @self: a #PanelFrameTabBar
 * @expand_tabs: the expand_tabs value
 *
 * Sets whether tabs expand to full width.
 */
  WRAP_BOOLEAN_PROPERTY (expand_tabs);
/**
 * panel_frame_tab_bar_get_inverted:
 * @self: a #PanelFrameTabBar
 *
 * Gets whether tabs use inverted layout.
 *
 * Returns: the value of the inverted property.
 */
/**
 * panel_frame_tab_bar_set_inverted:
 * @self: a #PanelFrameTabBar
 * @inverted: the inverted value
 *
 * Sets whether tabs tabs use inverted layout.
 */
  WRAP_BOOLEAN_PROPERTY (inverted);

#undef WRAP_BOOLEAN_PROPERTY
