/* panel-statusbar.c
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

#include "panel-statusbar.h"

#define GET_PRIORITY(w)   GPOINTER_TO_INT(g_object_get_data(G_OBJECT(w),"PRIORITY"))
#define SET_PRIORITY(w,i) g_object_set_data(G_OBJECT(w),"PRIORITY",GINT_TO_POINTER(i))

/**
 * PanelStatusbar:
 *
 * A panel status bar is meant to be displayed at the bottom of the
 * window. It can contain widgets in the prefix and in the suffix.
 */
struct _PanelStatusbar
{
  GtkWidget  parent_instance;
  GtkWidget *expander;
  guint      disposed : 1;
};

static void buildable_iface_init (GtkBuildableIface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelStatusbar, panel_statusbar, GTK_TYPE_WIDGET,
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, buildable_iface_init))

/**
 * panel_statusbar_new:
 *
 * Create a new #PanelStatusbar.
 *
 * Returns: a newly created #PanelStatusBar.
 */
GtkWidget *
panel_statusbar_new (void)
{
  return g_object_new (PANEL_TYPE_STATUSBAR, NULL);
}

static void
window_notify_css_classes_cb (GtkWidget      *window,
                              GParamSpec     *pspec,
                              PanelStatusbar *self)
{
  gboolean rounded =
    !gtk_widget_has_css_class (window, "maximized") &&
    !gtk_widget_has_css_class (window, "tiled") &&
    !gtk_widget_has_css_class (window, "tiled-left") &&
    !gtk_widget_has_css_class (window, "tiled-right") &&
    !gtk_widget_has_css_class (window, "tiled-top") &&
    !gtk_widget_has_css_class (window, "tiled-bottom") &&
    !gtk_widget_has_css_class (window, "fullscreen") &&
    !gtk_widget_has_css_class (window, "solid-csd");

  if (rounded)
    gtk_widget_add_css_class (GTK_WIDGET (self), "rounded");
  else
    gtk_widget_remove_css_class (GTK_WIDGET (self), "rounded");
}

static void
panel_statusbar_root (GtkWidget *widget)
{
  GtkRoot *root;

  GTK_WIDGET_CLASS (panel_statusbar_parent_class)->root (widget);

  root = gtk_widget_get_root (widget);

  if (GTK_IS_WINDOW (root))
    g_signal_connect (root, "notify::css-classes",
                      G_CALLBACK (window_notify_css_classes_cb), widget);

  window_notify_css_classes_cb (GTK_WIDGET (root), NULL, PANEL_STATUSBAR (widget));
}

static void
panel_statusbar_unroot (GtkWidget *widget)
{
  GtkRoot *root = gtk_widget_get_root (widget);

  if (GTK_IS_WINDOW (root))
    {
      g_signal_handlers_disconnect_by_func (root,
                                            G_CALLBACK (window_notify_css_classes_cb),
                                            widget);

      gtk_widget_remove_css_class (widget, "rounded");
    }

  GTK_WIDGET_CLASS (panel_statusbar_parent_class)->unroot (widget);
}

static void
panel_statusbar_dispose (GObject *object)
{
  PanelStatusbar *self = (PanelStatusbar *)object;
  GtkWidget *child;

  self->disposed = TRUE;
  self->expander = NULL;

  while ((child = gtk_widget_get_first_child (GTK_WIDGET (self))))
    panel_statusbar_remove (self, child);

  G_OBJECT_CLASS (panel_statusbar_parent_class)->dispose (object);
}

static void
panel_statusbar_class_init (PanelStatusbarClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_statusbar_dispose;

  widget_class->root = panel_statusbar_root;
  widget_class->unroot = panel_statusbar_unroot;

  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BOX_LAYOUT);
  gtk_widget_class_set_css_name (widget_class, "panelstatusbar");
}

static void
panel_statusbar_init (PanelStatusbar *self)
{
  self->expander = g_object_new (GTK_TYPE_LABEL,
                                 "hexpand", TRUE,
                                 "visible", TRUE,
                                 NULL);
  gtk_widget_add_css_class (self->expander, "expander");
  gtk_widget_set_parent (self->expander, GTK_WIDGET (self));
}

