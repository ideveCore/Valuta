/* panel-omni-bar.c
 *
 * Copyright 2022 Christian Hergert <chergert@redhat.com>
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

#include "panel-omni-bar.h"

/**
 * PanelOmniBar:
 * A multi-use widget for user interaction in the window header bar.
 *
 * You can add widgets, a popover to provide action items, an icon,
 * updates on progress and pulse the main widget.
 *
 * There is also a prefix and suffix area that can contain more
 * widgets.
 *
 * <picture>
 *   <source srcset="omni-bar-dark.png" media="(prefers-color-scheme: dark)">
 *   <img src="omni-bar.png" alt="omni-bar">
 * </picture>
 *
 */
typedef struct
{
  GtkBox         *box;
  GtkButton      *button;
  GtkMenuButton  *menu_button;
  GtkOverlay     *overlay;
  GtkBox         *prefix;
  GtkBox         *center;
  GtkBox         *suffix;
  GtkPopover     *popover;
  GtkProgressBar *progress_bar;
} PanelOmniBarPrivate;

static void buildable_iface_init  (GtkBuildableIface      *iface);
static void actionable_iface_init (GtkActionableInterface *iface);

G_DEFINE_TYPE_WITH_CODE (PanelOmniBar, panel_omni_bar, GTK_TYPE_WIDGET,
                         G_ADD_PRIVATE (PanelOmniBar)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_BUILDABLE, buildable_iface_init)
                         G_IMPLEMENT_INTERFACE (GTK_TYPE_ACTIONABLE, actionable_iface_init))



enum {
  PROP_0,
  PROP_ACTION_TOOLTIP,
  PROP_POPOVER,
  PROP_PROGRESS,
  PROP_ICON_NAME,
  PROP_MENU_MODEL,
  N_PROPS,

  PROP_ACTION_NAME,
  PROP_ACTION_TARGET,
};

static GParamSpec *properties [N_PROPS];

/**
 * panel_omni_bar_get_popover:
 * @self: a #PanelOmniBar
 *
 * Gets the current popover or %NULL if none is setup.
 *
 * Returns: (transfer none) (nullable): a #GtkPopover or %NULL
 */
GtkPopover *
panel_omni_bar_get_popover (PanelOmniBar *self)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_OMNI_BAR (self), NULL);

  return priv->popover;
}

/**
 * panel_omni_bar_set_popover:
 * @self: a #PanelOmniBar
 * @popover: (transfer none) (nullable): a #GtkPopover or %NULL
 *
 * Sets the omnibar popover, that will appear when clicking on the omni bar.
 */
void
panel_omni_bar_set_popover (PanelOmniBar *self,
                            GtkPopover   *popover)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));
  g_return_if_fail (!popover || GTK_IS_POPOVER (popover));

  if (popover == priv->popover)
    return;

  if (priv->popover)
    gtk_widget_unparent (GTK_WIDGET (priv->popover));

  priv->popover = popover;

  if (popover)
    gtk_widget_set_parent (GTK_WIDGET (popover), GTK_WIDGET (self));

  g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_POPOVER]);
}

/**
 * panel_omni_bar_new:
 *
 * Create a new #PanelOmniBar.
 *
 * Returns: a newly created #PanelOmniBar
 */
GtkWidget *
panel_omni_bar_new (void)
{
  return g_object_new (PANEL_TYPE_OMNI_BAR, NULL);
}

static void
panel_omni_bar_click_released_cb (PanelOmniBar    *self,
                                  int              n_relases,
                                  double           x,
                                  double           y,
                                  GtkGestureClick *click)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_assert (PANEL_IS_OMNI_BAR (self));
  g_assert (GTK_IS_GESTURE_CLICK (click));

  if (priv->popover == NULL)
    return;

  gtk_popover_popup (priv->popover);
}

static void
panel_omni_bar_size_allocate (GtkWidget *widget,
                              int        width,
                              int        height,
                              int        baseline)
{
  PanelOmniBar *self = (PanelOmniBar *)widget;
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_assert (PANEL_IS_OMNI_BAR (self));

  if (priv->popover)
    gtk_popover_present (priv->popover);
}

