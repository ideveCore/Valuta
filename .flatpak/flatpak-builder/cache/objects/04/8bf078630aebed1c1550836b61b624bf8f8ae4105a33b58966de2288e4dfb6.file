/* panel-dock.c
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
#include "panel-dock-private.h"
#include "panel-dock-child-private.h"
#include "panel-frame-header.h"
#include "panel-frame-private.h"
#include "panel-grid-private.h"
#include "panel-grid-column.h"
#include "panel-maximized-controls-private.h"
#include "panel-paned.h"
#include "panel-position.h"
#include "panel-resizer-private.h"
#include "panel-frame-tab-bar.h"
#include "panel-widget.h"

/**
 * PanelDock:
 *
 * The #PanelDock is a widget designed to contain widgets that can be
 * docked. Use the #PanelDock as the top widget of your dockable UI.
 *
 * A #PanelDock is divided in 5 areas: %PANEL_AREA_TOP,
 * %PANEL_AREA_BOTTOM, %PANEL_AREA_START, %PANEL_AREA_END represent
 * the surrounding areas that can revealed. %PANEL_AREA_CENTER
 * represent the main area, that is always displayed and resized
 * depending on the reveal state of the surrounding areas.
 *
 * It will contain a #PanelDockChild for each of the areas in use,
 * albeit this is done by the widget.
 */
typedef struct
{
  GtkOverlay *overlay;
  GtkGrid *grid;
  PanelMaximizedControls *controls;

  PanelWidget *maximized;

  guint reveal_start : 1;
  guint reveal_end : 1;
  guint reveal_top : 1;
  guint reveal_bottom : 1;

  int start_width;
  int end_width;
  int top_height;
  int bottom_height;
} PanelDockPrivate;

static void buildable_iface_init (GtkBuildableIface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelDock, panel_dock, GTK_TYPE_WIDGET,
                         G_ADD_PRIVATE (PanelDock)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, buildable_iface_init))

enum {
  PROP_0,
  PROP_REVEAL_BOTTOM,
  PROP_REVEAL_END,
  PROP_REVEAL_START,
  PROP_REVEAL_TOP,
  PROP_CAN_REVEAL_BOTTOM,
  PROP_CAN_REVEAL_END,
  PROP_CAN_REVEAL_START,
  PROP_CAN_REVEAL_TOP,
  PROP_START_WIDTH,
  PROP_END_WIDTH,
  PROP_TOP_HEIGHT,
  PROP_BOTTOM_HEIGHT,
  N_PROPS
};

enum {
  ADOPT_WIDGET,
  CREATE_FRAME,
  PANEL_DRAG_BEGIN,
  PANEL_DRAG_END,
  N_SIGNALS
};

static GParamSpec *properties [N_PROPS];
static guint signals [N_SIGNALS];

/**
 * panel_dock_new:
 * Create a new #PanelDock.
 *
 * Returns: a newly created #PanelDock
 */
GtkWidget *
panel_dock_new (void)
{
  return g_object_new (PANEL_TYPE_DOCK, NULL);
}

static void
notify_can_reveal (PanelDock *self,
                   PanelArea  area)
{
  switch (area)
    {
    case PANEL_AREA_START:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_START]);
      break;

    case PANEL_AREA_END:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_END]);
      break;

    case PANEL_AREA_TOP:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_TOP]);
      break;

    case PANEL_AREA_BOTTOM:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_BOTTOM]);
      break;

    case PANEL_AREA_CENTER:
    default:
      break;
    }
}

static void
get_grid_positions (PanelArea       area,
                    int            *left,
                    int            *top,
                    int            *width,
                    int            *height,
                    GtkOrientation *orientation)
{

  switch (area)
    {
    case PANEL_AREA_START:
      *left = 0, *top = 0, *width = 1, *height = 3;
      *orientation = GTK_ORIENTATION_VERTICAL;
      break;

    case PANEL_AREA_END:
      *left = 2, *top = 0, *width = 1, *height = 3;
      *orientation = GTK_ORIENTATION_VERTICAL;
      break;

    case PANEL_AREA_TOP:
      *left = 1, *top = 0, *width = 1, *height = 1;
      *orientation = GTK_ORIENTATION_HORIZONTAL;
      break;

    case PANEL_AREA_BOTTOM:
      *left = 1, *top = 2, *width = 1, *height = 1;
      *orientation = GTK_ORIENTATION_HORIZONTAL;
      break;

    default:
    case PANEL_AREA_CENTER:
      *left = 1, *top = 1, *width = 1, *height = 1;
      *orientation = GTK_ORIENTATION_HORIZONTAL;
      break;
    }
}

static gboolean
set_reveal (PanelDock *self,
            PanelArea  area,
            gboolean   value)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->grid));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (!PANEL_IS_DOCK_CHILD (child))
        continue;

      if (panel_dock_child_get_area (PANEL_DOCK_CHILD (child)) == area)
        {
          if (value != panel_dock_child_get_reveal_child (PANEL_DOCK_CHILD (child)))
            {
              panel_dock_child_set_reveal_child (PANEL_DOCK_CHILD (child), value);

              if (value)
                gtk_widget_grab_focus (child);

              return TRUE;
            }
        }
    }

  return FALSE;
}

