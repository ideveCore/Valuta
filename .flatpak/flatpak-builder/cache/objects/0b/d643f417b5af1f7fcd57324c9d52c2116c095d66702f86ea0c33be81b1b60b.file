/* panel-grid.c
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

#include "panel-dock-private.h"
#include "panel-frame.h"
#include "panel-frame-header.h"
#include "panel-frame-private.h"
#include "panel-frame-tab-bar.h"
#include "panel-grid-column.h"
#include "panel-grid-private.h"
#include "panel-paned.h"
#include "panel-position.h"
#include "panel-resizer-private.h"
#include "panel-save-dialog.h"
#include "panel-widget.h"

/**
 * PanelGrid:
 *
 * The #PanelGrid is a widget used to layout the dock item in the
 * center area.
 */
typedef struct
{
  PanelPaned *columns;
  GQueue      frame_mru;
} PanelGridPrivate;

static void buildable_iface_init (GtkBuildableIface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelGrid, panel_grid, GTK_TYPE_WIDGET,
                         G_ADD_PRIVATE (PanelGrid)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, buildable_iface_init))

enum {
  CREATE_FRAME,
  N_SIGNALS
};

static guint signals [N_SIGNALS];

/**
 * panel_grid_new:
 *
 * Creates a new #PanelGrid.
 *
 * Returns: a newly created #PanelGrid
 */
GtkWidget *
panel_grid_new (void)
{
  return g_object_new (PANEL_TYPE_GRID, NULL);
}

static void
panel_grid_reexpand (PanelGrid *self)
{
  guint n_columns;

  g_return_if_fail (PANEL_IS_GRID (self));

  n_columns = panel_grid_get_n_columns (self);

  for (guint i = 0; i < n_columns; i++)
    {
      PanelGridColumn *column = panel_grid_get_column (self, i);

      gtk_widget_set_hexpand (GTK_WIDGET (column), TRUE);
    }
}

static PanelFrame *
panel_grid_real_create_frame (PanelGrid *self)
{
  PanelPosition *position;
  PanelFrame *frame = NULL;
  PanelDock *dock;

  g_assert (PANEL_IS_GRID (self));

  if ((dock = PANEL_DOCK (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_DOCK))))
    {
      position = g_object_new (PANEL_TYPE_POSITION,
                               "area", PANEL_AREA_CENTER,
                               NULL);
      frame = _panel_dock_create_frame (dock, position);
      g_object_unref (position);
    }

  if (frame == NULL)
    {
      PanelFrameHeader *header;

      frame = PANEL_FRAME (panel_frame_new ());
      header = PANEL_FRAME_HEADER (panel_frame_tab_bar_new ());
      panel_frame_set_header (frame, header);
    }

  return frame;
}

PanelFrame *
_panel_grid_create_frame (PanelGrid *self)
{
  PanelFrame *frame = NULL;

  g_return_val_if_fail (PANEL_IS_GRID (self), NULL);

  g_signal_emit (self, signals [CREATE_FRAME], 0, &frame);
  g_return_val_if_fail (PANEL_IS_FRAME (frame), NULL);
  return frame;
}

void
_panel_grid_update_focus (PanelGrid *self)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);
  GtkWidget *first;
  GtkWidget *second;

  g_assert (PANEL_IS_GRID (self));

  /* We only need to update head and second nodes because
   * the focus was always the head, and may now be the second.
   */
  first = g_queue_peek_nth (&priv->frame_mru, 0);
  second = g_queue_peek_nth (&priv->frame_mru, 1);

  if (second)
    gtk_widget_remove_css_class (second, "has-focus");

  if (first)
    gtk_widget_add_css_class (first, "has-focus");
}

void
_panel_grid_drop_frame_mru (PanelGrid  *self,
                            PanelFrame *frame)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_assert (PANEL_IS_GRID (self));
  g_assert (PANEL_IS_FRAME (frame));

  g_queue_remove (&priv->frame_mru, frame);
  _panel_grid_update_focus (self);
}

static void
on_set_focus_cb (PanelGrid  *self,
                 GParamSpec *pspec,
                 GtkWindow  *window)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);
  GtkWidget *focus;
  GtkWidget *frame;

  g_assert (PANEL_IS_GRID (self));
  g_assert (GTK_IS_WINDOW (window));

  if ((focus = gtk_window_get_focus (window)) &&
      (frame = gtk_widget_get_ancestor (focus, PANEL_TYPE_FRAME)) &&
      GTK_WIDGET (self) == gtk_widget_get_ancestor (focus, PANEL_TYPE_GRID))
    {
      g_queue_remove (&priv->frame_mru, frame);
      g_queue_push_head (&priv->frame_mru, frame);
      _panel_grid_update_focus (self);
    }
}

