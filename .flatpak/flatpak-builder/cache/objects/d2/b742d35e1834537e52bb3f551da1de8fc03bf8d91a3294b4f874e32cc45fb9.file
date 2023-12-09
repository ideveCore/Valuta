/* panel-document-workspace.c
 *
 * Copyright 2023 Christian Hergert <chergert@redhat.com>
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

#include "panel-document-workspace.h"
#include "panel-frame-header.h"
#include "panel-frame-switcher.h"
#include "panel-frame-tab-bar.h"
#include "panel-grid-column.h"
#include "panel-marshal.h"
#include "panel-paned.h"
#include "panel-widget.h"

#define GET_PRIORITY(w)   GPOINTER_TO_INT(g_object_get_data(G_OBJECT(w),"PRIORITY"))
#define SET_PRIORITY(w,i) g_object_set_data(G_OBJECT(w),"PRIORITY",GINT_TO_POINTER(i))

typedef struct
{
  PanelGrid *grid;
  PanelDock *dock;
  PanelStatusbar *statusbar;
  AdwBin *titlebar_bin;
  PanelPaned *start_area;
  PanelPaned *end_area;
  PanelPaned *top_area;
  PanelPaned *bottom_area;
} PanelDocumentWorkspacePrivate;

enum {
  PROP_0,
  PROP_DOCK,
  PROP_GRID,
  PROP_STATUSBAR,
  N_PROPS,

  OVERRIDE_PROP_TITLEBAR,
};

enum {
  ADD_WIDGET,
  CREATE_FRAME,
  N_SIGNALS
};

static void buildable_iface_init (GtkBuildableIface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelDocumentWorkspace, panel_document_workspace, PANEL_TYPE_WORKSPACE,
                         G_ADD_PRIVATE (PanelDocumentWorkspace)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, buildable_iface_init))

static GParamSpec *properties[N_PROPS];
static guint signals[N_SIGNALS];
static GtkBuildableIface *parent_buildable;

static gboolean
get_column (PanelPosition *self,
            guint         *column)
{
  if (column != NULL)
    *column = panel_position_get_column (self);
  return panel_position_get_column_set (self);
}

static gboolean
get_row (PanelPosition *self,
         guint         *row)
{
  if (row != NULL)
    *row = panel_position_get_row (self);
  return panel_position_get_row_set (self);
}

static gboolean
get_depth (PanelPosition *self,
           guint         *depth)
{
  if (depth != NULL)
    *depth = panel_position_get_depth (self);
  return panel_position_get_depth_set (self);
}

static gboolean
find_open_frame (PanelGrid *grid,
                 guint     *column,
                 guint     *row)
{
  guint n_columns;

  g_assert (PANEL_IS_GRID (grid));
  g_assert (column != NULL);
  g_assert (row != NULL);

  n_columns = panel_grid_get_n_columns (PANEL_GRID (grid));

  for (guint c = 0; c < n_columns; c++)
    {
      PanelGridColumn *grid_column = panel_grid_get_column (PANEL_GRID (grid), c);
      guint n_rows = panel_grid_column_get_n_rows (grid_column);

      for (guint r = 0; r < n_rows; r++)
        {
          PanelFrame *frame = panel_grid_column_get_row (grid_column, r);

          if (panel_frame_get_empty (frame))
            {
              *column = c;
              *row = r;
              return TRUE;
            }
        }
    }

  return FALSE;
}

static void
find_most_recent_frame (PanelDocumentWorkspace *self,
                        PanelGrid              *grid,
                        guint                  *column,
                        guint                  *row)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);
  GtkWidget *grid_column;
  PanelFrame *frame;
  guint n_columns;

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (PANEL_IS_GRID (grid));
  g_assert (column != NULL);
  g_assert (row != NULL);

  *column = 0;
  *row = 0;

  if (!(frame = panel_grid_get_most_recent_frame (priv->grid)) ||
      !(grid_column = gtk_widget_get_ancestor (GTK_WIDGET (frame), PANEL_TYPE_GRID_COLUMN)))
    return;

  n_columns = panel_grid_get_n_columns (PANEL_GRID (grid));

  for (guint c = 0; c < n_columns; c++)
    {
      if (grid_column == (GtkWidget *)panel_grid_get_column (PANEL_GRID (grid), c))
        {
          guint n_rows = panel_grid_column_get_n_rows (PANEL_GRID_COLUMN (grid_column));

          for (guint r = 0; r < n_rows; r++)
            {
              if ((PanelFrame *)frame == panel_grid_column_get_row (PANEL_GRID_COLUMN (grid_column), r))
                {
                  *column = c;
                  *row = r;
                  return;
                }
            }
        }
    }
}

static PanelFrame *
panel_document_workspace_find_frame (PanelDocumentWorkspace *self,
                                     PanelPosition          *position)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);
  PanelArea area = PANEL_AREA_CENTER;
  PanelPaned *paned = NULL;
  GtkWidget *parent;
  guint column = 0;
  guint row = 0;
  guint nth = 0;

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (position != NULL);

  if (panel_position_get_area_set (position))
    area = panel_position_get_area (position);

  if (area == PANEL_AREA_CENTER)
    {
      gboolean has_column = get_column (position, &column);
      gboolean has_row = get_row (position, &row);

      /* If we are adding a page, and no row or column is set, then the next
       * best thing to do is to try to find an open frame. If we can't do that
       * then we'll try to find the most recent frame.
       */
      if (!has_column && !has_row)
        {
          if (!find_open_frame (priv->grid, &column, &row))
            find_most_recent_frame (self, priv->grid, &column, &row);
        }

      return panel_grid_column_get_row (panel_grid_get_column (PANEL_GRID (priv->grid), column), row);
    }

  switch (area)
    {
    case PANEL_AREA_START:
      paned = priv->start_area;
      get_row (position, &nth);
      break;

    case PANEL_AREA_END:
      paned = priv->end_area;
      get_row (position, &nth);
      break;

    case PANEL_AREA_BOTTOM:
      paned = priv->bottom_area;
      get_column (position, &nth);
      break;

    case PANEL_AREA_TOP:
      paned = priv->top_area;
      get_column (position, &nth);
      break;

    case PANEL_AREA_CENTER:
    default:
      return NULL;
    }

  while (!(parent = panel_paned_get_nth_child (paned, nth)))
    {
      parent = panel_frame_new ();

      if (area == PANEL_AREA_START ||
          area == PANEL_AREA_END)
        gtk_orientable_set_orientation (GTK_ORIENTABLE (parent), GTK_ORIENTATION_VERTICAL);
      else
        gtk_orientable_set_orientation (GTK_ORIENTABLE (parent), GTK_ORIENTATION_HORIZONTAL);

      panel_paned_append (paned, parent);
    }

  return PANEL_FRAME (parent);
}