static gboolean
panel_dock_get_child_position_cb (PanelDock     *self,
                                  GtkWidget     *child,
                                  GtkAllocation *allocation,
                                  GtkOverlay    *overlay)
{
  GtkRequisition min, nat;

  g_assert (PANEL_IS_DOCK (self));
  g_assert (GTK_IS_WIDGET (child));
  g_assert (allocation != NULL);
  g_assert (GTK_IS_OVERLAY (overlay));

  if (PANEL_IS_MAXIMIZED_CONTROLS (child))
    return FALSE;

  /* Just use the whole section for now and rely on styling to
   * adjust the margin/padding/etc.
   */
  gtk_widget_get_preferred_size (child, &min, &nat);
  gtk_widget_get_allocation (GTK_WIDGET (self), allocation);
  allocation->x = 0;
  allocation->y = 0;

  return TRUE;
}

static void
page_unmaximize_action (GtkWidget  *widget,
                        const char *action_name,
                        GVariant   *param)
{
  PanelDock *self = (PanelDock *)widget;
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_assert (PANEL_IS_DOCK (self));

  if (priv->maximized != NULL)
    {
      PanelWidget *page = g_object_ref (priv->maximized);

      panel_widget_unmaximize (page);
      panel_widget_raise (page);
      panel_widget_focus_default (page);

      g_object_unref (page);
    }
}

static int
get_drag_size (PanelDock *self,
               PanelArea  area,
               int        fallback)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_assert (PANEL_IS_DOCK (self));

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->grid));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (PANEL_IS_DOCK_CHILD (child))
        {
          if (area == panel_dock_child_get_area (PANEL_DOCK_CHILD (child)))
            {
              int ret = panel_dock_child_get_drag_position (PANEL_DOCK_CHILD (child));

              if (ret > 0)
                return ret;
            }
        }
    }

  return fallback;
}

static int
panel_dock_get_start_width (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  return get_drag_size (self, PANEL_AREA_START, priv->start_width);
}

static int
panel_dock_get_end_width (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  return get_drag_size (self, PANEL_AREA_END, priv->end_width);
}

static int
panel_dock_get_top_height (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  return get_drag_size (self, PANEL_AREA_TOP, priv->top_height);
}

static int
panel_dock_get_bottom_height (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  return get_drag_size (self, PANEL_AREA_BOTTOM, priv->bottom_height);
}

static PanelFrame *
panel_dock_real_create_frame (PanelDock     *self,
                              PanelPosition *position)
{
  PanelFrame *frame;

  g_assert (PANEL_IS_DOCK (self));
  g_assert (PANEL_IS_POSITION (position));

  frame = PANEL_FRAME (panel_frame_new ());

  if (panel_position_get_area (position) == PANEL_AREA_CENTER)
    panel_frame_set_header (frame, PANEL_FRAME_HEADER (panel_frame_tab_bar_new ()));

  return frame;
}

PanelFrame *
_panel_dock_create_frame (PanelDock     *self,
                          PanelPosition *position)
{
  PanelFrame *ret = NULL;

  g_assert (PANEL_IS_DOCK (self));
  g_assert (PANEL_IS_POSITION (position));

  g_signal_emit (self, signals [CREATE_FRAME], 0, position, &ret);

  g_assert (!ret || PANEL_IS_FRAME (ret));

  return ret;
}

gboolean
_panel_dock_can_adopt (PanelDock   *dock,
                       PanelWidget *widget)
{
  gboolean ret = GDK_EVENT_PROPAGATE;

  g_signal_emit (dock, signals [ADOPT_WIDGET], 0, widget, &ret);

  return ret == GDK_EVENT_PROPAGATE;
}

static gboolean
panel_dock_real_adopt_widget (PanelDock   *dock,
                              PanelWidget *widget)
{
  return GDK_EVENT_PROPAGATE;
}

static void
panel_dock_dispose (GObject *object)
{
  PanelDock *self = (PanelDock *)object;
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  _panel_dock_set_maximized (self, NULL);
  g_clear_pointer ((GtkWidget **)&priv->overlay, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_dock_parent_class)->dispose (object);
}