static void
panel_grid_root (GtkWidget *widget)
{
  PanelGrid *self = (PanelGrid *)widget;
  GtkRoot *root;

  g_assert (PANEL_IS_GRID (self));

  GTK_WIDGET_CLASS (panel_grid_parent_class)->root (widget);

  if (GTK_IS_WINDOW ((root = gtk_widget_get_root (widget))))
    g_signal_connect_object (root,
                             "notify::focus-widget",
                             G_CALLBACK (on_set_focus_cb),
                             self,
                             G_CONNECT_SWAPPED);
}

static void
panel_grid_dispose (GObject *object)
{
  PanelGrid *self = (PanelGrid *)object;
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_clear_pointer ((GtkWidget **)&priv->columns, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_grid_parent_class)->dispose (object);
}

static void
panel_grid_class_init (PanelGridClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_grid_dispose;

  widget_class->root = panel_grid_root;

  klass->create_frame = panel_grid_real_create_frame;

  /**
   * PanelGrid::create-frame:
   * @self: a #PanelGrid
   *
   * The "create-frame" signal is used to create a new frame within
   * the grid.
   *
   * Consumers of this signal are required to return an unrooted
   * #PanelFrame from this signal. The first signal handler wins.
   *
   * Returns: (transfer full) (not nullable): an unrooted #PanelFrame
   */
  signals [CREATE_FRAME] =
    g_signal_new ("create-frame",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelGridClass, create_frame),
                  g_signal_accumulator_first_wins, NULL,
                  NULL,
                  PANEL_TYPE_FRAME, 0);

  gtk_widget_class_set_css_name (widget_class, "panelgrid");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
}

static void
panel_grid_init (PanelGrid *self)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  priv->columns = PANEL_PANED (panel_paned_new ());
  gtk_orientable_set_orientation (GTK_ORIENTABLE (priv->columns), GTK_ORIENTATION_HORIZONTAL);
  gtk_widget_set_parent (GTK_WIDGET (priv->columns), GTK_WIDGET (self));

  _panel_grid_prepend_column (self);
}

/**
 * panel_grid_get_most_recent_column:
 * @self: a #PanelGrid
 *
 * Gets the most recently acive column on a grid.
 *
 * Returns: (transfer none): a #PanelGridColumn
 */
PanelGridColumn *
panel_grid_get_most_recent_column (PanelGrid *self)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);
  GtkWidget *column;

  g_return_val_if_fail (PANEL_IS_GRID (self), NULL);

  if (priv->frame_mru.head != NULL)
    {
      GtkWidget *frame = g_queue_peek_head (&priv->frame_mru);
      column = gtk_widget_get_ancestor (frame, PANEL_TYPE_GRID_COLUMN);
    }
  else
    {
      column = panel_paned_get_nth_child (priv->columns, 0);
    }

  if (column == NULL)
    {
      _panel_grid_prepend_column (self);
      column = panel_paned_get_nth_child (priv->columns, 0);
    }

  return PANEL_GRID_COLUMN (column);
}

/**
 * panel_grid_get_most_recent_frame:
 * @self: a #PanelGrid
 *
 * Gets the most recently acive frame on a grid.
 *
 * Returns: (transfer none): a #PanelGridFrame
 */
PanelFrame *
panel_grid_get_most_recent_frame (PanelGrid *self)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);
  PanelGridColumn *column;

  g_return_val_if_fail (PANEL_IS_GRID (self), NULL);

  if (priv->frame_mru.head != NULL)
    return g_queue_peek_head (&priv->frame_mru);

  column = panel_grid_get_most_recent_column (self);
  return panel_grid_column_get_most_recent_frame (column);
}

static void
get_empty_frame_cb (PanelFrame *frame,
                    gpointer    user_data)
{
  PanelFrame **empty = user_data;

  if (*empty == NULL && panel_frame_get_empty (frame))
    *empty = frame;
}

static PanelFrame *
panel_grid_get_empty_frame (PanelGrid *self)
{
  PanelFrame *ret = NULL;

  g_assert (PANEL_IS_GRID (self));

  _panel_grid_foreach_frame (self, get_empty_frame_cb, &ret);

  return ret;
}