static gboolean
dummy_cb (gpointer data)
{
  return G_SOURCE_REMOVE;
}

static void
add_to_frame_with_depth (PanelFrame  *frame,
                         PanelWidget *widget,
                         guint        depth,
                         gboolean     depth_set)
{
  PanelWidget *previous_page;
  guint n_pages;

  g_assert (PANEL_IS_FRAME (frame));
  g_assert (PANEL_IS_WIDGET (widget));

  previous_page = panel_frame_get_visible_child (frame);

  if (!depth_set || depth > G_MAXINT)
    depth = G_MAXINT;

  SET_PRIORITY (widget, depth);

  n_pages = panel_frame_get_n_pages (frame);

  for (guint i = 0; i < n_pages; i++)
    {
      PanelWidget *child = panel_frame_get_page (frame, i);

      if ((int)depth < GET_PRIORITY (child))
        {
          panel_frame_add_before (frame, widget, child);
          goto reset_page;
        }
    }

  panel_frame_add (frame, widget);

reset_page:
  if (previous_page != NULL)
    panel_frame_set_visible_child (frame, previous_page);
}

static gboolean
panel_document_workspace_real_add_widget (PanelDocumentWorkspace *self,
                                          PanelWidget            *widget,
                                          PanelPosition          *position)
{
  PanelFrame *frame;
  gboolean depth_set;
  guint depth = 0;

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (PANEL_IS_WIDGET (widget));
  g_assert (PANEL_IS_POSITION (position));

  if (!(frame = panel_document_workspace_find_frame (self, position)))
    return FALSE;

  depth_set = get_depth (position, &depth);
  add_to_frame_with_depth (frame, widget, depth, depth_set);

  return TRUE;
}

