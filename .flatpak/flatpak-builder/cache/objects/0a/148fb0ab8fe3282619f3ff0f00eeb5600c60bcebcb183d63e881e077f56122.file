/* panel-paned.c
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

#include <string.h>

#include "panel-dock-child-private.h"
#include "panel-dock-private.h"
#include "panel-paned.h"
#include "panel-resizer-private.h"

/**
 * PanelPaned:
 *
 * A #PanelPaned is the concrete widget for a panel area.
 */
struct _PanelPaned
{
  GtkWidget      parent_instance;
  GtkOrientation orientation;
};

static void buildable_iface_init (GtkBuildableIface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelPaned, panel_paned, GTK_TYPE_WIDGET,
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, buildable_iface_init)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_ORIENTABLE, NULL))

enum {
  PROP_0,
  N_PROPS,

  PROP_ORIENTATION,
};

/**
 * panel_paned_new:
 *
 * Create a new #PanelPaned.
 *
 * Returns: a newly created #PanelPaned
 */
GtkWidget *
panel_paned_new (void)
{
  return g_object_new (PANEL_TYPE_PANED, NULL);
}

static void
panel_paned_set_orientation (PanelPaned     *self,
                             GtkOrientation  orientation)
{
  PanelArea area;

  g_assert (PANEL_IS_PANED (self));
  g_assert (orientation == GTK_ORIENTATION_HORIZONTAL ||
            orientation == GTK_ORIENTATION_VERTICAL);

  if (self->orientation == orientation)
    return;

  self->orientation = orientation;

  if (self->orientation == GTK_ORIENTATION_HORIZONTAL)
    area = PANEL_AREA_START;
  else
    area = PANEL_AREA_TOP;

  for (GtkWidget *child = gtk_widget_get_last_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_prev_sibling (child))
    {
      g_assert (PANEL_IS_RESIZER (child));

      panel_resizer_set_area (PANEL_RESIZER (child), area);
    }

  _panel_dock_update_orientation (GTK_WIDGET (self), self->orientation);
  gtk_widget_queue_resize (GTK_WIDGET (self));
  g_object_notify (G_OBJECT (self), "orientation");
}

static void
panel_paned_measure (GtkWidget      *widget,
                     GtkOrientation  orientation,
                     int             for_size,
                     int            *minimum,
                     int            *natural,
                     int            *minimum_baseline,
                     int            *natural_baseline)
{
  PanelPaned *self = (PanelPaned *)widget;

  g_assert (PANEL_IS_PANED (self));

  *minimum = 0;
  *natural = 0;
  *minimum_baseline = -1;
  *natural_baseline = -1;

  for (GtkWidget *child = gtk_widget_get_first_child (widget);
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      int child_min, child_nat;

      gtk_widget_measure (child, orientation, for_size, &child_min, &child_nat, NULL, NULL);

      if (orientation == self->orientation)
        {
          *minimum += child_min;
          *natural += child_nat;
        }
      else
        {
          *minimum = MAX (*minimum, child_min);
          *natural = MAX (*natural, child_nat);
        }
    }
}

typedef struct
{
  GtkWidget      *widget;
  GtkRequisition  min_request;
  GtkRequisition  nat_request;
  GtkAllocation   alloc;
} ChildAllocation;