/**
 * panel_grid_add:
 * @self: a #PanelGrid
 * @widget: (transfer none): a #PanelWidget the widget to add.
 *
 * Add a #PanelWidget to the grid.
 */
void
panel_grid_add (PanelGrid   *self,
                PanelWidget *widget)
{
  PanelFrame *frame;
  PanelFrame *empty;

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (PANEL_IS_WIDGET (widget));

  frame = panel_grid_get_most_recent_frame (self);
  empty = panel_grid_get_empty_frame (self);

  if (empty)
    panel_frame_add (empty, widget);
  else
    panel_frame_add (frame, widget);
}

static void
panel_grid_add_child (GtkBuildable *buildable,
                      GtkBuilder   *builder,
                      GObject      *child,
                      const char   *type)
{
  PanelGrid *self = (PanelGrid *)buildable;
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_assert (PANEL_IS_GRID (self));
  g_assert (GTK_IS_BUILDER (builder));
  g_assert (G_IS_OBJECT (child));

  if (PANEL_IS_GRID_COLUMN (child))
    {
      GtkWidget *column;

      if (panel_paned_get_n_children (priv->columns) == 1 &&
          (column = panel_paned_get_nth_child (priv->columns, 0)) &&
          panel_grid_column_get_empty (PANEL_GRID_COLUMN (column)))
        panel_paned_remove (priv->columns, column);

      panel_paned_append (priv->columns, GTK_WIDGET (child));
      panel_grid_reexpand (self);
      _panel_grid_update_closeable (self);
    }
  else if (PANEL_IS_WIDGET (child))
    {
      panel_grid_add (self, PANEL_WIDGET (child));
    }
  else
    g_warning ("%s cannot add children of type %s",
               G_OBJECT_TYPE_NAME (self),
               G_OBJECT_TYPE_NAME (child));
}

static void
buildable_iface_init (GtkBuildableIface *iface)
{
  iface->add_child = panel_grid_add_child;
}

gboolean
_panel_grid_get_position (PanelGrid *self,
                          GtkWidget *widget,
                          guint     *column,
                          guint     *row)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);
  guint n_columns;

  g_return_val_if_fail (PANEL_IS_GRID (self), FALSE);
  g_return_val_if_fail (PANEL_IS_FRAME (widget), FALSE);

  /* TODO: This could be made better by walking towards the root
   *       from the child and calculating offsets.
   */

  *column = 0;
  *row = 0;

  n_columns = panel_paned_get_n_children (priv->columns);

  for (guint i = 0; i < n_columns; i++)
    {
      GtkWidget *column_widget = panel_paned_get_nth_child (priv->columns, i);
      guint n_rows;

      g_assert (PANEL_IS_GRID_COLUMN (column_widget));

      if (!gtk_widget_is_ancestor (widget, column_widget))
        continue;

      n_rows = panel_grid_column_get_n_rows (PANEL_GRID_COLUMN (column_widget));

      for (guint j = 0; j < n_rows; j++)
        {
          PanelFrame *frame = panel_grid_column_get_row (PANEL_GRID_COLUMN (column_widget), j);

          g_assert (PANEL_IS_FRAME (frame));

          if (widget != GTK_WIDGET (frame) &&
              !gtk_widget_is_ancestor (widget, GTK_WIDGET (frame)))
            continue;

          *column = i;
          *row = j;

          return TRUE;
        }
    }

  return FALSE;
}

/**
 * panel_grid_get_column:
 * @self: a #PanelGrid
 * @column: a column index
 *
 * Gets the #PanelGridColumn for a column index.
 *
 * Returns: (transfer none): a #PanelGridColumn
 */
PanelGridColumn *
panel_grid_get_column (PanelGrid *self,
                       guint      column)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);
  GtkWidget *child;

  g_return_val_if_fail (PANEL_IS_GRID (self), NULL);

  while (panel_paned_get_n_children (priv->columns) <= column)
    {
      GtkWidget *column_widget = panel_grid_column_new ();
      panel_paned_append (priv->columns, column_widget);
      panel_grid_reexpand (self);
      _panel_grid_update_closeable (self);
    }

  if (column > 0)
    gtk_widget_add_css_class (GTK_WIDGET (self), "multi-column");

  child = panel_paned_get_nth_child (priv->columns, column);
  g_return_val_if_fail (PANEL_IS_GRID_COLUMN (child), NULL);
  return PANEL_GRID_COLUMN (child);
}