static void
panel_dock_get_property (GObject    *object,
                         guint       prop_id,
                         GValue     *value,
                         GParamSpec *pspec)
{
  PanelDock *self = PANEL_DOCK (object);

  switch (prop_id)
    {
    case PROP_REVEAL_BOTTOM:
      g_value_set_boolean (value, panel_dock_get_reveal_bottom (self));
      break;

    case PROP_REVEAL_END:
      g_value_set_boolean (value, panel_dock_get_reveal_end (self));
      break;

    case PROP_REVEAL_START:
      g_value_set_boolean (value, panel_dock_get_reveal_start (self));
      break;

    case PROP_REVEAL_TOP:
      g_value_set_boolean (value, panel_dock_get_reveal_top (self));
      break;

    case PROP_CAN_REVEAL_BOTTOM:
      g_value_set_boolean (value, panel_dock_get_can_reveal_bottom (self));
      break;

    case PROP_CAN_REVEAL_END:
      g_value_set_boolean (value, panel_dock_get_can_reveal_end (self));
      break;

    case PROP_CAN_REVEAL_START:
      g_value_set_boolean (value, panel_dock_get_can_reveal_start (self));
      break;

    case PROP_CAN_REVEAL_TOP:
      g_value_set_boolean (value, panel_dock_get_can_reveal_top (self));
      break;

    case PROP_START_WIDTH:
      g_value_set_int (value, panel_dock_get_start_width (self));
      break;

    case PROP_END_WIDTH:
      g_value_set_int (value, panel_dock_get_end_width (self));
      break;

    case PROP_TOP_HEIGHT:
      g_value_set_int (value, panel_dock_get_top_height (self));
      break;

    case PROP_BOTTOM_HEIGHT:
      g_value_set_int (value, panel_dock_get_bottom_height (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_dock_set_property (GObject      *object,
                         guint         prop_id,
                         const GValue *value,
                         GParamSpec   *pspec)
{
  PanelDock *self = PANEL_DOCK (object);

  switch (prop_id)
    {
    case PROP_REVEAL_BOTTOM:
      panel_dock_set_reveal_bottom (self, g_value_get_boolean (value));
      break;

    case PROP_REVEAL_END:
      panel_dock_set_reveal_end (self, g_value_get_boolean (value));
      break;

    case PROP_REVEAL_START:
      panel_dock_set_reveal_start (self, g_value_get_boolean (value));
      break;

    case PROP_REVEAL_TOP:
      panel_dock_set_reveal_top (self, g_value_get_boolean (value));
      break;

    case PROP_START_WIDTH:
      panel_dock_set_start_width (self, g_value_get_int (value));
      break;

    case PROP_END_WIDTH:
      panel_dock_set_end_width (self, g_value_get_int (value));
      break;

    case PROP_TOP_HEIGHT:
      panel_dock_set_top_height (self, g_value_get_int (value));
      break;

    case PROP_BOTTOM_HEIGHT:
      panel_dock_set_bottom_height (self, g_value_get_int (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_dock_class_init (PanelDockClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_dock_dispose;
  object_class->get_property = panel_dock_get_property;
  object_class->set_property = panel_dock_set_property;

  properties [PROP_REVEAL_BOTTOM] =
    g_param_spec_boolean ("reveal-bottom",
                          "Reveal bottom",
                          "Reveal bottom",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_REVEAL_TOP] =
    g_param_spec_boolean ("reveal-top",
                          "Reveal top",
                          "Reveal top",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_REVEAL_START] =
    g_param_spec_boolean ("reveal-start",
                          "Reveal start",
                          "Reveal start",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_REVEAL_END] =
    g_param_spec_boolean ("reveal-end",
                          "Reveal end",
                          "Reveal end",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_CAN_REVEAL_BOTTOM] =
    g_param_spec_boolean ("can-reveal-bottom",
                          "Can reveal bottom",
                          "Can reveal bottom",
                          FALSE,
                          (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  properties [PROP_CAN_REVEAL_TOP] =
    g_param_spec_boolean ("can-reveal-top",
                          "Can reveal top",
                          "Can reveal top",
                          FALSE,
                          (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  properties [PROP_CAN_REVEAL_START] =
    g_param_spec_boolean ("can-reveal-start",
                          "Can reveal start",
                          "Can reveal start",
                          FALSE,
                          (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  properties [PROP_CAN_REVEAL_END] =
    g_param_spec_boolean ("can-reveal-end",
                          "Can reveal end",
                          "Can reveal end",
                          FALSE,
                          (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  properties [PROP_START_WIDTH] =
    g_param_spec_int ("start-width",
                      "Start Width",
                      "Start Width",
                      -1, G_MAXINT, -1,
                      (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  properties [PROP_END_WIDTH] =
    g_param_spec_int ("end-width",
                      "End Width",
                      "End Width",
                      -1, G_MAXINT, -1,
                      (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  properties [PROP_TOP_HEIGHT] =
    g_param_spec_int ("top-height",
                      "Top Height",
                      "Top Height",
                      -1, G_MAXINT, -1,
                      (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  properties [PROP_BOTTOM_HEIGHT] =
    g_param_spec_int ("bottom-height",
                      "Bottom Height",
                      "Bottom Height",
                      -1, G_MAXINT, -1,
                      (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  /**
   * PanelDock::panel-drag-begin:
   * @self: a #PanelDock
   * @panel: a #PanelWidget
   *
   * This signal is emitted when dragging of a panel begins.
   */
  signals [PANEL_DRAG_BEGIN] =
    g_signal_new ("panel-drag-begin",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelDockClass, panel_drag_begin),
                  NULL, NULL, NULL,
                  G_TYPE_NONE, 1, PANEL_TYPE_WIDGET);

  /**
   * PanelDock::panel-drag-end:
   * @self: a #PanelDock
   * @panel: a #PanelWidget
   *
   * This signal is emitted when dragging of a panel either
   * completes or was cancelled.
   */
  signals [PANEL_DRAG_END] =
    g_signal_new ("panel-drag-end",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelDockClass, panel_drag_end),
                  NULL, NULL, NULL,
                  G_TYPE_NONE, 1, PANEL_TYPE_WIDGET);

  /**
   * PanelDock::create-frame:
   * @self: a #PanelDock
   * @position: the position for the frame
   *
   * This signal is emitted when a new frame is needed.
   *
   * Returns: (transfer full) (not nullable): a #PanelFrame
   *
   * Since: 1.2
   */
  signals [CREATE_FRAME] =
    g_signal_new_class_handler ("create-frame",
                                G_TYPE_FROM_CLASS (klass),
                                G_SIGNAL_RUN_LAST,
                                G_CALLBACK (panel_dock_real_create_frame),
                                g_signal_accumulator_first_wins, NULL,
                                NULL,
                                PANEL_TYPE_FRAME,
                                1,
                                PANEL_TYPE_POSITION);

  /**
   * PanelDock::adopt-widget:
   * @self: a #PanelDock
   * @widget: a #PanelWidget
   *
   * Signal is emitted when a widget is requesting to be added via a
   * drag-n-drop event.
   *
   * This is generally propagated via #PanelFrame::adopt-widget to the
   * dock so that applications do not need to attach signal handlers
   * to every #PanelFrame.
   *
   * Returns: %GDK_EVENT_STOP to prevent dropping, otherwise
   *   %GDK_EVENT_PROPAGATE to allow adopting the widget.
   *
   * Since: 1.2
   */
  signals [ADOPT_WIDGET] =
    g_signal_new_class_handler ("adopt-widget",
                                G_TYPE_FROM_CLASS (klass),
                                G_SIGNAL_RUN_LAST,
                                G_CALLBACK (panel_dock_real_adopt_widget),
                                g_signal_accumulator_true_handled, NULL,
                                NULL,
                                G_TYPE_BOOLEAN,
                                1,
                                PANEL_TYPE_WIDGET);

  gtk_widget_class_install_action (widget_class, "page.unmaximize", NULL, page_unmaximize_action);

  gtk_widget_class_add_binding_action (widget_class, GDK_KEY_F11, GDK_SHIFT_MASK, "page.unmaximize", NULL);

  gtk_widget_class_set_css_name (widget_class, "paneldock");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
}

static void
panel_dock_init (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  priv->overlay = GTK_OVERLAY (gtk_overlay_new ());
  g_signal_connect_object (priv->overlay,
                           "get-child-position",
                           G_CALLBACK (panel_dock_get_child_position_cb),
                           self,
                           G_CONNECT_SWAPPED);
  gtk_widget_set_parent (GTK_WIDGET (priv->overlay), GTK_WIDGET (self));

  priv->grid = GTK_GRID (gtk_grid_new ());
  gtk_overlay_set_child (priv->overlay, GTK_WIDGET (priv->grid));

  priv->controls = PANEL_MAXIMIZED_CONTROLS (panel_maximized_controls_new ());
  gtk_widget_set_halign (GTK_WIDGET (priv->controls), GTK_ALIGN_END);
  gtk_widget_set_valign (GTK_WIDGET (priv->controls), GTK_ALIGN_START);
  gtk_widget_hide (GTK_WIDGET (priv->controls));
  gtk_overlay_add_overlay (priv->overlay, GTK_WIDGET (priv->controls));
}

static void
panel_dock_notify_empty_cb (PanelDock      *self,
                            GParamSpec     *pspec,
                            PanelDockChild *child)
{
  PanelArea area;

  g_assert (PANEL_IS_DOCK (self));
  g_assert (PANEL_IS_DOCK_CHILD (child));

  area = panel_dock_child_get_area (child);
  if (area == PANEL_AREA_CENTER)
    return;

  if (panel_dock_child_get_empty (child))
    panel_dock_child_set_reveal_child (child, FALSE);

  switch (panel_dock_child_get_area (child))
    {
    case PANEL_AREA_START:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_START]);
      break;

    case PANEL_AREA_END:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_END]);
      break;

    case PANEL_AREA_TOP:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_TOP]);
      break;

    case PANEL_AREA_BOTTOM:
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_REVEAL_BOTTOM]);
      break;

    case PANEL_AREA_CENTER:
    default:
      break;
    }
}

static GtkWidget *
get_or_create_dock_child (PanelDock *self,
                          PanelArea  area,
                          int        left,
                          int        top,
                          int        width,
                          int        height)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  GtkWidget *child;

  g_assert (PANEL_IS_DOCK (self));

  for (child = gtk_widget_get_first_child (GTK_WIDGET (priv->grid));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (PANEL_IS_DOCK_CHILD (child))
        {
          if (area == panel_dock_child_get_area (PANEL_DOCK_CHILD (child)))
            return child;
        }
    }

  child = panel_dock_child_new (area);
  panel_dock_child_set_reveal_child (PANEL_DOCK_CHILD (child), FALSE);
  g_signal_connect_object (child,
                           "notify::empty",
                           G_CALLBACK (panel_dock_notify_empty_cb),
                           self,
                           G_CONNECT_SWAPPED);
  gtk_grid_attach (priv->grid, child, left, top, width, height);

  return child;
}

static GtkWidget *
find_first_frame (GtkWidget *parent)
{
  for (GtkWidget *child = gtk_widget_get_first_child (parent);
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (PANEL_IS_FRAME (child))
        return child;

      if (PANEL_IS_RESIZER (child))
        {
          GtkWidget *resizer_child = panel_resizer_get_child (PANEL_RESIZER (child));

          if (PANEL_IS_FRAME (resizer_child))
            return resizer_child;
        }
    }

  return NULL;
}

static void
panel_dock_add_child (GtkBuildable *buildable,
                      GtkBuilder   *builder,
                      GObject      *object,
                      const char   *type)
{
  PanelDock *self = (PanelDock *)buildable;
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  PanelArea area = 0;
  GtkOrientation orientation = 0;
  gboolean reveal;
  int left;
  int top;
  int width;
  int height;
  int drag_position = -1;

  g_assert (PANEL_IS_DOCK (self));
  g_assert (GTK_IS_BUILDER (builder));
  g_assert (G_IS_OBJECT (object));

  if (!GTK_IS_WIDGET (object))
    return;

  if (g_strcmp0 (type, "start") == 0)
    {
      area = PANEL_AREA_START;
      reveal = priv->reveal_start;
      drag_position = priv->start_width;
    }
  else if (g_strcmp0 (type, "end") == 0)
    {
      area = PANEL_AREA_END;
      reveal = priv->reveal_end;
      drag_position = priv->end_width;
    }
  else if (g_strcmp0 (type, "top") == 0)
    {
      area = PANEL_AREA_TOP;
      reveal = priv->reveal_top;
      drag_position = priv->top_height;
    }
  else if (g_strcmp0 (type, "bottom") == 0)
    {
      area = PANEL_AREA_BOTTOM;
      reveal = priv->reveal_bottom;
      drag_position = priv->bottom_height;
    }
  else
    {
      area = PANEL_AREA_CENTER;
      reveal = TRUE;
    }

  get_grid_positions (area, &left, &top, &width, &height, &orientation);

  if (!PANEL_IS_DOCK_CHILD (object))
    {
      GtkWidget *dock_child = get_or_create_dock_child (self, area, left, top, width, height);

      panel_dock_child_set_drag_position (PANEL_DOCK_CHILD (dock_child), drag_position);

      if (area != PANEL_AREA_CENTER && PANEL_IS_WIDGET (object))
        {
          GtkWidget *paned = panel_dock_child_get_child (PANEL_DOCK_CHILD (dock_child));
          PanelFrame *frame;

          if (paned == NULL)
            {
              paned = panel_paned_new ();
              gtk_orientable_set_orientation (GTK_ORIENTABLE (paned), orientation);
              panel_dock_child_set_child (PANEL_DOCK_CHILD (dock_child), paned);
            }

          if (!(frame = PANEL_FRAME (find_first_frame (paned))))
            {
              PanelPosition *position = panel_position_new ();

              position = g_object_new (PANEL_TYPE_POSITION,
                                       "area", panel_dock_child_get_area (PANEL_DOCK_CHILD (dock_child)),
                                       NULL);
              frame = _panel_dock_create_frame (self, position);
              gtk_orientable_set_orientation (GTK_ORIENTABLE (frame), orientation);
              panel_paned_append (PANEL_PANED (paned), GTK_WIDGET (frame));

              g_object_unref (position);
            }

          panel_frame_add (frame, PANEL_WIDGET (object));
        }
      else
        {
          panel_dock_child_set_child (PANEL_DOCK_CHILD (dock_child), GTK_WIDGET (object));
        }
    }
  else
    {
      if (drag_position != -1)
        panel_dock_child_set_drag_position (PANEL_DOCK_CHILD (object), drag_position);
      gtk_grid_attach (priv->grid, GTK_WIDGET (object), left, top, width, height);
    }

  notify_can_reveal (self, area);
  set_reveal (self, area, reveal);
}

static void
buildable_iface_init (GtkBuildableIface *iface)
{
  iface->add_child = panel_dock_add_child;
}

/**
 * panel_dock_get_reveal_bottom:
 * @self: a #PanelDock
 *
 * Tells if the bottom area is revealed.
 *
 * Returns: The reveal state of the bottom area.
 */
gboolean
panel_dock_get_reveal_bottom (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);
  return priv->reveal_bottom;
}

/**
 * panel_dock_get_reveal_end:
 * @self: a #PanelDock
 *
 * Tells if the end area is revealed.
 *
 * Returns: The reveal state of the end area.
 */
gboolean
panel_dock_get_reveal_end (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);
  return priv->reveal_end;
}

/**
 * panel_dock_get_reveal_start:
 * @self: a #PanelDock
 *
 * Tells if the start area is revealed.
 *
 * Returns: The reveal state of the start area.
 */
gboolean
panel_dock_get_reveal_start (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);
  return priv->reveal_start;
}

/**
 * panel_dock_get_reveal_top:
 * @self: a #PanelDock
 *
 * Tells if the top area is revealed.
 *
 * Returns: The reveal state of the top area.
 */
gboolean
panel_dock_get_reveal_top (PanelDock *self)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);
  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);
  return priv->reveal_top;
}

/**
 * panel_dock_get_reveal_area:
 * @self: a #PanelDock
 * @area: the #PanelArea to return the reveal status of.
 *
 * Tells if an area if revealed.
 *
 * Returns: The reveal state.
 */
gboolean
panel_dock_get_reveal_area (PanelDock *self,
                            PanelArea  area)
{
  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);

  switch (area)
    {
    case PANEL_AREA_END:
      return panel_dock_get_reveal_end (self);
    case PANEL_AREA_TOP:
      return panel_dock_get_reveal_top (self);
    case PANEL_AREA_BOTTOM:
      return panel_dock_get_reveal_bottom (self);
    case PANEL_AREA_START:
      return panel_dock_get_reveal_start (self);
    case PANEL_AREA_CENTER:
    default:
      g_return_val_if_reached (FALSE);
    }
}

/**
 * panel_dock_set_reveal_bottom:
 * @self: a #PanelDock
 * @reveal_bottom: reveal the bottom area.
 *
 * Sets the reveal status of the bottom area.
 */
void
panel_dock_set_reveal_bottom (PanelDock *self,
                              gboolean   reveal_bottom)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->reveal_bottom = !!reveal_bottom;
  if (set_reveal (self, PANEL_AREA_BOTTOM, reveal_bottom))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_REVEAL_BOTTOM]);
}

/**
 * panel_dock_set_reveal_end:
 * @self: a #PanelDock
 * @reveal_end: reveal the end area.
 *
 * Sets the reveal status of the end area.
 */
void
panel_dock_set_reveal_end (PanelDock *self,
                           gboolean   reveal_end)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->reveal_end = !!reveal_end;
  if (set_reveal (self, PANEL_AREA_END, reveal_end))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_REVEAL_END]);
}

