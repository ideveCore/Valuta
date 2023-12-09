/* panel-grid-column.c
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

#include "panel-frame.h"
#include "panel-grid-private.h"
#include "panel-grid-column-private.h"
#include "panel-paned.h"
#include "panel-resizer-private.h"

struct _PanelGridColumn
{
  GtkWidget   parent_instance;
  PanelPaned *rows;
};

G_DEFINE_TYPE (PanelGridColumn, panel_grid_column, GTK_TYPE_WIDGET)

GtkWidget *
panel_grid_column_new (void)
{
  return g_object_new (PANEL_TYPE_GRID_COLUMN, NULL);
}

static void
panel_grid_column_dispose (GObject *object)
{
  PanelGridColumn *self = (PanelGridColumn *)object;

  g_clear_pointer ((GtkWidget **)&self->rows, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_grid_column_parent_class)->dispose (object);
}

static void
panel_grid_column_class_init (PanelGridColumnClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_grid_column_dispose;

  gtk_widget_class_set_css_name (widget_class, "panelgridcolumn");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
}

static void
panel_grid_column_init (PanelGridColumn *self)
{
  gtk_widget_set_hexpand (GTK_WIDGET (self), TRUE);

  self->rows = PANEL_PANED (panel_paned_new ());
  gtk_orientable_set_orientation (GTK_ORIENTABLE (self->rows), GTK_ORIENTATION_VERTICAL);
  gtk_widget_set_parent (GTK_WIDGET (self->rows), GTK_WIDGET (self));
}

gboolean
panel_grid_column_get_empty (PanelGridColumn *self)
{
  g_return_val_if_fail (PANEL_IS_GRID_COLUMN (self), FALSE);

  return panel_paned_get_n_children (self->rows) == 0;
}

/**
 * panel_grid_column_get_most_recent_frame:
 * @self: a #PanelGridColumn
 *
 * Gets the most recently acive frame on a grid column.
 *
 * Returns: (transfer none): a #PanelGridFrame
 */
PanelFrame *
panel_grid_column_get_most_recent_frame (PanelGridColumn *self)
{
  g_return_val_if_fail (PANEL_IS_GRID_COLUMN (self), NULL);

  /* TODO: Actually track with MRU */

  return panel_grid_column_get_row (self, 0);
}

/**
 * panel_grid_column_get_row:
 * @self: a #PanelGridColumn
 * @row: the index of the row
 *
 * Gets the frame corresponding to a row index.
 *
 * Returns: (transfer none): a #PanelGridFrame
 */
PanelFrame *
panel_grid_column_get_row (PanelGridColumn *self,
                           guint            row)
{
  PanelGrid *grid;
  GtkWidget *child;

  g_return_val_if_fail (PANEL_IS_GRID_COLUMN (self), NULL);

  if (!(grid = PANEL_GRID (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_GRID))))
    g_return_val_if_reached (NULL);

  while (panel_paned_get_n_children (self->rows) <= row)
    {
      PanelFrame *frame = _panel_grid_create_frame (grid);
      panel_paned_append (self->rows, GTK_WIDGET (frame));
    }

  child = panel_paned_get_nth_child (self->rows, row);
  g_return_val_if_fail (PANEL_IS_FRAME (child), NULL);
  return PANEL_FRAME (child);
}

guint
panel_grid_column_get_n_rows (PanelGridColumn *self)
{
  g_return_val_if_fail (PANEL_IS_GRID_COLUMN (self), 0);

  return panel_paned_get_n_children (self->rows);
}

/**
 * panel_grid_column_foreach_frame:
 * @self: a #PanelGridColumn
 * @callback: (not nullable) (scope call): a function to be called on each frame
 * @user_data: (closure callback): data to pass to @callback
 *
 * Invokes a callback for each frame in the grid column.
 */
void
panel_grid_column_foreach_frame (PanelGridColumn    *self,
                                 PanelFrameCallback  callback,
                                 gpointer            user_data)
{
  g_return_if_fail (PANEL_IS_GRID_COLUMN (self));
  g_return_if_fail (callback != NULL);

  for (GtkWidget *resizer = gtk_widget_get_first_child (GTK_WIDGET (self->rows));
       resizer != NULL;
       resizer = gtk_widget_get_next_sibling (resizer))
    {
      GtkWidget *child = panel_resizer_get_child (PANEL_RESIZER (resizer));

      callback (PANEL_FRAME (child), user_data);
    }
}

void
_panel_grid_column_prepend_frame (PanelGridColumn *self)
{
  PanelFrame *frame;
  PanelGrid *grid;

  g_return_if_fail (PANEL_IS_GRID_COLUMN (self));

  if (!(grid = PANEL_GRID (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_GRID))))
    g_return_if_reached ();

  frame = _panel_grid_create_frame (grid);
  panel_paned_prepend (self->rows, GTK_WIDGET (frame));
}