void
_panel_grid_reposition (PanelGrid *self,
                        GtkWidget *widget,
                        guint      column,
                        guint      row,
                        gboolean   force_row)
{
  GtkWidget *frame;
  PanelFrame *new_frame;
  PanelGridColumn *column_widget;
  guint n_rows;

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (PANEL_IS_WIDGET (widget));

  if (!(frame = gtk_widget_get_ancestor (widget, PANEL_TYPE_FRAME)) ||
      !(column_widget = panel_grid_get_column (self, column)))
    g_return_if_reached ();

  if (!force_row)
    {
      n_rows = panel_grid_column_get_n_rows (column_widget);
      if (row >= n_rows)
        row = n_rows ? n_rows - 1 : 0;
    }

  new_frame = panel_grid_column_get_row (column_widget, row);

  if (frame == GTK_WIDGET (new_frame))
    g_return_if_reached ();

  _panel_frame_transfer (PANEL_FRAME (frame),
                         PANEL_WIDGET (widget),
                         new_frame,
                         -1);
}

void
_panel_grid_prepend_column (PanelGrid *self)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_return_if_fail (PANEL_IS_GRID (self));

  panel_paned_insert (priv->columns, 0, panel_grid_column_new ());
  panel_grid_reexpand (self);
  _panel_grid_update_closeable (self);
}

void
_panel_grid_insert_column (PanelGrid *self,
                           guint      position)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_return_if_fail (PANEL_IS_GRID (self));

  panel_paned_insert (priv->columns, position, panel_grid_column_new ());
  panel_grid_reexpand (self);
  _panel_grid_update_closeable (self);
}

/**
 * panel_grid_insert_column:
 * @self: a #PanelGrid
 * @position: The position to insert the column at.
 *
 * Inserts a column at @position.
 */
void
panel_grid_insert_column (PanelGrid *self,
                          guint      position)
{
  _panel_grid_insert_column (self, position);
}

/**
 * panel_grid_get_n_columns:
 * @self: a #PanelGrid
 *
 * Gets the number of columns in the grid.
 *
 * Returns: The number of columns.
 */
guint
panel_grid_get_n_columns (PanelGrid *self)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_GRID (self), 0);

  return panel_paned_get_n_children (priv->columns);
}

void
_panel_grid_remove_column (PanelGrid       *self,
                           PanelGridColumn *column)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (PANEL_IS_GRID_COLUMN (column));

  panel_paned_remove (priv->columns, GTK_WIDGET (column));
  panel_grid_reexpand (self);
  _panel_grid_update_closeable (self);
}

void
_panel_grid_foreach_frame (PanelGrid          *self,
                           PanelFrameCallback  callback,
                           gpointer            user_data)
{
  PanelGridPrivate *priv = panel_grid_get_instance_private (self);

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (callback != NULL);

  for (GtkWidget *resizer = gtk_widget_get_first_child (GTK_WIDGET (priv->columns));
       resizer != NULL;
       resizer = gtk_widget_get_next_sibling (resizer))
    {
      GtkWidget *column = panel_resizer_get_child (PANEL_RESIZER (resizer));

      panel_grid_column_foreach_frame (PANEL_GRID_COLUMN (column), callback, user_data);
    }
}

static void
has_pages_cb (PanelFrame *frame,
              gpointer    user_data)
{
  gboolean *has_page = user_data;
  *has_page |= !panel_frame_get_empty (frame);
}

static gboolean
has_pages (PanelGridColumn *column)
{
  gboolean has_page = FALSE;
  panel_grid_column_foreach_frame (column, has_pages_cb, &has_page);
  return has_page;
}

static gboolean
_panel_grid_has_single_frame (PanelGrid *self)
{
  g_assert (PANEL_IS_GRID (self));

  return panel_grid_get_n_columns (self) == 1 &&
         panel_grid_column_get_n_rows (panel_grid_get_column (self, 0)) == 1;
}

static void
adjust_can_close_frame (PanelFrame *frame,
                        gpointer    user_data)
{
  _panel_frame_set_closeable (frame, !!user_data);
}

void
_panel_grid_collapse (PanelGrid       *self,
                      PanelGridColumn *column)
{
  guint n_columns;

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (PANEL_IS_GRID_COLUMN (column));

  n_columns = panel_grid_get_n_columns (self);

  if (!has_pages (column) && n_columns > 1)
    {
      _panel_grid_remove_column (self, PANEL_GRID_COLUMN (column));
      n_columns--;
    }

  if (n_columns < 2)
    gtk_widget_remove_css_class (GTK_WIDGET (self), "multi-column");

  _panel_grid_update_closeable (self);
}

