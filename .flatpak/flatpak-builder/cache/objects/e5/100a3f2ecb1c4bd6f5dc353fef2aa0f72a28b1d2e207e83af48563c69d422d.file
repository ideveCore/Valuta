/* panel-frame-header-bar-row.c
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

#include "panel-frame-private.h"
#include "panel-frame-header-bar-row-private.h"

struct _PanelFrameHeaderBarRow
{
  GtkWidget   parent_instance;

  AdwTabPage *page;

  GtkBox     *box;
  GtkLabel   *label;
  GtkImage   *image;
};

G_DEFINE_TYPE (PanelFrameHeaderBarRow, panel_frame_header_bar_row, GTK_TYPE_WIDGET)

enum {
  PROP_0,
  PROP_PAGE,
  PROP_SHOW_ICON,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

/**
 * panel_frame_header_bar_row_new:
 *
 * Create a new #PanelFrameHeaderBarRow.
 *
 * Returns: a newly created #PanelFrameHeaderBarRow
 */
GtkWidget *
panel_frame_header_bar_row_new (void)
{
  return g_object_new (PANEL_TYPE_FRAME_HEADER_BAR_ROW, NULL);
}

static void
page_close_action (GtkWidget  *widget,
                   const char *action_name,
                   GVariant   *param)
{
  PanelFrameHeaderBarRow *self = (PanelFrameHeaderBarRow *)widget;
  AdwTabView *tab_view;
  GtkWidget *frame;

  g_assert (PANEL_FRAME_HEADER_BAR_ROW (self));

  if (self->page != NULL &&
      (frame = gtk_widget_get_ancestor (widget, PANEL_TYPE_FRAME)) &&
      (tab_view = _panel_frame_get_tab_view (PANEL_FRAME (frame))))
    adw_tab_view_close_page (tab_view, self->page);
}

static void
panel_frame_header_bar_row_dispose (GObject *object)
{
  PanelFrameHeaderBarRow *self = (PanelFrameHeaderBarRow *)object;

  g_clear_object (&self->page);
  g_clear_pointer ((GtkWidget **)&self->box, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_frame_header_bar_row_parent_class)->dispose (object);
}

static void
panel_frame_header_bar_row_get_property (GObject    *object,
                                         guint       prop_id,
                                         GValue     *value,
                                         GParamSpec *pspec)
{
  PanelFrameHeaderBarRow *self = PANEL_FRAME_HEADER_BAR_ROW (object);

  switch (prop_id)
    {
    case PROP_PAGE:
      g_value_set_object (value, panel_frame_header_bar_row_get_page (self));
      break;

    case PROP_SHOW_ICON:
      g_value_set_boolean (value, gtk_widget_get_visible (GTK_WIDGET (self->image)));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_frame_header_bar_row_set_property (GObject      *object,
                                         guint         prop_id,
                                         const GValue *value,
                                         GParamSpec   *pspec)
{
  PanelFrameHeaderBarRow *self = PANEL_FRAME_HEADER_BAR_ROW (object);

  switch (prop_id)
    {
    case PROP_PAGE:
      panel_frame_header_bar_row_set_page (self, g_value_get_object (value));
      break;

    case PROP_SHOW_ICON:
      gtk_widget_set_visible (GTK_WIDGET (self->image), g_value_get_boolean (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_frame_header_bar_row_class_init (PanelFrameHeaderBarRowClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_frame_header_bar_row_dispose;
  object_class->get_property = panel_frame_header_bar_row_get_property;
  object_class->set_property = panel_frame_header_bar_row_set_property;

  properties [PROP_PAGE] =
    g_param_spec_object ("page",
                         "Page",
                         "Page",
                         ADW_TYPE_TAB_PAGE,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_SHOW_ICON] =
    g_param_spec_boolean ("show-icon",
                          "Show Icon",
                          "Show Icon",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_template_from_resource (widget_class, "/org/gnome/libpanel/panel-frame-header-bar-row.ui");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBarRow, box);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBarRow, image);
  gtk_widget_class_bind_template_child (widget_class, PanelFrameHeaderBarRow, label);

  gtk_widget_class_install_action (widget_class, "page.close", NULL, page_close_action);
}

static void
panel_frame_header_bar_row_init (PanelFrameHeaderBarRow *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));
}

static void
panel_frame_header_bar_row_notify_cb (PanelFrameHeaderBarRow *self,
                                      GParamSpec             *pspec,
                                      AdwTabPage             *page)
{
  g_assert (PANEL_IS_FRAME_HEADER_BAR_ROW (self));
  g_assert (ADW_IS_TAB_PAGE (page));

  gtk_image_set_from_gicon (self->image, adw_tab_page_get_icon (page));
  gtk_label_set_label (self->label, adw_tab_page_get_title (page));

  if (adw_tab_page_get_needs_attention (page))
    gtk_widget_add_css_class (GTK_WIDGET (self), "needs-attention");
  else
    gtk_widget_remove_css_class (GTK_WIDGET (self), "needs-attention");
}

AdwTabPage *
panel_frame_header_bar_row_get_page (PanelFrameHeaderBarRow *self)
{
  g_return_val_if_fail (PANEL_IS_FRAME_HEADER_BAR_ROW (self), NULL);

  return self->page;
}

void
panel_frame_header_bar_row_set_page (PanelFrameHeaderBarRow *self,
                                     AdwTabPage             *page)
{
  g_return_if_fail (PANEL_IS_FRAME_HEADER_BAR_ROW (self));
  g_return_if_fail (!page || ADW_IS_TAB_PAGE (page));

  if (page == self->page)
    return;

  if (self->page)
    g_signal_handlers_disconnect_by_func (self->page,
                                          G_CALLBACK (panel_frame_header_bar_row_notify_cb),
                                          self);

  g_set_object (&self->page, page);

  if (self->page)
    {
      g_signal_connect_object (self->page,
                               "notify",
                               G_CALLBACK (panel_frame_header_bar_row_notify_cb),
                               self,
                               G_CONNECT_SWAPPED);
      panel_frame_header_bar_row_notify_cb (self, NULL, self->page);
    }

  g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_PAGE]);
}