static PanelFrame *
panel_document_workspace_real_create_frame (PanelDocumentWorkspace *self,
                                            PanelPosition          *position)
{
  PanelFrame *frame;

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (PANEL_IS_POSITION (position));

  frame = PANEL_FRAME (panel_frame_new ());

  if (panel_position_get_area (position) == PANEL_AREA_CENTER)
    {
      GtkWidget *tab_bar = panel_frame_tab_bar_new ();
      panel_frame_set_header (frame, PANEL_FRAME_HEADER (tab_bar));
    }
  else
    {
      GtkWidget *switcher = panel_frame_switcher_new ();
      panel_frame_set_header (frame, PANEL_FRAME_HEADER (switcher));
    }

  return frame;
}

static PanelFrame *
panel_document_workspace_create_frame_cb (PanelDocumentWorkspace *self,
                                          PanelPosition          *position,
                                          PanelDock              *dock)
{
  PanelFrame *frame = NULL;

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (PANEL_IS_POSITION (position));
  g_assert (PANEL_IS_DOCK (dock));

  g_signal_emit (self, signals[CREATE_FRAME], 0, position, &frame);

  return frame;
}

static void
panel_document_workspace_dispose (GObject *object)
{
  G_OBJECT_CLASS (panel_document_workspace_parent_class)->dispose (object);
}