void
_panel_grid_update_closeable (PanelGrid *self)
{
  g_return_if_fail (PANEL_IS_GRID (self));

  /* If there is a single frame open, we don't want to allow closing it */
  if (_panel_grid_has_single_frame (self))
    _panel_grid_foreach_frame (self,
                               adjust_can_close_frame,
                               GUINT_TO_POINTER (FALSE));
  else
    _panel_grid_foreach_frame (self,
                               adjust_can_close_frame,
                               GUINT_TO_POINTER (TRUE));
}

static void
panel_grid_agree_to_close_frame_cb (PanelFrame *frame,
                                    gpointer    user_data)
{
  PanelSaveDialog *dialog = user_data;
  guint n_pages;

  g_assert (PANEL_IS_FRAME (frame));
  g_assert (PANEL_IS_SAVE_DIALOG (dialog));

  n_pages = panel_frame_get_n_pages (frame);

  for (guint i = 0; i < n_pages; i++)
    {
      PanelWidget *page = panel_frame_get_page (frame, i);
      PanelSaveDelegate *delegate = panel_widget_get_save_delegate (page);

      if (delegate != NULL)
        panel_save_dialog_add_delegate (dialog, delegate);
    }
}

static void
panel_grid_agree_to_close_cb (GObject      *object,
                              GAsyncResult *result,
                              gpointer      user_data)
{
  PanelSaveDialog *dialog = (PanelSaveDialog *)object;
  GError *error = NULL;
  GTask *task = user_data;

  g_assert (PANEL_IS_SAVE_DIALOG (dialog));
  g_assert (G_IS_ASYNC_RESULT (result));
  g_assert (G_IS_TASK (task));

  if (panel_save_dialog_run_finish (dialog, result, &error))
    g_task_return_boolean (task, TRUE);
  else
    g_task_return_error (task, error);

  g_clear_object (&task);
}

/**
 * panel_grid_agree_to_close_async:
 * @self: a #PanelGrid
 * @cancellable:
 * @callback: (not nullable) (scope call): callback called when ready
 * @user_data: (closure callback): data to pass to @callback
 *
 * Request to close, asynchronously. This will display the save dialog.
 */
void
panel_grid_agree_to_close_async (PanelGrid           *self,
                                 GCancellable        *cancellable,
                                 GAsyncReadyCallback  callback,
                                 gpointer             user_data)
{
  PanelSaveDialog *dialog;
  GTask *task = NULL;

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (!cancellable || G_IS_CANCELLABLE (cancellable));

  task = g_task_new (self, cancellable, callback, user_data);
  g_task_set_source_tag (task, panel_grid_agree_to_close_async);

  dialog = PANEL_SAVE_DIALOG (panel_save_dialog_new ());
  _panel_grid_foreach_frame (self,
                             panel_grid_agree_to_close_frame_cb,
                             dialog);
  panel_save_dialog_run_async (dialog,
                               cancellable,
                               panel_grid_agree_to_close_cb,
                               g_steal_pointer (&task));
}

/**
 * panel_grid_agree_to_close_finish:
 * @self: #PanelGrid
 * @result:
 * @error: (nullable): The #GError
 *
 * Returns:
 */
gboolean
panel_grid_agree_to_close_finish (PanelGrid     *self,
                                  GAsyncResult  *result,
                                  GError       **error)
{
  g_return_val_if_fail (PANEL_IS_GRID (self), FALSE);
  g_return_val_if_fail (G_IS_TASK (result), FALSE);

  return g_task_propagate_boolean (G_TASK (result), error);
}

/**
 * panel_grid_foreach_frame:
 * @self: a #PanelGrid
 * @callback: (scope call): a #PanelFrameCallback
 * @user_data: closure data for @callback
 *
 * Calls @callback for each #PanelFrame within @grid.
 */
void
panel_grid_foreach_frame (PanelGrid          *self,
                          PanelFrameCallback  callback,
                          gpointer            user_data)
{
  guint n_columns;

  g_return_if_fail (PANEL_IS_GRID (self));
  g_return_if_fail (callback != NULL);

  n_columns = panel_grid_get_n_columns (self);

  for (guint i = 0; i < n_columns; i++)
    {
      PanelGridColumn *column = panel_grid_get_column (self, i);

      panel_grid_column_foreach_frame (column, callback, user_data);
    }
}
