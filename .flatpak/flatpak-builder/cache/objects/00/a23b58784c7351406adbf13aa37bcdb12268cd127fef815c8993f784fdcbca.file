/* panel-handle.c
 *
 * Copyright 2021 Christian Hergert <chergert@redhat.com>
 *
 * This file is free software; you can redistribute it and/or modify it under
 * the terms of the GNU Lesser General Public License as published by the Free
 * Software Foundation; either version 3 of the License, or (at your option)
 * any later version.
 *
 * This file is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
 * License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "config.h"

#include "panel-dock.h"
#include "panel-dock-child-private.h"
#include "panel-handle-private.h"

#define EXTRA_SIZE 8

struct _PanelHandle
{
  GtkWidget parent_instance;
  GtkWidget *separator;
  PanelArea  area : 4;
};

G_DEFINE_TYPE (PanelHandle, panel_handle, GTK_TYPE_WIDGET)

static gboolean
panel_handle_contains (GtkWidget *widget,
                       double     x,
                       double     y)
{
  PanelHandle *self = (PanelHandle *)widget;
  GtkWidget *dock_child;
  graphene_rect_t area;

  g_assert (PANEL_IS_HANDLE (self));

  /* Ignore when dragging */
  if ((dock_child = gtk_widget_get_ancestor (widget, PANEL_TYPE_DOCK_CHILD)) &&
      panel_dock_child_get_dragging (PANEL_DOCK_CHILD (dock_child)))
    return FALSE;

  if (!gtk_widget_compute_bounds (GTK_WIDGET (self->separator),
                                  GTK_WIDGET (self),
                                  &area))
      return FALSE;

  switch (self->area)
    {
    case PANEL_AREA_START:
      area.origin.x -= EXTRA_SIZE;
      area.size.width = EXTRA_SIZE;
      break;

    case PANEL_AREA_END:
      area.size.width = EXTRA_SIZE;
      break;

    case PANEL_AREA_TOP:
      area.origin.y -= EXTRA_SIZE;
      area.size.height = EXTRA_SIZE;
      break;

    case PANEL_AREA_BOTTOM:
      area.size.height = EXTRA_SIZE;
      break;

    case PANEL_AREA_CENTER:
    default:
      g_assert_not_reached ();
      break;
    }

  return graphene_rect_contains_point (&area, &GRAPHENE_POINT_INIT (x, y));
}

static void
panel_handle_dispose (GObject *object)
{
  PanelHandle *self = (PanelHandle *)object;

  g_clear_pointer (&self->separator, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_handle_parent_class)->dispose (object);
}

static void
panel_handle_class_init (PanelHandleClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_handle_dispose;

  widget_class->contains = panel_handle_contains;

  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
}

static void
panel_handle_init (PanelHandle *self)
{
  self->separator = gtk_separator_new (GTK_ORIENTATION_HORIZONTAL);
  gtk_widget_set_parent (GTK_WIDGET (self->separator), GTK_WIDGET (self));
}

void
panel_handle_set_area (PanelHandle *self,
                       PanelArea    area)
{
  g_return_if_fail (PANEL_IS_HANDLE (self));

  self->area = area;

  switch (area)
    {
    case PANEL_AREA_START:
    case PANEL_AREA_END:
      gtk_widget_set_cursor_from_name (GTK_WIDGET (self), "col-resize");
      gtk_orientable_set_orientation (GTK_ORIENTABLE (self->separator), GTK_ORIENTATION_VERTICAL);
      break;

    case PANEL_AREA_TOP:
    case PANEL_AREA_BOTTOM:
      gtk_widget_set_cursor_from_name (GTK_WIDGET (self), "row-resize");
      gtk_orientable_set_orientation (GTK_ORIENTABLE (self->separator), GTK_ORIENTATION_HORIZONTAL);
      break;

    case PANEL_AREA_CENTER:
    default:
      gtk_widget_set_cursor_from_name (GTK_WIDGET (self), "arrow");
      break;
    }
}

GtkWidget *
panel_handle_new (PanelArea area)
{
  PanelHandle *self;

  self = g_object_new (PANEL_TYPE_HANDLE, NULL);
  panel_handle_set_area (self, area);

  return GTK_WIDGET (self);
}