/**
 * panel_dock_set_reveal_start:
 * @self: a #PanelDock
 * @reveal_start: reveal the start area.
 *
 * Sets the reveal status of the start area.
 */
void
panel_dock_set_reveal_start (PanelDock *self,
                             gboolean   reveal_start)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->reveal_start = !!reveal_start;
  if (set_reveal (self, PANEL_AREA_START, reveal_start))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_REVEAL_START]);
}

/**
 * panel_dock_set_reveal_top:
 * @self: a #PanelDock
 * @reveal_top: reveal the top area.
 *
 * Sets the reveal status of the top area.
 */
void
panel_dock_set_reveal_top (PanelDock *self,
                           gboolean   reveal_top)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->reveal_top = !!reveal_top;
  if (set_reveal (self, PANEL_AREA_TOP, reveal_top))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_REVEAL_TOP]);
}

/**
 * panel_dock_set_reveal_area:
 * @self: a #PanelDock
 * @area: a #PanelArea. %PANEL_AREA_CENTER is an invalid value.
 * @reveal: reveal the area.
 *
 * Sets the reveal status of the area.
 */
void
panel_dock_set_reveal_area (PanelDock *self,
                            PanelArea  area,
                            gboolean   reveal)
{
  g_return_if_fail (PANEL_IS_DOCK (self));

  switch (area)
    {
    case PANEL_AREA_END:
      panel_dock_set_reveal_end (self, reveal);
      break;

    case PANEL_AREA_TOP:
      panel_dock_set_reveal_top (self, reveal);
      break;

    case PANEL_AREA_BOTTOM:
      panel_dock_set_reveal_bottom (self, reveal);
      break;

    case PANEL_AREA_START:
      panel_dock_set_reveal_start (self, reveal);
      break;

    case PANEL_AREA_CENTER:
    default:
      g_return_if_reached ();
    }
}