static void
panel_document_workspace_get_property (GObject    *object,
                                       guint       prop_id,
                                       GValue     *value,
                                       GParamSpec *pspec)
{
  PanelDocumentWorkspace *self = PANEL_DOCUMENT_WORKSPACE (object);

  switch (prop_id)
    {
    case PROP_DOCK:
      g_value_set_object (value, panel_document_workspace_get_dock (self));
      break;

    case PROP_GRID:
      g_value_set_object (value, panel_document_workspace_get_grid (self));
      break;

    case PROP_STATUSBAR:
      g_value_set_object (value, panel_document_workspace_get_statusbar (self));
      break;

    case OVERRIDE_PROP_TITLEBAR:
      g_value_set_object (value, panel_document_workspace_get_titlebar (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_document_workspace_set_property (GObject      *object,
                                       guint         prop_id,
                                       const GValue *value,
                                       GParamSpec   *pspec)
{
  PanelDocumentWorkspace *self = PANEL_DOCUMENT_WORKSPACE (object);

  switch (prop_id)
    {
    case OVERRIDE_PROP_TITLEBAR:
      panel_document_workspace_set_titlebar (self, g_value_get_object (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_document_workspace_class_init (PanelDocumentWorkspaceClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_document_workspace_dispose;
  object_class->get_property = panel_document_workspace_get_property;
  object_class->set_property = panel_document_workspace_set_property;

  klass->add_widget = panel_document_workspace_real_add_widget;
  klass->create_frame = panel_document_workspace_real_create_frame;

  properties[PROP_DOCK] =
    g_param_spec_object ("dock", NULL, NULL,
                         PANEL_TYPE_DOCK,
                         (G_PARAM_READABLE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties[PROP_GRID] =
    g_param_spec_object ("grid", NULL, NULL,
                         PANEL_TYPE_GRID,
                         (G_PARAM_READABLE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties[PROP_STATUSBAR] =
    g_param_spec_object ("statusbar", NULL, NULL,
                         PANEL_TYPE_STATUSBAR,
                         (G_PARAM_READABLE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);
  g_object_class_override_property (object_class, OVERRIDE_PROP_TITLEBAR, "titlebar");

  /**
   * PanelDocumentWorkspace::add-widget:
   * @self: a #PanelDocumentWorkspace
   * @widget: a #PanelWidget
   * @position: a #PanelPosition
   *
   * This signal is used to add a #PanelWidget to the document workspace,
   * generally in the document grid.
   *
   * Returns: %TRUE if the widget was added and no more signal handlers
   *    will be notified.
   *
   * Since: 1.4
   */
  signals[ADD_WIDGET] =
    g_signal_new ("add-widget",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelDocumentWorkspaceClass, add_widget),
                  g_signal_accumulator_first_wins, NULL,
                  panel_marshal_BOOLEAN__OBJECT_OBJECT,
                  G_TYPE_BOOLEAN,
                  2,
                  PANEL_TYPE_WIDGET,
                  PANEL_TYPE_POSITION | G_SIGNAL_TYPE_STATIC_SCOPE);
  g_signal_set_va_marshaller (signals[ADD_WIDGET],
                              G_TYPE_FROM_CLASS (klass),
                              panel_marshal_BOOLEAN__OBJECT_OBJECTv);

  /**
   * PanelDocumentWorkspace::create-frame:
   * @self: a #PanelDocumentWorkspace
   * @position: the position of the frame
   *
   * Creates a new #PanelFrame to be added to the document grid.
   *
   * Returns: (transfer full): a #PanelFrame
   *
   * Since: 1.4
   */
  signals[CREATE_FRAME] =
    g_signal_new ("create-frame",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelDocumentWorkspaceClass, create_frame),
                  g_signal_accumulator_first_wins, NULL,
                  panel_marshal_OBJECT__OBJECT,
                  PANEL_TYPE_FRAME,
                  1,
                  PANEL_TYPE_POSITION);
  g_signal_set_va_marshaller (signals[CREATE_FRAME],
                              G_TYPE_FROM_CLASS (klass),
                              panel_marshal_OBJECT__OBJECTv);

  gtk_widget_class_set_template_from_resource (widget_class, "/org/gnome/libpanel/panel-document-workspace.ui");
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, bottom_area);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, dock);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, end_area);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, grid);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, start_area);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, statusbar);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, titlebar_bin);
  gtk_widget_class_bind_template_child_private (widget_class, PanelDocumentWorkspace, top_area);
  gtk_widget_class_bind_template_callback (widget_class, panel_document_workspace_create_frame_cb);
}

static void
panel_document_workspace_init (PanelDocumentWorkspace *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));
}

/**
 * panel_document_workspace_new:
 *
 * Creates a new #PanelDocumentWorkspace.
 *
 * Returns: (transfer full) (type PanelDocumentWorkspace): a #PanelDocumentWorkspace
 *
 * Since: 1.4
 */
GtkWidget *
panel_document_workspace_new (void)
{
  return g_object_new (PANEL_TYPE_DOCUMENT_WORKSPACE, NULL);
}

/**
 * panel_document_workspace_get_dock:
 * @self: a #PanelDocumentWorkspace
 *
 * Get the #PanelDock for the workspace.
 *
 * Returns: (transfer none): a #PanelDock
 *
 * Since: 1.4
 */
PanelDock *
panel_document_workspace_get_dock (PanelDocumentWorkspace *self)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_DOCUMENT_WORKSPACE (self), NULL);

  return priv->dock;
}

/**
 * panel_document_workspace_get_grid:
 * @self: a #PanelDocumentWorkspace
 *
 * Get the document grid for the workspace.
 *
 * Returns: (transfer none): a #PanelGrid
 *
 * Since: 1.4
 */
PanelGrid *
panel_document_workspace_get_grid (PanelDocumentWorkspace *self)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_DOCUMENT_WORKSPACE (self), NULL);

  return priv->grid;
}

/**
 * panel_document_workspace_get_statusbar:
 * @self: a #PanelDocumentWorkspace
 *
 * Gets the statusbar for the workspace.
 *
 * Returns: (transfer none) (nullable): a #PanelStatusbar
 *
 * Since: 1.4
 */
PanelStatusbar *
panel_document_workspace_get_statusbar (PanelDocumentWorkspace *self)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_DOCUMENT_WORKSPACE (self), NULL);

  return priv->statusbar;
}

/**
 * panel_document_workspace_get_titlebar:
 * @self: a #PanelDocumentWorkspace
 *
 * Gets the titlebar for the workspace.
 *
 * Returns: (transfer none) (nullable): a #GtkWidget or %NULL
 *
 * Since: 1.4
 */
GtkWidget *
panel_document_workspace_get_titlebar (PanelDocumentWorkspace *self)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_DOCUMENT_WORKSPACE (self), NULL);

  return adw_bin_get_child (priv->titlebar_bin);
}