static void
panel_paned_size_allocate (GtkWidget *widget,
                           int        width,
                           int        height,
                           int        baseline)
{
  PanelPaned *self = (PanelPaned *)widget;
  ChildAllocation *allocs;
  ChildAllocation *last_alloc = NULL;
  GtkOrientation orientation;
  guint n_children = 0;
  guint n_expand = 0;
  guint i;
  int extra_width = width;
  int extra_height = height;
  int expand_width;
  int expand_height;
  int x, y;

  g_assert (PANEL_IS_PANED (self));

  GTK_WIDGET_CLASS (panel_paned_parent_class)->size_allocate (widget, width, height, baseline);

  n_children = panel_paned_get_n_children (self);

  if (n_children == 1)
    {
      GtkWidget *child = gtk_widget_get_first_child (widget);
      GtkAllocation alloc = { 0, 0, width, height };

      if (gtk_widget_get_visible (child))
        {
          gtk_widget_size_allocate (child, &alloc, -1);
          return;
        }
    }

  orientation = gtk_orientable_get_orientation (GTK_ORIENTABLE (self));
  allocs = g_newa (ChildAllocation, n_children);
  memset (allocs, 0, sizeof *allocs * n_children);

  /* Give min size to each of the children */
  i = 0;
  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child), i++)
    {
      ChildAllocation *child_alloc = &allocs[i];

      if (!gtk_widget_get_visible (child))
        continue;

      gtk_widget_measure (child, GTK_ORIENTATION_HORIZONTAL, height,
                          &child_alloc->min_request.width,
                          &child_alloc->nat_request.width,
                          NULL, NULL);
      gtk_widget_measure (child, GTK_ORIENTATION_VERTICAL, width,
                          &child_alloc->min_request.height,
                          &child_alloc->nat_request.height,
                          NULL, NULL);

      child_alloc->alloc.width = child_alloc->min_request.width;
      child_alloc->alloc.height = child_alloc->min_request.height;

      n_expand += gtk_widget_compute_expand (child, orientation);

      if (orientation == GTK_ORIENTATION_HORIZONTAL)
        {
          extra_width -= child_alloc->alloc.width;
          child_alloc->alloc.height = height;
        }
      else
        {
          extra_height -= child_alloc->alloc.height;
          child_alloc->alloc.width = width;
        }
    }

  /* Now try to distribute extra space for natural size */
  i = 0;
  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child), i++)
    {
      ChildAllocation *child_alloc = &allocs[i];

      if (!gtk_widget_get_visible (child))
        continue;

      if (orientation == GTK_ORIENTATION_HORIZONTAL)
        {
          int taken = MIN (extra_width, child_alloc->nat_request.width - child_alloc->alloc.width);

          if (taken > 0)
            {
              child_alloc->alloc.width += taken;
              extra_width -= taken;
            }
        }
      else
        {
          int taken = MIN (extra_height, child_alloc->nat_request.height - child_alloc->alloc.height);

          if (taken > 0)
            {
              child_alloc->alloc.height += taken;
              extra_height -= taken;
            }
        }

      last_alloc = child_alloc;
    }

  /* Now give extra space for those that expand */
  expand_width = n_expand ? extra_width / n_expand : 0;
  expand_height = n_expand ? extra_height / n_expand : 0;
  i = n_children;
  for (GtkWidget *child = gtk_widget_get_last_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_prev_sibling (child), i--)
    {
      ChildAllocation *child_alloc = &allocs[i-1];

      if (!gtk_widget_get_visible (child))
        continue;

      if (!gtk_widget_compute_expand (child, orientation))
        continue;

      if (orientation == GTK_ORIENTATION_HORIZONTAL)
        {
          child_alloc->alloc.width += expand_width;
          extra_width -= expand_width;
        }
      else
        {
          child_alloc->alloc.height += expand_height;
          extra_height -= expand_height;
        }
    }

  /* Give any leftover to the last visible child */
  if (last_alloc)
    {
      if (orientation == GTK_ORIENTATION_HORIZONTAL)
        last_alloc->alloc.width += extra_width;
      else
        last_alloc->alloc.height += extra_height;
    }

  i = 0;
  x = 0;
  y = 0;
  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child), i++)
    {
      ChildAllocation *child_alloc = &allocs[i];

      child_alloc->alloc.x = x;
      child_alloc->alloc.y = y;

      if (orientation == GTK_ORIENTATION_HORIZONTAL)
        x += child_alloc->alloc.width;
      else
        y += child_alloc->alloc.height;

      gtk_widget_size_allocate (child, &child_alloc->alloc, -1);
    }
}

static gboolean
panel_paned_grab_focus (GtkWidget *widget)
{
  for (GtkWidget *child = gtk_widget_get_first_child (widget);
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (gtk_widget_grab_focus (child))
        return TRUE;
    }

  return FALSE;
}

static void
panel_paned_dispose (GObject *object)
{
  PanelPaned *self = (PanelPaned *)object;
  GtkWidget *child;

  child = gtk_widget_get_first_child (GTK_WIDGET (self));
  while (child)
    {
      GtkWidget *next = gtk_widget_get_next_sibling (child);
      gtk_widget_unparent (child);
      child = next;
    }

  G_OBJECT_CLASS (panel_paned_parent_class)->dispose (object);
}