static void
panel_omni_bar_dispose (GObject *object)
{
  PanelOmniBar *self = (PanelOmniBar *)object;
  GtkWidget *child;

  panel_omni_bar_stop_pulsing (self);

  while ((child = gtk_widget_get_first_child (GTK_WIDGET (self))))
    gtk_widget_unparent (child);

  G_OBJECT_CLASS (panel_omni_bar_parent_class)->dispose (object);
}

static void
panel_omni_bar_get_property (GObject    *object,
                             guint       prop_id,
                             GValue     *value,
                             GParamSpec *pspec)
{
  PanelOmniBar *self = PANEL_OMNI_BAR (object);
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  switch (prop_id)
    {
    case PROP_ACTION_NAME:
      g_value_set_string (value,
                          gtk_actionable_get_action_name (GTK_ACTIONABLE (priv->button)));
      break;

    case PROP_ACTION_TARGET:
      g_value_set_variant (value,
                           gtk_actionable_get_action_target_value (GTK_ACTIONABLE (priv->button)));
      break;

    case PROP_ACTION_TOOLTIP:
      g_value_set_string (value, gtk_widget_get_tooltip_text (GTK_WIDGET (priv->button)));
      break;

    case PROP_POPOVER:
      g_value_set_object (value, panel_omni_bar_get_popover (self));
      break;

    case PROP_PROGRESS:
      g_value_set_double (value, panel_omni_bar_get_progress (self));
      break;

    case PROP_ICON_NAME:
      g_value_set_string (value, gtk_button_get_icon_name (priv->button));
      break;

    case PROP_MENU_MODEL:
      g_value_set_object (value, gtk_menu_button_get_menu_model (priv->menu_button));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_omni_bar_set_property (GObject      *object,
                             guint         prop_id,
                             const GValue *value,
                             GParamSpec   *pspec)
{
  PanelOmniBar *self = PANEL_OMNI_BAR (object);
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  switch (prop_id)
    {
    case PROP_ACTION_NAME:
      gtk_actionable_set_action_name (GTK_ACTIONABLE (priv->button),
                                      g_value_get_string (value));
      break;

    case PROP_ACTION_TARGET:
      gtk_actionable_set_action_target_value (GTK_ACTIONABLE (priv->button),
                                              g_value_get_variant (value));
      break;

    case PROP_ACTION_TOOLTIP:
      gtk_widget_set_tooltip_text (GTK_WIDGET (priv->button), g_value_get_string (value));
      break;

    case PROP_POPOVER:
      panel_omni_bar_set_popover (self, g_value_get_object (value));
      break;

    case PROP_PROGRESS:
      panel_omni_bar_set_progress (self, g_value_get_double (value));
      break;

    case PROP_ICON_NAME:
      gtk_button_set_icon_name (priv->button, g_value_get_string (value));
      break;

    case PROP_MENU_MODEL:
      gtk_menu_button_set_menu_model (priv->menu_button, g_value_get_object (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_omni_bar_class_init (PanelOmniBarClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_omni_bar_dispose;
  object_class->get_property = panel_omni_bar_get_property;
  object_class->set_property = panel_omni_bar_set_property;

  widget_class->size_allocate = panel_omni_bar_size_allocate;

  g_object_class_override_property (object_class, PROP_ACTION_NAME, "action-name");
  g_object_class_override_property (object_class, PROP_ACTION_TARGET, "action-target");

  /**
   * PanelOmniBar:action-tooltip:
   *
   * The tooltip for the action.
   */
  properties[PROP_ACTION_TOOLTIP] =
    g_param_spec_string ("action-tooltip", NULL, NULL, NULL,
                         (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  /**
   * PanelOmniBar:icon-name:
   *
   * The name of the icon to use.
   */
  properties [PROP_ICON_NAME] =
    g_param_spec_string ("icon-name",
                         "Icon Name",
                         "Icon Name",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  /**
   * PanelOmniBar:menu-model:
   *
   * The menu model of the omni bar menu.
   */
  properties [PROP_MENU_MODEL] =
    g_param_spec_object ("menu-model",
                         "Menu Model",
                         "Menu Model",
                         G_TYPE_MENU_MODEL,
                         (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  /**
   * PanelOmniBar:popover:
   *
   * The popover to show.
   */
  properties [PROP_POPOVER] =
    g_param_spec_object ("popover",
                         "Popover",
                         "Popover",
                         GTK_TYPE_POPOVER,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelOmniBar:progress:
   *
   * The current progress value.
   */
  properties [PROP_PROGRESS] =
    g_param_spec_double ("progress",
                         "Progress",
                         "Progress bar fraction",
                         0.0, 1.0, 0.0,
                         (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BOX_LAYOUT);
  gtk_widget_class_set_css_name (widget_class, "splitbutton");
}

static void
panel_omni_bar_init (PanelOmniBar *self)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);
  GtkGesture *gesture;
  GtkWidget *separator;
  GtkBox *box;

  gtk_widget_add_css_class (GTK_WIDGET (self), "omnibar");

  priv->box = g_object_new (GTK_TYPE_BOX,
                            "css-name", "button",
                            "orientation", GTK_ORIENTATION_HORIZONTAL,
                            NULL);
  gtk_widget_set_parent (GTK_WIDGET (priv->box), GTK_WIDGET (self));

  priv->button = g_object_new (GTK_TYPE_BUTTON, NULL);
  gtk_widget_set_parent (GTK_WIDGET (priv->button), GTK_WIDGET (self));

  separator = g_object_new (GTK_TYPE_SEPARATOR,
                            "orientation", GTK_ORIENTATION_VERTICAL,
                            NULL);
  gtk_widget_set_parent (separator, GTK_WIDGET (self));

  priv->menu_button = g_object_new (GTK_TYPE_MENU_BUTTON,
                                    NULL);
  gtk_widget_set_parent (GTK_WIDGET (priv->menu_button), GTK_WIDGET (self));

  priv->prefix = g_object_new (GTK_TYPE_BOX, NULL);
  priv->center = g_object_new (GTK_TYPE_BOX,
                               "hexpand", TRUE,
                               NULL);
  priv->suffix = g_object_new (GTK_TYPE_BOX, NULL);

  box = g_object_new (GTK_TYPE_BOX,
                      "orientation", GTK_ORIENTATION_HORIZONTAL,
                      NULL);
  gtk_box_append (box, GTK_WIDGET (priv->prefix));
  gtk_box_append (box, GTK_WIDGET (priv->center));
  gtk_box_append (box, GTK_WIDGET (priv->suffix));

  priv->overlay = g_object_new (GTK_TYPE_OVERLAY, NULL);
  gtk_overlay_set_child (priv->overlay, GTK_WIDGET (box));
  gtk_box_append (priv->box, GTK_WIDGET (priv->overlay));

  priv->progress_bar = g_object_new (GTK_TYPE_PROGRESS_BAR,
                                     "valign", GTK_ALIGN_END,
                                     "visible", FALSE,
                                     NULL);
  gtk_widget_add_css_class (GTK_WIDGET (priv->progress_bar), "osd");
  gtk_overlay_add_overlay (priv->overlay, GTK_WIDGET (priv->progress_bar));

  gesture = gtk_gesture_click_new ();
  g_signal_connect_object (gesture,
                           "released",
                           G_CALLBACK (panel_omni_bar_click_released_cb),
                           self,
                           G_CONNECT_SWAPPED);
  gtk_widget_add_controller (GTK_WIDGET (priv->box), GTK_EVENT_CONTROLLER (gesture));
}

#define GET_PRIORITY(w)   GPOINTER_TO_INT(g_object_get_data(G_OBJECT(w),"PRIORITY"))
#define SET_PRIORITY(w,i) g_object_set_data(G_OBJECT(w),"PRIORITY",GINT_TO_POINTER(i))

/**
 * panel_omni_bar_add_prefix:
 * @self: a #PanelOmniBar
 * @priority: the priority
 * @widget: (transfer none): the widget to add at the start.
 *
 * Add a widget at the start of the container, ordered by priority.
 * The highest the priority, the closest to the start.
 */
void
panel_omni_bar_add_prefix (PanelOmniBar *self,
                           int           priority,
                           GtkWidget    *widget)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);
  GtkWidget *sibling = NULL;

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));

  SET_PRIORITY (widget, priority);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->prefix));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (priority < GET_PRIORITY(child))
        break;
      sibling = child;
    }

  gtk_box_insert_child_after (priv->prefix, widget, sibling);
}

/**
 * panel_omni_bar_add_suffix:
 * @self: a #PanelOmniBar
 * @priority: the priority
 * @widget: (transfer none): the widget to add toward the end.
 *
 * Add a widget towards the end of the container, ordered by priority.
 * The highest the priority, the closest to the start.
 */
void
panel_omni_bar_add_suffix (PanelOmniBar *self,
                           int           priority,
                           GtkWidget    *widget)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);
  GtkWidget *sibling = NULL;

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));

  SET_PRIORITY (widget, priority);

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (priv->suffix));
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (priority < GET_PRIORITY(child))
        break;
      sibling = child;
    }

  gtk_box_insert_child_after (priv->suffix, widget, sibling);
}