static void
update_expander (PanelStatusbar *self)
{
  gboolean has_hexpand = FALSE;

  g_assert (PANEL_IS_STATUSBAR (self));

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (child == self->expander || !gtk_widget_get_visible (GTK_WIDGET (self)))
        continue;

      has_hexpand |= gtk_widget_compute_expand (child, GTK_ORIENTATION_HORIZONTAL);
    }

  gtk_widget_set_visible (self->expander, has_hexpand == FALSE);
}

/**
 * panel_statusbar_add_prefix:
 * @self: a #PanelStatusbar
 * @priority: the priority
 * @widget: (transfer none): a #GtkWidget to add.
 *
 * Adds a widget into the prefix with @priority. The higher the
 * priority the closer to the start the widget will be added.
 */
void
panel_statusbar_add_prefix (PanelStatusbar *self,
                            int             priority,
                            GtkWidget      *widget)
{
  GtkWidget *sibling = NULL;

  g_return_if_fail (PANEL_IS_STATUSBAR (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));
  g_return_if_fail (self->expander != NULL);

  SET_PRIORITY (widget, priority);

  g_signal_connect_swapped (widget,
                            "notify::visible",
                            G_CALLBACK (update_expander),
                            self);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      sibling = child;
      if (priority < GET_PRIORITY (child) || child == self->expander)
        break;
    }

  g_assert (sibling != NULL);

  gtk_widget_insert_before (widget, GTK_WIDGET (self), sibling);
  update_expander (self);
}

/**
 * panel_statusbar_add_suffix:
 * @self: a #PanelStatusbar
 * @priority: the priority
 * @widget: (transfer none): a #GtkWidget to add.
 *
 * Adds a widget into the suffix with @priority. The higher the
 * priority the closer to the start the widget will be added.
 */
void
panel_statusbar_add_suffix (PanelStatusbar *self,
                            int             priority,
                            GtkWidget      *widget)
{
  GtkWidget *sibling = NULL;

  g_return_if_fail (PANEL_IS_STATUSBAR (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));
  g_return_if_fail (self->expander != NULL);

  SET_PRIORITY (widget, priority);

  g_signal_connect_swapped (widget,
                            "notify::visible",
                            G_CALLBACK (update_expander),
                            self);

  for (GtkWidget *child = gtk_widget_get_last_child (GTK_WIDGET (self));
       child != NULL;
       child = gtk_widget_get_prev_sibling (child))
    {
      sibling = child;
      if (priority < GET_PRIORITY (child) || child == self->expander)
        break;
    }

  g_assert (sibling != NULL);

  gtk_widget_insert_after (widget, GTK_WIDGET (self), sibling);
  update_expander (self);
}

/**
 * panel_statusbar_remove:
 * @self: a #PanelStatusbar
 * @widget: (transfer none): a #GtkWidget to remove.
 *
 * Removes @widget from the #PanelStatusbar.
 */
void
panel_statusbar_remove (PanelStatusbar *self,
                        GtkWidget      *widget)
{
  g_return_if_fail (PANEL_IS_STATUSBAR (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));
  g_return_if_fail (GTK_WIDGET (self) == gtk_widget_get_parent (widget));
  g_return_if_fail (widget != self->expander);

  g_signal_handlers_disconnect_by_func (widget,
                                        G_CALLBACK (update_expander),
                                        self);

  gtk_widget_unparent (widget);

  if (!self->disposed)
    update_expander (self);
}

static void
panel_statusbar_add_child (GtkBuildable *buildable,
                           GtkBuilder   *builder,
                           GObject      *child,
                           const char   *type)
{
  PanelStatusbar *self = (PanelStatusbar *)buildable;

  g_assert (PANEL_IS_STATUSBAR (self));
  g_assert (GTK_IS_BUILDER (builder));

  if (g_strcmp0 (type, "suffix") == 0)
    panel_statusbar_add_suffix (self, 0, GTK_WIDGET (child));
  else if (GTK_IS_WIDGET (child))
    panel_statusbar_add_prefix (self, 0, GTK_WIDGET (child));
  else
    g_warning ("%s cannot add child of type %s",
               G_OBJECT_TYPE_NAME (self),
               G_OBJECT_TYPE_NAME (child));
}

static void
buildable_iface_init (GtkBuildableIface *iface)
{
  iface->add_child = panel_statusbar_add_child;
}