static GtkWidget *
panel_dock_get_child_for_area (PanelDock *self,
                               PanelArea  area)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_DOCK (self), NULL);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->grid));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (!PANEL_IS_DOCK_CHILD (child))
        continue;

      if (panel_dock_child_get_area (PANEL_DOCK_CHILD (child)) == area)
        return child;
    }

  return NULL;
}

GtkWidget *
_panel_dock_get_top_child (PanelDock *self)
{
  return panel_dock_get_child_for_area (self, PANEL_AREA_TOP);
}

GtkWidget *
_panel_dock_get_bottom_child (PanelDock *self)
{
  return panel_dock_get_child_for_area (self, PANEL_AREA_BOTTOM);
}

GtkWidget *
_panel_dock_get_start_child (PanelDock *self)
{
  return panel_dock_get_child_for_area (self, PANEL_AREA_START);
}

GtkWidget *
_panel_dock_get_end_child (PanelDock *self)
{
  return panel_dock_get_child_for_area (self, PANEL_AREA_END);
}

/**
 * panel_dock_get_can_reveal_area:
 * @self: a #PanelDock
 * @area: the panel area to check.
 *
 * Tells if the panel area can be revealed.
 *
 * Returns: whether it can reveal the area or not. If the is no child
 * or the child is empty, will return %FALSE.
 */