/**
 * panel_omni_bar_remove:
 * @self: a #PanelOmniBar
 * @widget: The widget to remove.
 *
 * Removes a widget from the omni bar. Currently only prefix or suffix
 * widgets are supported.
 */
void
panel_omni_bar_remove (PanelOmniBar *self,
                       GtkWidget    *widget)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);
  GtkWidget *parent;

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));
  g_return_if_fail (GTK_IS_WIDGET (widget));

  parent = gtk_widget_get_parent (widget);

  if (parent == GTK_WIDGET (priv->suffix) ||
      parent == GTK_WIDGET (priv->prefix))
    {
      gtk_box_remove (GTK_BOX (parent), widget);
      return;
    }

  /* TODO: Support removing internal things */
}

static void
panel_omni_bar_add_child (GtkBuildable *buildable,
                          GtkBuilder   *builder,
                          GObject      *child,
                          const char   *type)
{
  PanelOmniBar *self = (PanelOmniBar *)buildable;

  g_assert (GTK_IS_BUILDABLE (buildable));
  g_assert (GTK_IS_BUILDER (builder));
  g_assert (G_IS_OBJECT (child));

  if (!GTK_IS_WIDGET (child))
    {
      g_critical ("Attempted to add a non-widget to %s, which is not supported",
                  G_OBJECT_TYPE_NAME (self));
      return;
    }

  if (g_strcmp0 (type, "suffix") == 0)
    panel_omni_bar_add_suffix (self, 0, GTK_WIDGET (child));
  else
    panel_omni_bar_add_prefix (self, 0, GTK_WIDGET (child));
}

