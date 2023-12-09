/* panel-maximized-controls.c
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

#include "panel-maximized-controls-private.h"

struct _PanelMaximizedControls
{
  GtkWidget  parent_instance;
  GtkBox    *box;
  GtkButton *close;
};

G_DEFINE_TYPE (PanelMaximizedControls, panel_maximized_controls, GTK_TYPE_WIDGET)

GtkWidget *
panel_maximized_controls_new (void)
{
  return g_object_new (PANEL_TYPE_MAXIMIZED_CONTROLS, NULL);
}

static void
panel_maximized_controls_dispose (GObject *object)
{
  PanelMaximizedControls *self = (PanelMaximizedControls *)object;

  g_clear_pointer ((GtkWidget **)&self->box, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_maximized_controls_parent_class)->dispose (object);
}

static void
panel_maximized_controls_class_init (PanelMaximizedControlsClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_maximized_controls_dispose;

  gtk_widget_class_set_css_name (widget_class, "panelmaximizedcontrols");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
}

static void
panel_maximized_controls_init (PanelMaximizedControls *self)
{
  self->box = GTK_BOX (gtk_box_new (GTK_ORIENTATION_HORIZONTAL, 0));
  gtk_widget_set_parent (GTK_WIDGET (self->box), GTK_WIDGET (self));

  self->close = GTK_BUTTON (gtk_button_new ());
  gtk_actionable_set_action_name (GTK_ACTIONABLE (self->close), "page.unmaximize");
  gtk_button_set_icon_name (self->close, "view-restore-symbolic");
  gtk_widget_set_tooltip_text (GTK_WIDGET (self->close), _("Restore panel to previous location"));
  gtk_widget_set_can_focus (GTK_WIDGET (self->close), TRUE);
  gtk_widget_set_margin_end (GTK_WIDGET (self->close), 12);
  gtk_widget_set_margin_top (GTK_WIDGET (self->close), 12);
  gtk_widget_add_css_class (GTK_WIDGET (self->close), "circular");
  gtk_widget_add_css_class (GTK_WIDGET (self->close), "close");
  gtk_box_append (self->box, GTK_WIDGET (self->close));
}