gboolean
panel_dock_get_can_reveal_area (PanelDock *self,
                                PanelArea  area)
{
  GtkWidget *child;

  g_return_val_if_fail (PANEL_IS_DOCK (self), FALSE);

  if (!(child = panel_dock_get_child_for_area (self, area)))
    return FALSE;

  return !panel_dock_child_get_empty (PANEL_DOCK_CHILD (child));
}

/**
 * panel_dock_get_can_reveal_bottom:
 * @self: a #PanelDock
 *
 * Tells if the bottom panel area can be revealed.
 *
 * Returns: whether it can reveal the bottom area or not. If the is no
 * child or the child is empty, will return %FALSE.
 */
gboolean
panel_dock_get_can_reveal_bottom (PanelDock *self)
{
  return panel_dock_get_can_reveal_area (self, PANEL_AREA_BOTTOM);
}

/**
 * panel_dock_get_can_reveal_top:
 * @self: a #PanelDock
 *
 * Tells if the top panel area can be revealed.
 *
 * Returns: whether it can reveal the top area or not. If the is no
 * child or the child is empty, will return %FALSE.
 */
gboolean
panel_dock_get_can_reveal_top (PanelDock *self)
{
  return panel_dock_get_can_reveal_area (self, PANEL_AREA_TOP);
}

/**
 * panel_dock_get_can_reveal_start:
 * @self: a #PanelDock
 *
 * Tells if the start panel area can be revealed.
 *
 * Returns: whether it can reveal the start area or not. If the is no
 * child or the child is empty, will return %FALSE.
 */
gboolean
panel_dock_get_can_reveal_start (PanelDock *self)
{
  return panel_dock_get_can_reveal_area (self, PANEL_AREA_START);
}

/**
 * panel_dock_get_can_reveal_end:
 * @self: a #PanelDock
 *
 * Tells if the end panel area can be revealed.
 *
 * Returns: whether it can reveal the end area or not. If the is no
 * child or the child is empty, will return %FALSE.
 */
gboolean
panel_dock_get_can_reveal_end (PanelDock *self)
{
  return panel_dock_get_can_reveal_area (self, PANEL_AREA_END);
}