static void
panel_paned_get_property (GObject    *object,
                          guint       prop_id,
                          GValue     *value,
                          GParamSpec *pspec)
{
  PanelPaned *self = PANEL_PANED (object);

  switch (prop_id)
    {
    case PROP_ORIENTATION:
      g_value_set_enum (value, self->orientation);
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_paned_set_property (GObject      *object,
                          guint         prop_id,
                          const GValue *value,
                          GParamSpec   *pspec)
{
  PanelPaned *self = PANEL_PANED (object);

  switch (prop_id)
    {
    case PROP_ORIENTATION:
      panel_paned_set_orientation (self, g_value_get_enum (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_paned_class_init (PanelPanedClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_paned_dispose;
  object_class->get_property = panel_paned_get_property;
  object_class->set_property = panel_paned_set_property;

  widget_class->grab_focus = panel_paned_grab_focus;
  widget_class->measure = panel_paned_measure;
  widget_class->size_allocate = panel_paned_size_allocate;

  g_object_class_override_property (object_class, PROP_ORIENTATION, "orientation");

  gtk_widget_class_set_css_name (widget_class, "panelpaned");
}

static void
panel_paned_init (PanelPaned *self)
{
  self->orientation = GTK_ORIENTATION_HORIZONTAL;

  _panel_dock_update_orientation (GTK_WIDGET (self), self->orientation);
}

static void
panel_paned_update_handles (PanelPaned *self)
{
  GtkWidget *child;

  g_assert (PANEL_IS_PANED (self));

  for (child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      GtkWidget *handle;

      g_assert (PANEL_IS_RESIZER (child));

      if ((handle = panel_resizer_get_handle (PANEL_RESIZER (child))))
        gtk_widget_show (handle);
    }

  if ((child = gtk_widget_get_last_child (GTK_WIDGET (self))))
    {
      GtkWidget *handle = panel_resizer_get_handle (PANEL_RESIZER (child));
      gtk_widget_hide (handle);
    }
}

/**
 * panel_paned_remove:
 * @self: a #PanelPaned
 * @child: (transfer none): a #GtkWidget
 *
 * Removes a widget from the paned.
 */
void
panel_paned_remove (PanelPaned *self,
                    GtkWidget  *child)
{
  GtkWidget *resizer;

  g_return_if_fail (PANEL_IS_PANED (self));
  g_return_if_fail (GTK_IS_WIDGET (child));

  resizer = gtk_widget_get_ancestor (child, PANEL_TYPE_RESIZER);
  g_return_if_fail (resizer != NULL &&
                    gtk_widget_get_parent (resizer) == GTK_WIDGET (self));
  gtk_widget_unparent (resizer);
  panel_paned_update_handles (self);
  gtk_widget_queue_resize (GTK_WIDGET (self));

  /* If we find a dock child, we might have changed its reveal
   * status and need to propagate that up.
   */
  if (gtk_widget_get_first_child (GTK_WIDGET (self)) ==
      gtk_widget_get_last_child (GTK_WIDGET (self)))
    {
      GtkWidget *dock_child = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_DOCK_CHILD);

      if (dock_child != NULL)
        g_object_notify (G_OBJECT (dock_child), "empty");
    }
}

/**
 * panel_paned_insert:
 * @self: a #PanelPaned
 * @position: the position
 * @child: (transfer none): a #GtkWidget to insert.
 *
 * Inserts a widget at position in the paned.
 */
void
panel_paned_insert (PanelPaned *self,
                    int         position,
                    GtkWidget  *child)
{
  PanelArea area;
  GtkWidget *resizer;

  g_return_if_fail (PANEL_IS_PANED (self));
  g_return_if_fail (GTK_IS_WIDGET (child));
  g_return_if_fail (gtk_widget_get_parent (child) == NULL);

  if (self->orientation == GTK_ORIENTATION_HORIZONTAL)
    area = PANEL_AREA_START;
  else
    area = PANEL_AREA_TOP;

  resizer = panel_resizer_new (area);
  panel_resizer_set_child (PANEL_RESIZER (resizer), child);

  if (position < 0)
    gtk_widget_insert_before (GTK_WIDGET (resizer), GTK_WIDGET (self), NULL);
  else if (position == 0)
    gtk_widget_insert_after (GTK_WIDGET (resizer), GTK_WIDGET (self), NULL);
  else
    {
      GtkWidget *sibling = gtk_widget_get_first_child (GTK_WIDGET (self));

      for (int i = position; i > 0 && sibling != NULL; i--)
        sibling = gtk_widget_get_next_sibling (sibling);

      gtk_widget_insert_before (GTK_WIDGET (resizer), GTK_WIDGET (self), sibling);
    }

  panel_paned_update_handles (self);

  gtk_widget_queue_resize (GTK_WIDGET (self));
}

/**
 * panel_paned_append:
 * @self: a #PanelPaned
 * @child: (transfer none): a #GtkWidget to append.
 *
 * Append a widget in the paned.
 */
void
panel_paned_append (PanelPaned *self,
                    GtkWidget  *child)
{
  panel_paned_insert (self, -1, child);
}

/**
 * panel_paned_prepend:
 * @self: a #PanelPaned
 * @child: (transfer none): a #GtkWidget to prepend.
 *
 * Prepends a widget in the paned.
 */
void
panel_paned_prepend (PanelPaned *self,
                     GtkWidget  *child)
{
  panel_paned_insert (self, 0, child);
}

/**
 * panel_paned_insert_after:
 * @self: a #PanelPaned
 * @child: (transfer none): a #GtkWidget to insert.
 * @sibling: (transfer none): the widget after which to insert.
 *
 * Inserts a widget afer @sibling in the paned.
 */
void
panel_paned_insert_after (PanelPaned *self,
                          GtkWidget  *child,
                          GtkWidget  *sibling)
{
  int position = 0;

  g_return_if_fail (PANEL_IS_PANED (self));
  g_return_if_fail (GTK_IS_WIDGET (child));
  g_return_if_fail (!sibling || GTK_IS_WIDGET (sibling));

  if (sibling == NULL)
    {
      panel_paned_prepend (self, child);
      return;
    }

  /* TODO: We should reverse insert() to call this */

  for (GtkWidget *ancestor = gtk_widget_get_first_child (GTK_WIDGET (self));
       ancestor != NULL;
       ancestor = gtk_widget_get_next_sibling (ancestor))
    {
      position++;

      if (sibling == ancestor || gtk_widget_is_ancestor (sibling, ancestor))
        break;
    }

  panel_paned_insert (self, position, child);
}

/**
 * panel_paned_get_n_children:
 * @self: a #PanelPaned
 *
 * Gets the number of children in the paned.
 *
 * Returns: the number of children.
 */
guint
panel_paned_get_n_children (PanelPaned *self)
{
  guint count = 0;

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    count++;

  return count;
}

/**
 * panel_paned_get_nth_child:
 * @self: a #PanelPaned
 * @nth: the child position
 *
 * Gets the child at position @nth.
 *
 * Returns: (transfer none) (nullable): a #GtkWidget or %NULL
 */
GtkWidget *
panel_paned_get_nth_child (PanelPaned *self,
                           guint       nth)
{
  g_return_val_if_fail (PANEL_IS_PANED (self), NULL);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      g_assert (PANEL_IS_RESIZER (child));

      if (nth == 0)
        return panel_resizer_get_child (PANEL_RESIZER (child));

      nth--;
    }

  return NULL;
}

static void
panel_paned_add_child (GtkBuildable *buildable,
                       GtkBuilder   *builder,
                       GObject      *child,
                       const char   *type)
{
  if (GTK_IS_WIDGET (child))
    panel_paned_append (PANEL_PANED (buildable), GTK_WIDGET (child));
  else
    g_warning ("Cannot add child of type %s to %s",
               G_OBJECT_TYPE_NAME (child),
               G_OBJECT_TYPE_NAME (buildable));
}

static void
buildable_iface_init (GtkBuildableIface *iface)
{
  iface->add_child = panel_paned_add_child;
}