static void
buildable_iface_init (GtkBuildableIface *iface)
{
  iface->add_child = panel_omni_bar_add_child;
}

static const char *
get_action_name (GtkActionable *actionable)
{
  PanelOmniBar *self = (PanelOmniBar *)actionable;
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  return gtk_actionable_get_action_name (GTK_ACTIONABLE (priv->button));
}

static void
set_action_name (GtkActionable *actionable,
                 const char    *action_name)
{
  PanelOmniBar *self = (PanelOmniBar *)actionable;
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  gtk_actionable_set_action_name (GTK_ACTIONABLE (priv->button), action_name);
}

static GVariant *
get_action_target (GtkActionable *actionable)
{
  PanelOmniBar *self = (PanelOmniBar *)actionable;
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  return gtk_actionable_get_action_target_value (GTK_ACTIONABLE (priv->button));
}

static void
set_action_target (GtkActionable *actionable,
                   GVariant      *action_target)
{
  PanelOmniBar *self = (PanelOmniBar *)actionable;
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  gtk_actionable_set_action_target_value (GTK_ACTIONABLE (priv->button), action_target);
}

static void
actionable_iface_init (GtkActionableInterface *iface)
{
  iface->get_action_name = get_action_name;
  iface->set_action_name = set_action_name;
  iface->get_action_target_value = get_action_target;
  iface->set_action_target_value = set_action_target;
}

