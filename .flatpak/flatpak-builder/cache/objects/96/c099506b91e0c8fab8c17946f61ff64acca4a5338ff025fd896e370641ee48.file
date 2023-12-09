/* panel-resizer.c
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

#include "panel-dock-child-private.h"
#include "panel-handle-private.h"
#include "panel-frame-private.h"
#include "panel-resizer-private.h"

#define HANDLE_SIZE 8

struct _PanelResizer
{
  GtkWidget    parent_instance;

  PanelHandle *handle;
  GtkWidget   *child;

  double       drag_orig_size;
  double       drag_position;
  guint        drag_position_set : 1;

  PanelArea    area : 4;
};

G_DEFINE_TYPE (PanelResizer, panel_resizer, GTK_TYPE_WIDGET)

enum {
  PROP_0,
  PROP_CHILD,
  PROP_DRAG_POSITION,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

static void
panel_resizer_drag_begin_cb (PanelResizer   *self,
                             double          start_x,
                             double          start_y,
                             GtkGestureDrag *drag)
{
  GtkAllocation child_alloc;
  GtkAllocation handle_alloc;
  GtkWidget *dock_child;

  g_assert (PANEL_IS_RESIZER (self));
  g_assert (GTK_IS_GESTURE_DRAG (drag));

  if (self->child == NULL)
    return;

  if ((dock_child = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_DOCK_CHILD)) &&
      panel_dock_child_get_dragging (PANEL_DOCK_CHILD (dock_child)))
    goto deny_sequence;

  if (self->child != NULL)
    {
      switch (self->area)
        {
        case PANEL_AREA_START:
          if (start_x > gtk_widget_get_width (GTK_WIDGET (self)) - HANDLE_SIZE)
            goto start_drag;
          break;

        case PANEL_AREA_END:
          if (start_x <= HANDLE_SIZE)
            goto start_drag;
          break;

        case PANEL_AREA_TOP:
          if (start_y > gtk_widget_get_height (GTK_WIDGET (self)) - HANDLE_SIZE)
            goto start_drag;
          break;

        case PANEL_AREA_BOTTOM:
          if (start_y <= HANDLE_SIZE)
            goto start_drag;
          break;

        case PANEL_AREA_CENTER:
        default:
          break;
        }
    }

deny_sequence:
  gtk_gesture_set_state (GTK_GESTURE (drag),
                         GTK_EVENT_SEQUENCE_DENIED);

  return;

start_drag:

  gtk_widget_get_allocation (self->child, &child_alloc);
  gtk_widget_get_allocation (GTK_WIDGET (self->handle), &handle_alloc);

  if (self->area == PANEL_AREA_START ||
      self->area == PANEL_AREA_END)
    {
      self->drag_orig_size = child_alloc.width + handle_alloc.width;
      gtk_widget_set_hexpand (self->child, FALSE);
    }
  else
    {
      self->drag_orig_size = child_alloc.height + handle_alloc.height;
      gtk_widget_set_vexpand (self->child, FALSE);
    }

  self->drag_position = self->drag_orig_size;
  self->drag_position_set = TRUE;

  gtk_widget_queue_resize (GTK_WIDGET (self));
}

static void
panel_resizer_drag_update_cb (PanelResizer   *self,
                              double          offset_x,
                              double          offset_y,
                              GtkGestureDrag *drag)
{
  g_assert (PANEL_IS_RESIZER (self));
  g_assert (GTK_IS_GESTURE_DRAG (drag));

  if (self->area == PANEL_AREA_START)
    self->drag_position = self->drag_orig_size + offset_x;
  else if (self->area == PANEL_AREA_END)
    self->drag_position = gtk_widget_get_width (GTK_WIDGET (self)) - offset_x;
  else if (self->area == PANEL_AREA_TOP)
    self->drag_position = self->drag_orig_size + offset_y;
  else if (self->area == PANEL_AREA_BOTTOM)
    self->drag_position = gtk_widget_get_height (GTK_WIDGET (self)) - offset_y;

  g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_DRAG_POSITION]);

  gtk_widget_queue_resize (GTK_WIDGET (self));
}

static void
panel_resizer_drag_end_cb (PanelResizer   *self,
                           double          offset_x,
                           double          offset_y,
                           GtkGestureDrag *drag)
{
  g_assert (PANEL_IS_RESIZER (self));
  g_assert (GTK_IS_GESTURE_DRAG (drag));
}

GtkWidget *
panel_resizer_new (PanelArea area)
{
  PanelResizer *self;

  self = g_object_new (PANEL_TYPE_RESIZER, NULL);
  self->area = area;
  self->handle = PANEL_HANDLE (panel_handle_new (area));
  gtk_widget_set_parent (GTK_WIDGET (self->handle), GTK_WIDGET (self));

  if (area == PANEL_AREA_CENTER)
    gtk_widget_hide (GTK_WIDGET (self->handle));

  return GTK_WIDGET (self);
}

static void
panel_resizer_measure (GtkWidget      *widget,
                       GtkOrientation  orientation,
                       int             for_size,
                       int            *minimum,
                       int            *natural,
                       int            *minimum_baseline,
                       int            *natural_baseline)
{
  PanelResizer *self = (PanelResizer *)widget;

  g_assert (PANEL_IS_RESIZER (self));

  *minimum = 0;
  *natural = 0;
  *minimum_baseline = -1;
  *natural_baseline = -1;

  if (self->child != NULL)
    gtk_widget_measure (self->child,
                        orientation,
                        for_size,
                        minimum, natural,
                        NULL, NULL);

  if ((orientation == GTK_ORIENTATION_HORIZONTAL &&
       (self->area == PANEL_AREA_START ||
        self->area == PANEL_AREA_END)) ||
      (orientation == GTK_ORIENTATION_VERTICAL &&
       (self->area == PANEL_AREA_TOP ||
        self->area == PANEL_AREA_BOTTOM)))
    {
      int handle_min, handle_nat;

      if (self->drag_position_set)
        {
          if (self->drag_position > *minimum)
            *natural = self->drag_position;
          else if (self->drag_position < *minimum)
            *natural = *minimum;
        }

      if (gtk_widget_get_visible (GTK_WIDGET (self->handle)))
        {
          gtk_widget_measure (GTK_WIDGET (self->handle),
                              orientation, for_size,
                              &handle_min, &handle_nat,
                              NULL, NULL);

          *minimum += handle_min;
          *natural += handle_nat;
        }
    }
}

static void
panel_resizer_size_allocate (GtkWidget *widget,
                             int        width,
                             int        height,
                             int        baseline)
{
  PanelResizer *self = (PanelResizer *)widget;
  GtkOrientation orientation;
  GtkAllocation child_alloc;
  GtkAllocation handle_alloc;
  int handle_min = 0, handle_nat = 0;

  g_assert (PANEL_IS_RESIZER (self));

  if (self->area == PANEL_AREA_START ||
      self->area == PANEL_AREA_END)
    orientation = GTK_ORIENTATION_HORIZONTAL;
  else
    orientation = GTK_ORIENTATION_VERTICAL;

  if (gtk_widget_get_visible (GTK_WIDGET (self->handle)))
    gtk_widget_measure (GTK_WIDGET (self->handle),
                        orientation,
                        -1,
                        &handle_min, &handle_nat,
                        NULL, NULL);

  switch (self->area)
    {
    case PANEL_AREA_START:
      handle_alloc.x = width - handle_min;
      handle_alloc.width = handle_min;
      handle_alloc.y = 0;
      handle_alloc.height = height;
      child_alloc.x = 0;
      child_alloc.y = 0;
      child_alloc.width = width - handle_min;
      child_alloc.height = height;
      break;

    case PANEL_AREA_END:
      handle_alloc.x = 0;
      handle_alloc.width = handle_min;
      handle_alloc.y = 0;
      handle_alloc.height = height;
      child_alloc.x = handle_min;
      child_alloc.y = 0;
      child_alloc.width = width - handle_min;
      child_alloc.height = height;
      break;

    case PANEL_AREA_TOP:
      handle_alloc.x = 0;
      handle_alloc.width = width;
      handle_alloc.y = height - handle_min;
      handle_alloc.height = handle_min;
      child_alloc.x = 0;
      child_alloc.y = 0;
      child_alloc.width = width;
      child_alloc.height = height - handle_min;
      break;

    case PANEL_AREA_BOTTOM:
      handle_alloc.x = 0;
      handle_alloc.width = width;
      handle_alloc.y = 0;
      handle_alloc.height = handle_min;
      child_alloc.x = 0;
      child_alloc.y = handle_min;
      child_alloc.width = width;
      child_alloc.height = height - handle_min;
      break;

    case PANEL_AREA_CENTER:
    default:
      handle_alloc.x = 0;
      handle_alloc.width = 0;
      handle_alloc.y = 0;
      handle_alloc.height = 0;
      child_alloc.x = 0;
      child_alloc.y = 0;
      child_alloc.width = width;
      child_alloc.height = height;
      break;
    }

  if (gtk_widget_get_mapped (GTK_WIDGET (self->handle)))
    gtk_widget_size_allocate (GTK_WIDGET (self->handle), &handle_alloc, -1);

  if (self->child != NULL &&
      gtk_widget_get_mapped (self->child))
    gtk_widget_size_allocate (self->child, &child_alloc, -1);
}

static void
panel_resizer_compute_expand (GtkWidget *widget,
                              gboolean  *hexpand,
                              gboolean  *vexpand)
{
  PanelResizer *self = PANEL_RESIZER (widget);

  if (self->child != NULL)
    {
      *hexpand = gtk_widget_compute_expand (self->child, GTK_ORIENTATION_HORIZONTAL);
      *vexpand = gtk_widget_compute_expand (self->child, GTK_ORIENTATION_VERTICAL);
    }
  else
    {
      *hexpand = FALSE;
      *vexpand = FALSE;
    }
}

static gboolean
panel_resizer_grab_focus (GtkWidget *widget)
{
  PanelResizer *self = PANEL_RESIZER (widget);

  if (self->child != NULL)
    return gtk_widget_grab_focus (self->child);

  return FALSE;
}

static void
panel_resizer_dispose (GObject *object)
{
  PanelResizer *self = (PanelResizer *)object;

  g_clear_pointer ((GtkWidget **)&self->handle, gtk_widget_unparent);
  g_clear_pointer ((GtkWidget **)&self->child, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_resizer_parent_class)->dispose (object);
}

static void
panel_resizer_get_property (GObject    *object,
                            guint       prop_id,
                            GValue     *value,
                            GParamSpec *pspec)
{
  PanelResizer *self = PANEL_RESIZER (object);

  switch (prop_id)
    {
    case PROP_CHILD:
      g_value_set_object (value, panel_resizer_get_child (self));
      break;

    case PROP_DRAG_POSITION:
      g_value_set_int (value, self->drag_position);
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_resizer_set_property (GObject      *object,
                            guint         prop_id,
                            const GValue *value,
                            GParamSpec   *pspec)
{
  PanelResizer *self = PANEL_RESIZER (object);

  switch (prop_id)
    {
    case PROP_CHILD:
      panel_resizer_set_child (self, g_value_get_object (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_resizer_class_init (PanelResizerClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_resizer_dispose;
  object_class->get_property = panel_resizer_get_property;
  object_class->set_property = panel_resizer_set_property;

  widget_class->compute_expand = panel_resizer_compute_expand;
  widget_class->grab_focus = panel_resizer_grab_focus;
  widget_class->measure = panel_resizer_measure;
  widget_class->size_allocate = panel_resizer_size_allocate;

  properties [PROP_CHILD] =
    g_param_spec_object ("child",
                         "Child",
                         "Child",
                         GTK_TYPE_WIDGET,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_DRAG_POSITION] =
    g_param_spec_int ("drag-position", NULL, NULL, G_MININT, G_MAXINT, 0,
                      (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_css_name (widget_class, "panelresizer");
}

static void
panel_resizer_init (PanelResizer *self)
{
  GtkGesture *gesture;

  gesture = gtk_gesture_drag_new ();
  gtk_event_controller_set_propagation_phase (GTK_EVENT_CONTROLLER (gesture), GTK_PHASE_CAPTURE);
  g_signal_connect_object (gesture,
                           "drag-begin",
                           G_CALLBACK (panel_resizer_drag_begin_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (gesture,
                           "drag-update",
                           G_CALLBACK (panel_resizer_drag_update_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (gesture,
                           "drag-end",
                           G_CALLBACK (panel_resizer_drag_end_cb),
                           self,
                           G_CONNECT_SWAPPED);
  gtk_widget_add_controller (GTK_WIDGET (self), GTK_EVENT_CONTROLLER (gesture));
}

/**
 * panel_resizer_get_child:
 * @self: a #PanelResizer
 *
 * Gets the child widget of the resizer.
 *
 * Returns: (transfer none) (nullable): A #GtkWidget or %NULL
 */