void
panel_document_workspace_set_titlebar (PanelDocumentWorkspace *self,
                                       GtkWidget              *titlebar)
{
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_return_if_fail (!titlebar || GTK_IS_WIDGET (titlebar));

  if (titlebar != panel_document_workspace_get_titlebar (self))
    {
      adw_bin_set_child (priv->titlebar_bin, titlebar);
      g_object_notify (G_OBJECT (self), "titlebar");
    }
}

/**
 * panel_document_workspace_add_widget:
 * @self: a #PanelDocumentWorkspace
 * @widget: a #PanelWidget
 * @position: (nullable): a #PanelPosition or %NULL
 *
 * Requests the workspace add @widget to the dock at @position.
 *
 * Returns: %TRUE if @widget was added; otherwise %FALSE and @widget
 *   will have g_object_ref_sink() called and unref'd from an idle
 *   callback.
 *
 * Since: 1.4
 */
gboolean
panel_document_workspace_add_widget (PanelDocumentWorkspace *self,
                                     PanelWidget            *widget,
                                     PanelPosition          *position)
{
  PanelPosition *local_position = NULL;
  gboolean ret = FALSE;

  g_return_val_if_fail (PANEL_IS_DOCUMENT_WORKSPACE (self), FALSE);
  g_return_val_if_fail (PANEL_IS_WIDGET (widget), FALSE);
  g_return_val_if_fail (!position || PANEL_IS_POSITION (position), FALSE);

  if (position == NULL)
    position = local_position = panel_position_new ();

  g_signal_emit (self, signals [ADD_WIDGET], 0, widget, position, &ret);

  if (!ret)
    {
      /* Extreme failure case, try to be nice and wait until
       * end of the main loop to destroy
       */
      g_idle_add_full (G_PRIORITY_LOW,
                       dummy_cb,
                       g_object_ref_sink (widget),
                       g_object_unref);
    }

  g_clear_object (&local_position);

  return ret;
}

static GObject *
panel_document_workspace_get_internal_child (GtkBuildable *buildable,
                                             GtkBuilder   *builder,
                                             const char   *child_name)
{
  PanelDocumentWorkspace *self = PANEL_DOCUMENT_WORKSPACE (buildable);
  PanelDocumentWorkspacePrivate *priv = panel_document_workspace_get_instance_private (self);

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (GTK_IS_BUILDER (builder));
  g_assert (child_name != NULL);

  if (g_strcmp0 (child_name, "start_area") == 0)
    return G_OBJECT (priv->start_area);

  if (g_strcmp0 (child_name, "bottom_area") == 0)
    return G_OBJECT (priv->bottom_area);

  if (g_strcmp0 (child_name, "end_area") == 0)
    return G_OBJECT (priv->end_area);

  if (g_strcmp0 (child_name, "top_area") == 0)
    return G_OBJECT (priv->top_area);

  if (g_strcmp0 (child_name, "grid") == 0)
    return G_OBJECT (priv->grid);

  if (g_strcmp0 (child_name, "statusbar") == 0)
    return G_OBJECT (priv->statusbar);

  if (g_strcmp0 (child_name, "dock") == 0)
    return G_OBJECT (priv->dock);

  return parent_buildable->get_internal_child (buildable, builder, child_name);
}

static void
panel_document_workspace_add_child (GtkBuildable *buildable,
                                    GtkBuilder   *builder,
                                    GObject      *child,
                                    const char   *type)
{
  PanelDocumentWorkspace *self = PANEL_DOCUMENT_WORKSPACE (buildable);

  g_assert (PANEL_IS_DOCUMENT_WORKSPACE (self));
  g_assert (GTK_IS_BUILDER (builder));

  if (g_strcmp0 (type, "titlebar") == 0 && GTK_IS_WIDGET (child))
    panel_document_workspace_set_titlebar (self, GTK_WIDGET (child));
  else
    parent_buildable->add_child (buildable, builder, child, type);
}

static void
buildable_iface_init (GtkBuildableIface *iface)
{
  parent_buildable = g_type_interface_peek_parent (iface);

  iface->get_internal_child = panel_document_workspace_get_internal_child;
  iface->add_child = panel_document_workspace_add_child;
}