/**
 * panel_omni_bar_get_progress:
 * @self: a #PanelOmniBar
 *
 * Gets the progress value displayed in the omni bar.
 *
 * Returns: the progress value.
 */
double
panel_omni_bar_get_progress (PanelOmniBar *self)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_OMNI_BAR (self), 0.0);

  return gtk_progress_bar_get_fraction (priv->progress_bar);
}

/**
 * panel_omni_bar_set_progress:
 * @self: a #PanelOmniBar
 * @progress: the progress value
 *
 * Sets the progress value displayed in the omni bar.
 */
void
panel_omni_bar_set_progress (PanelOmniBar *self,
                             double        progress)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));

  progress = CLAMP (progress, 0.0, 1.0);

  if (progress != panel_omni_bar_get_progress (self))
    {
      gtk_progress_bar_set_fraction (priv->progress_bar, progress);
      gtk_widget_set_visible (GTK_WIDGET (priv->progress_bar), progress > 0.0);
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_PROGRESS]);
    }
}

static gboolean
progress_bar_tick_cb (gpointer data)
{
  GtkProgressBar *progress = data;

  g_assert (GTK_IS_PROGRESS_BAR (progress));

  gtk_progress_bar_pulse (progress);
  gtk_widget_queue_draw (GTK_WIDGET (progress));

  return G_SOURCE_CONTINUE;
}

static void
progress_bar_stop_pulsing (GtkProgressBar *progress)
{
  guint tick_id;

  g_return_if_fail (GTK_IS_PROGRESS_BAR (progress));

  tick_id = GPOINTER_TO_UINT (g_object_get_data (G_OBJECT (progress), "PULSE_ID"));

  if (tick_id != 0)
    {
      g_source_remove (tick_id);
      g_object_set_data (G_OBJECT (progress), "PULSE_ID", NULL);
    }

  gtk_progress_bar_set_fraction (progress, 0.0);
}

static void
progress_bar_start_pulsing (GtkProgressBar *progress)
{
  guint tick_id;

  g_return_if_fail (GTK_IS_PROGRESS_BAR (progress));

  if (g_object_get_data (G_OBJECT (progress), "PULSE_ID"))
    return;

  gtk_progress_bar_set_fraction (progress, 0.0);
  gtk_progress_bar_set_pulse_step (progress, .5);

  /* We want lower than the frame rate, because that is all that is needed */
  tick_id = g_timeout_add_full (G_PRIORITY_LOW,
                                500,
                                progress_bar_tick_cb,
                                g_object_ref (progress),
                                g_object_unref);
  g_object_set_data (G_OBJECT (progress), "PULSE_ID", GUINT_TO_POINTER (tick_id));
  progress_bar_tick_cb (progress);
}


/**
 * panel_omni_bar_start_pulsing:
 * @self: a #PanelOmniBar
 *
 * Starts pulsing the omni bar. Use
 * @panel_omni_bar_stop_pulsing to stop.
 */
void
panel_omni_bar_start_pulsing (PanelOmniBar *self)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));

  progress_bar_start_pulsing (priv->progress_bar);
  gtk_widget_show (GTK_WIDGET (priv->progress_bar));
}

/**
 * panel_omni_bar_stop_pulsing:
 * @self: #PanelOmniBar
 *
 * Stops pulsing the omni bar, that was started with
 * @panel_omni_bar_start_pulsing.
 */
void
panel_omni_bar_stop_pulsing (PanelOmniBar *self)
{
  PanelOmniBarPrivate *priv = panel_omni_bar_get_instance_private (self);

  g_return_if_fail (PANEL_IS_OMNI_BAR (self));

  progress_bar_stop_pulsing (priv->progress_bar);
  gtk_widget_hide (GTK_WIDGET (priv->progress_bar));
}