static void
prepare_for_drag (PanelDock *self,
                  PanelArea  area)
{
  GtkWidget *child;
  GtkWidget *paned;

  g_assert (PANEL_IS_DOCK (self));

  if (!(child = panel_dock_get_child_for_area (self, area)))
    {
      GtkOrientation orientation;
      int left, top, width, height;

      /* TODO: Add policy to disable creating some panels (like top). */

      get_grid_positions (area, &left, &top, &width, &height, &orientation);
      child = get_or_create_dock_child (self, area, left, top, width, height);
      paned = panel_dock_child_get_child (PANEL_DOCK_CHILD (child));

      if (paned == NULL)
        {
          PanelPosition *position;
          PanelFrame *frame;

          position = g_object_new (PANEL_TYPE_POSITION,
                                   "area", area,
                                   NULL);

          paned = panel_paned_new ();
          gtk_orientable_set_orientation (GTK_ORIENTABLE (paned), orientation);
          panel_dock_child_set_child (PANEL_DOCK_CHILD (child), paned);

          frame = _panel_dock_create_frame (self, position);
          gtk_orientable_set_orientation (GTK_ORIENTABLE (frame), orientation);
          panel_paned_append (PANEL_PANED (paned), GTK_WIDGET (frame));

          g_object_unref (position);
        }
    }

  panel_dock_child_set_dragging (PANEL_DOCK_CHILD (child), TRUE);
}

static void
unprepare_from_drag (PanelDock *self,
                     PanelArea  area)
{
  GtkWidget *child;

  g_assert (PANEL_IS_DOCK (self));

  if ((child = panel_dock_get_child_for_area (self, area)))
    panel_dock_child_set_dragging (PANEL_DOCK_CHILD (child), FALSE);
}

void
_panel_dock_begin_drag (PanelDock   *self,
                        PanelWidget *panel)
{
  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (PANEL_IS_WIDGET (panel));

  /* For each of the edges that policy does not prohibit it,
   * make sure that there is a child there that we can expand
   * if necessary.
   */
  prepare_for_drag (self, PANEL_AREA_START);
  prepare_for_drag (self, PANEL_AREA_END);
  prepare_for_drag (self, PANEL_AREA_TOP);
  prepare_for_drag (self, PANEL_AREA_BOTTOM);

  g_signal_emit (self, signals [PANEL_DRAG_BEGIN], 0, panel);
}

void
_panel_dock_end_drag (PanelDock   *self,
                      PanelWidget *panel)
{
  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (PANEL_IS_WIDGET (panel));

  g_signal_emit (self, signals [PANEL_DRAG_END], 0, panel);

  unprepare_from_drag (self, PANEL_AREA_START);
  unprepare_from_drag (self, PANEL_AREA_END);
  unprepare_from_drag (self, PANEL_AREA_TOP);
  unprepare_from_drag (self, PANEL_AREA_BOTTOM);
}

void
_panel_dock_update_orientation (GtkWidget      *widget,
                                GtkOrientation  orientation)
{
  g_return_if_fail (GTK_IS_WIDGET (widget));

  if (orientation == GTK_ORIENTATION_HORIZONTAL)
    {
      gtk_widget_remove_css_class (widget, "vertical");
      gtk_widget_add_css_class (widget, "horizontal");
    }
  else
    {
      gtk_widget_remove_css_class (widget, "horizontal");
      gtk_widget_add_css_class (widget, "vertical");
    }

  gtk_accessible_update_property (GTK_ACCESSIBLE (widget),
                                  GTK_ACCESSIBLE_PROPERTY_ORIENTATION, orientation,
                                  -1);
}

void
_panel_dock_set_maximized (PanelDock   *self,
                           PanelWidget *widget)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (!widget || PANEL_IS_WIDGET (widget));
  g_return_if_fail (!widget || gtk_widget_get_parent (GTK_WIDGET (widget)) == NULL);

  if (priv->maximized == widget)
    return;

  if (priv->maximized)
    {
      gtk_widget_remove_css_class (GTK_WIDGET (priv->maximized), "maximized");
      gtk_overlay_remove_overlay (priv->overlay, GTK_WIDGET (priv->maximized));
      gtk_widget_hide (GTK_WIDGET (priv->controls));
      priv->maximized = NULL;
    }

  priv->maximized = widget;

  gtk_widget_action_set_enabled (GTK_WIDGET (self), "page.unmaximize", !!priv->maximized);

  if (priv->maximized)
    {
      gtk_widget_add_css_class (GTK_WIDGET (priv->maximized), "maximized");
      gtk_overlay_add_overlay (priv->overlay, GTK_WIDGET (priv->maximized));

      /* Move the controls to the top */
      g_object_ref (priv->controls);
      gtk_overlay_remove_overlay (priv->overlay, GTK_WIDGET (priv->controls));
      gtk_overlay_add_overlay (priv->overlay, GTK_WIDGET (priv->controls));
      gtk_widget_show (GTK_WIDGET (priv->controls));
      panel_widget_focus_default (widget);
      g_object_unref (priv->controls);
    }
}