GtkWidget *
panel_resizer_get_child (PanelResizer *self)
{
  g_return_val_if_fail (PANEL_IS_RESIZER (self), NULL);

  return self->child;
}

void
panel_resizer_set_child (PanelResizer *self,
                         GtkWidget    *child)
{
  g_return_if_fail (PANEL_IS_RESIZER (self));
  g_return_if_fail (!child || GTK_IS_WIDGET (child));

  if (child == self->child)
    return;

  g_clear_pointer (&self->child, gtk_widget_unparent);

  self->child = child;

  if (self->child != NULL)
    gtk_widget_insert_before (self->child,
                              GTK_WIDGET (self),
                              GTK_WIDGET (self->handle));

  g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CHILD]);
}

PanelArea
panel_resizer_get_area (PanelResizer *self)
{
  g_return_val_if_fail (PANEL_IS_RESIZER (self), 0);

  return self->area;
}

void
panel_resizer_set_area (PanelResizer *self,
                        PanelArea     area)
{
  g_return_if_fail (PANEL_IS_RESIZER (self));

  if (area != self->area)
    {
      self->area = area;

      panel_handle_set_area (self->handle, area);
      gtk_widget_queue_resize (GTK_WIDGET (self));
    }
}

GtkWidget *
panel_resizer_get_handle (PanelResizer *self)
{
  g_return_val_if_fail (PANEL_IS_RESIZER (self), NULL);

  return GTK_WIDGET (self->handle);
}

int
panel_resizer_get_drag_position (PanelResizer *self)
{
  g_return_val_if_fail (PANEL_IS_RESIZER (self), -1);

  return self->drag_position_set ? self->drag_position : -1;
}

void
panel_resizer_set_drag_position (PanelResizer *self,
                                 int           drag_position)
{
  g_return_if_fail (PANEL_IS_RESIZER (self));

  self->drag_position_set = drag_position >= 0;
  self->drag_position = MAX (drag_position, 0);

  g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_DRAG_POSITION]);

  gtk_widget_queue_resize (GTK_WIDGET (self));
}