void
_panel_dock_add_widget (PanelDock      *self,
                        PanelDockChild *dock_child,
                        PanelFrame     *frame,
                        PanelWidget    *widget)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (!dock_child || PANEL_IS_DOCK_CHILD (dock_child));
  g_return_if_fail (!frame || PANEL_IS_FRAME (frame));
  g_return_if_fail (PANEL_IS_WIDGET (widget));

  if (dock_child == NULL)
    {
      if (!(dock_child = PANEL_DOCK_CHILD (_panel_dock_get_start_child (self))))
        {
          int left, top, width, height;
          GtkOrientation orientation;

          get_grid_positions (PANEL_AREA_START, &left, &top, &width, &height, &orientation);

          dock_child = PANEL_DOCK_CHILD (panel_dock_child_new (PANEL_AREA_START));
          gtk_orientable_set_orientation (GTK_ORIENTABLE (dock_child), orientation);
          gtk_grid_attach (priv->grid, GTK_WIDGET (dock_child), left, top, width, height);
        }

      frame = NULL;
    }

  if (frame == NULL)
    {
      PanelArea area = panel_dock_child_get_area (dock_child);
      GtkOrientation orientation;

      if (area == PANEL_AREA_START || area == PANEL_AREA_END)
        orientation = GTK_ORIENTATION_VERTICAL;
      else
        orientation = GTK_ORIENTATION_HORIZONTAL;

      frame = PANEL_FRAME (panel_frame_new ());
      gtk_orientable_set_orientation (GTK_ORIENTABLE (dock_child), orientation);
      panel_dock_child_set_child (dock_child, GTK_WIDGET (frame));
    }

  g_assert (PANEL_IS_DOCK_CHILD (dock_child));
  g_assert (PANEL_IS_FRAME (frame));

  panel_frame_add (frame, widget);
  panel_frame_set_visible_child (frame, widget);

  notify_can_reveal (self, panel_dock_child_get_area (PANEL_DOCK_CHILD (dock_child)));
  set_reveal (self, panel_dock_child_get_area (PANEL_DOCK_CHILD (dock_child)), TRUE);
}

void
_panel_dock_remove_frame (PanelDock  *self,
                          PanelFrame *frame)
{
  GtkWidget *paned;
  GtkWidget *grid_column;
  GtkWidget *grid;

  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (PANEL_IS_FRAME (frame));

  /* We must at least be in a paned */
  if (!(paned = gtk_widget_get_ancestor (GTK_WIDGET (frame), PANEL_TYPE_PANED)))
    {
      g_warning ("Attempt to remove frame not in a PanelPaned");
      return;
    }

  grid_column = gtk_widget_get_ancestor (paned, PANEL_TYPE_GRID_COLUMN);
  grid = gtk_widget_get_ancestor (grid_column, PANEL_TYPE_GRID);

  panel_paned_remove (PANEL_PANED (paned), GTK_WIDGET (frame));

  if (grid && grid_column)
    _panel_grid_collapse (PANEL_GRID (grid),
                          PANEL_GRID_COLUMN (grid_column));
}

/**
 * panel_dock_foreach_frame:
 * @self: a #PanelDock
 * @callback: (not nullable) (scope call): a function to be called on each frame
 * @user_data: (closure callback): data to pass to @callback
 *
 * Invokes a callback for each frame in the dock.
 */
void
panel_dock_foreach_frame (PanelDock          *self,
                          PanelFrameCallback  callback,
                          gpointer            user_data)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (callback != NULL);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->grid));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (PANEL_IS_DOCK_CHILD (child))
        panel_dock_child_foreach_frame (PANEL_DOCK_CHILD (child), callback, user_data);
    }
}

static void
panel_dock_set_panel_size (PanelDock *self,
                           PanelArea  area,
                           int        size)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->grid));
       child;
       child = gtk_widget_get_next_sibling (child))
    {
      if (!PANEL_IS_DOCK_CHILD (child))
        continue;

      if (panel_dock_child_get_area (PANEL_DOCK_CHILD (child)) != area)
        continue;

      panel_dock_child_set_drag_position (PANEL_DOCK_CHILD (child), size);
    }
}

/**
 * panel_dock_set_start_width:
 * @self: a #PanelDock
 * @width: the width
 *
 * Set the width of the start area.
 */
void
panel_dock_set_start_width (PanelDock *self,
                            int        width)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->start_width = width;
  panel_dock_set_panel_size (self, PANEL_AREA_START, width);
}

/**
 * panel_dock_set_end_width:
 * @self: a #PanelDock
 * @width: the width
 *
 * Set the width of the end area.
 */
void
panel_dock_set_end_width (PanelDock *self,
                          int        width)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->end_width = width;
  panel_dock_set_panel_size (self, PANEL_AREA_END, width);
}

/**
 * panel_dock_set_top_height:
 * @self: a #PanelDock
 * @height: the height
 *
 * Set the height of the top area.
 */
void
panel_dock_set_top_height (PanelDock *self,
                           int        height)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->top_height = height;
  panel_dock_set_panel_size (self, PANEL_AREA_TOP, height);
}

/**
 * panel_dock_set_bottom_height:
 * @self: a #PanelDock
 * @height: the height
 *
 * Set the height of the bottom area.
 */
void
panel_dock_set_bottom_height (PanelDock *self,
                              int        height)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));

  priv->bottom_height = height;
  panel_dock_set_panel_size (self, PANEL_AREA_BOTTOM, height);
}

/**
 * panel_dock_remove:
 * @self: a #PanelDock
 * @widget: (transfer none): a #GtkWidget to remove
 *
 * Removes a widget from the dock. If @widget is not a #DockChild,
 * then the closest #DockChild parent is removed.
 */
void
panel_dock_remove (PanelDock *self,
                   GtkWidget *widget)
{
  PanelDockPrivate *priv = panel_dock_get_instance_private (self);

  g_return_if_fail (PANEL_IS_DOCK (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));

  if (!PANEL_IS_DOCK_CHILD (widget))
    {
      GtkWidget *parent = gtk_widget_get_ancestor (widget, PANEL_TYPE_DOCK_CHILD);

      g_return_if_fail (PANEL_IS_DOCK_CHILD (parent));
      g_return_if_fail (GTK_WIDGET (priv->grid) == gtk_widget_get_parent (parent));

      widget = parent;
    }

  gtk_grid_remove (priv->grid, widget);
}
