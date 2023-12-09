/* panel-widget.c
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

/* GTK - The GIMP Toolkit
 * Copyright (C) 1995-1997 Peter Mattis, Spencer Kimball and Josh MacDonald
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library. If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * Modified by the GTK+ Team and others 1997-2000.  See the AUTHORS
 * file for a list of people on the GTK+ Team.  See the ChangeLog
 * files for a list of changes.  These files are distributed with
 * GTK+ at ftp://ftp.gtk.org/pub/gtk/.
 */

#include "config.h"

#include "panel-action-muxer-private.h"
#include "panel-dock-private.h"
#include "panel-dock-child-private.h"
#include "panel-frame-private.h"
#include "panel-position.h"
#include "panel-save-delegate.h"
#include "panel-util-private.h"
#include "panel-widget-private.h"

/**
 * PanelWidget:
 *
 * PanelWidget is the base widget class for widgets added to a
 * #PanelFrame. It can be use as-is or you can subclass it.
 */
typedef struct
{
  GtkWidget         *child;
  char              *title;
  char              *icon_name;
  GIcon             *icon;
  char              *id;
  char              *tooltip;
  GMenuModel        *menu_model;
  PanelSaveDelegate *save_delegate;
  PanelActionMuxer  *action_muxer;

  GtkWidget         *maximize_frame;
  GtkWidget         *maximize_dock_child;

  GQuark             kind;

  guint              busy_count;

  guint              reorderable : 1;
  guint              can_maximize : 1;
  guint              maximized : 1;
  guint              modified : 1;
  guint              needs_attention : 1;
  guint              saving : 1;
  guint              force_close : 1;
} PanelWidgetPrivate;

typedef struct
{
  const PanelAction *actions;
} PanelWidgetClassPrivate;

static void panel_widget_class_init_buildable (GtkBuildableIface *iface);
static void panel_widget_class_init           (PanelWidgetClass  *klass);
static void panel_widget_init                 (GTypeInstance     *instance,
                                               gpointer           g_class);

enum {
  PROP_0,
  PROP_BUSY,
  PROP_CAN_MAXIMIZE,
  PROP_CHILD,
  PROP_ICON,
  PROP_ICON_NAME,
  PROP_ID,
  PROP_MENU_MODEL,
  PROP_MODIFIED,
  PROP_NEEDS_ATTENTION,
  PROP_KIND,
  PROP_REORDERABLE,
  PROP_SAVE_DELEGATE,
  PROP_TITLE,
  PROP_TOOLTIP,
  N_PROPS
};

enum {
  GET_DEFAULT_FOCUS,
  PRESENTED,
  DESTROY,
  N_SIGNALS
};

static GParamSpec *properties [N_PROPS];
static guint       signals [N_SIGNALS];
static int         PanelWidget_private_offset;
static gpointer    panel_widget_parent_class;

static inline gpointer
panel_widget_get_instance_private (PanelWidget *self)
{
  return (G_STRUCT_MEMBER_P (self, PanelWidget_private_offset));
}

static inline gpointer
panel_widget_class_get_private (PanelWidgetClass *widget_class)
{
  return G_TYPE_CLASS_GET_PRIVATE (widget_class, PANEL_TYPE_WIDGET, PanelWidgetClassPrivate);
}

GType
panel_widget_get_type (void)
{
  static GType widget_type = 0;

  if G_UNLIKELY (widget_type == 0)
    {
      const GTypeInfo widget_info =
      {
        sizeof (PanelWidgetClass),
        NULL,
        NULL,
        (GClassInitFunc)panel_widget_class_init,
        NULL,
        NULL,
        sizeof (PanelWidget),
        0,
        panel_widget_init,
        NULL,
      };

      const GInterfaceInfo buildable_info =
      {
        (GInterfaceInitFunc)panel_widget_class_init_buildable,
        (GInterfaceFinalizeFunc)NULL,
        NULL /* interface data */
      };

      widget_type = g_type_register_static (GTK_TYPE_WIDGET,
                                            g_intern_static_string ("PanelWidget"),
                                            &widget_info,
                                            0);
      g_type_add_class_private (widget_type,
                                sizeof (PanelWidgetClassPrivate));
      PanelWidget_private_offset = g_type_add_instance_private (widget_type,
                                                                sizeof (PanelWidgetPrivate));
      g_type_add_interface_static (widget_type,
                                   GTK_TYPE_BUILDABLE,
                                   &buildable_info);
    }

  return widget_type;
}

static void
panel_widget_update_actions (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);
  gboolean can_maximize;
  gboolean can_save;

  g_assert (PANEL_IS_WIDGET (self));

  can_maximize = !priv->maximized &&
                 panel_widget_get_can_maximize (self);
  can_save = _panel_widget_can_save (self);

  panel_widget_action_set_enabled (self, "maximize", can_maximize);
  panel_widget_action_set_enabled (self, "save", can_save);
}

static void
panel_widget_maximize_action (GtkWidget  *widget,
                              const char *action_name,
                              GVariant   *param)
{
  panel_widget_maximize (PANEL_WIDGET (widget));
}

static void
panel_widget_save_cb (GObject      *object,
                      GAsyncResult *result,
                      gpointer      user_data)
{
  PanelSaveDelegate *save_delegate = (PanelSaveDelegate *)object;
  PanelWidget *self = user_data;
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);
  GError *error = NULL;

  g_assert (PANEL_IS_SAVE_DELEGATE (save_delegate));
  g_assert (G_IS_ASYNC_RESULT (result));
  g_assert (PANEL_IS_WIDGET (self));

  priv->saving = FALSE;

  if (!panel_save_delegate_save_finish (save_delegate, result, &error))
    {
      /* TODO: Request save delegate to format an error message to
       *       display to the user via adwaita infobar replacement.
       */
      g_warning ("Failed to save: %s", error->message);
      g_clear_error (&error);
    }

  panel_widget_update_actions (self);
  g_clear_object (&self);
}

static void
panel_widget_save_action (GtkWidget  *widget,
                          const char *action_name,
                          GVariant   *param)
{
  PanelWidget *self = (PanelWidget *)widget;
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (priv->save_delegate != NULL);
  g_return_if_fail (priv->saving == FALSE);

  priv->saving = TRUE;

  panel_save_delegate_save_async (priv->save_delegate,
                                  NULL,
                                  panel_widget_save_cb,
                                  g_object_ref (self));

  panel_widget_update_actions (self);
}

/**
 * panel_widget_new:
 *
 * Create a new #PanelWidget.
 *
 * Returns: a newly created #PanelWidget
 */
GtkWidget *
panel_widget_new (void)
{
  return g_object_new (PANEL_TYPE_WIDGET, NULL);
}

static void
panel_widget_measure (GtkWidget      *widget,
                      GtkOrientation  orientation,
                      int             for_size,
                      int            *minimum,
                      int            *natural,
                      int            *minimum_baseline,
                      int            *natural_baseline)
{
  PanelWidget *self = (PanelWidget *)widget;
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_assert (PANEL_IS_WIDGET (self));

  if (priv->child != NULL)
    gtk_widget_measure (priv->child, orientation, for_size, minimum, natural, minimum_baseline, natural_baseline);
}

static void
panel_widget_size_allocate (GtkWidget *widget,
                            int        width,
                            int        height,
                            int        baseline)
{
  PanelWidget *self = (PanelWidget *)widget;
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_assert (PANEL_IS_WIDGET (self));

  GTK_WIDGET_CLASS (panel_widget_parent_class)->size_allocate (widget, width, height, baseline);

  if (priv->child != NULL)
    gtk_widget_allocate (priv->child, width, height, baseline, NULL);
}

static gboolean
panel_widget_grab_focus (GtkWidget *widget)
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
panel_widget_constructed (GObject *object)
{
  PanelWidget *self = PANEL_WIDGET (object);
  PanelWidgetClass *widget_class = PANEL_WIDGET_GET_CLASS (self);
  PanelWidgetClassPrivate *class_priv = panel_widget_class_get_private (widget_class);
  PanelActionMuxer *muxer;

  G_OBJECT_CLASS (panel_widget_parent_class)->constructed (object);

  muxer = PANEL_ACTION_MUXER (_panel_widget_get_action_muxer (self));

  panel_action_muxer_connect_actions (muxer, self, class_priv->actions);
}

static void
panel_widget_dispose (GObject *object)
{
  PanelWidget *self = (PanelWidget *)object;
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  if (priv->action_muxer != NULL)
    {
      panel_action_muxer_remove_all (priv->action_muxer);
      g_clear_object (&priv->action_muxer);
    }

  g_clear_pointer (&priv->child, gtk_widget_unparent);
  g_clear_pointer (&priv->title, g_free);
  g_clear_pointer (&priv->icon_name, g_free);
  g_clear_object (&priv->icon);
  g_clear_pointer (&priv->id, g_free);
  g_clear_pointer (&priv->tooltip, g_free);
  g_clear_object (&priv->menu_model);
  g_clear_object (&priv->save_delegate);

  G_OBJECT_CLASS (panel_widget_parent_class)->dispose (object);
}

static void
panel_widget_get_property (GObject    *object,
                           guint       prop_id,
                           GValue     *value,
                           GParamSpec *pspec)
{
  PanelWidget *self = PANEL_WIDGET (object);

  switch (prop_id)
    {
    case PROP_BUSY:
      g_value_set_boolean (value, panel_widget_get_busy (self));
      break;

    case PROP_CAN_MAXIMIZE:
      g_value_set_boolean (value, panel_widget_get_can_maximize (self));
      break;

    case PROP_KIND:
      g_value_set_string (value, panel_widget_get_kind (self));
      break;

    case PROP_ICON:
      g_value_set_object (value, panel_widget_get_icon (self));
      break;

    case PROP_ICON_NAME:
      g_value_set_string (value, panel_widget_get_icon_name (self));
      break;

    case PROP_ID:
      g_value_set_string (value, panel_widget_get_id (self));
      break;

    case PROP_MENU_MODEL:
      g_value_set_object (value, panel_widget_get_menu_model (self));
      break;

    case PROP_MODIFIED:
      g_value_set_boolean (value, panel_widget_get_modified (self));
      break;

    case PROP_TITLE:
      g_value_set_string (value, panel_widget_get_title (self));
      break;

    case PROP_TOOLTIP:
      g_value_set_string (value, panel_widget_get_tooltip (self));
      break;

    case PROP_CHILD:
      g_value_set_object (value, panel_widget_get_child (self));
      break;

    case PROP_REORDERABLE:
      g_value_set_boolean (value, panel_widget_get_reorderable (self));
      break;

    case PROP_NEEDS_ATTENTION:
      g_value_set_boolean (value, panel_widget_get_needs_attention (self));
      break;

    case PROP_SAVE_DELEGATE:
      g_value_set_object (value, panel_widget_get_save_delegate (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_widget_set_property (GObject      *object,
                           guint         prop_id,
                           const GValue *value,
                           GParamSpec   *pspec)
{
  PanelWidget *self = PANEL_WIDGET (object);

  switch (prop_id)
    {
    case PROP_CAN_MAXIMIZE:
      panel_widget_set_can_maximize (self, g_value_get_boolean (value));
      break;

    case PROP_KIND:
      panel_widget_set_kind (self, g_value_get_string (value));
      break;

    case PROP_ICON:
      panel_widget_set_icon (self, g_value_get_object (value));
      break;

    case PROP_ICON_NAME:
      panel_widget_set_icon_name (self, g_value_get_string (value));
      break;

    case PROP_ID:
      panel_widget_set_id (self, g_value_get_string (value));
      break;

    case PROP_MENU_MODEL:
      panel_widget_set_menu_model (self, g_value_get_object (value));
      break;

    case PROP_MODIFIED:
      panel_widget_set_modified (self, g_value_get_boolean (value));
      break;

    case PROP_TITLE:
      panel_widget_set_title (self, g_value_get_string (value));
      break;

    case PROP_TOOLTIP:
      panel_widget_set_tooltip (self, g_value_get_string (value));
      break;

    case PROP_CHILD:
      panel_widget_set_child (self, g_value_get_object (value));
      break;

    case PROP_REORDERABLE:
      panel_widget_set_reorderable (self, g_value_get_boolean (value));
      break;

    case PROP_NEEDS_ATTENTION:
      panel_widget_set_needs_attention (self, g_value_get_boolean (value));
      break;

    case PROP_SAVE_DELEGATE:
      panel_widget_set_save_delegate (self, g_value_get_object (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_widget_class_init (PanelWidgetClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  g_type_class_adjust_private_offset (klass, &PanelWidget_private_offset);
  panel_widget_parent_class = g_type_class_peek_parent (klass);

  object_class->constructed = panel_widget_constructed;
  object_class->dispose = panel_widget_dispose;
  object_class->get_property = panel_widget_get_property;
  object_class->set_property = panel_widget_set_property;

  widget_class->grab_focus = panel_widget_grab_focus;
  widget_class->measure = panel_widget_measure;
  widget_class->size_allocate = panel_widget_size_allocate;

  properties [PROP_BUSY] =
    g_param_spec_boolean ("busy",
                          "Busy",
                          "If the widget is busy, such as loading or saving a file",
                          FALSE,
                          (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  properties [PROP_CAN_MAXIMIZE] =
    g_param_spec_boolean ("can-maximize",
                          "Can Maximize",
                          "Can Maximize",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:icon:
   *
   * The icon for this widget.
   */
  properties [PROP_ICON] =
    g_param_spec_object ("icon",
                         "Icon",
                         "A GIcon for the panel",
                         G_TYPE_ICON,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY |G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:icon-name:
   *
   * The icon name for this widget.
   */
  properties [PROP_ICON_NAME] =
    g_param_spec_string ("icon-name",
                         "Icon Name",
                         "Icon Name",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_ID] =
    g_param_spec_string ("id",
                         "Identifier",
                         "The identifier for the widget which can be used for saving state",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_KIND] =
    g_param_spec_string ("kind",
                         "Kind",
                         "The kind of panel widget",
                         "unknown",
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:menu-model:
   *
   * A menu model to display additional options for the page to the user via
   * menus.
   */
  properties [PROP_MENU_MODEL] =
    g_param_spec_object ("menu-model",
                         "Menu Model",
                         "Menu Model",
                         G_TYPE_MENU_MODEL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_MODIFIED] =
    g_param_spec_boolean ("modified",
                          "Modified",
                          "If the widget contains unsaved state",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:title:
   *
   * The title for this widget.
   */
  properties [PROP_TITLE] =
    g_param_spec_string ("title",
                         "Title",
                         "Title",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:tooltip:
   *
   * The tooltip to display in tabs for the widget.
   *
   * Since: 1.2
   */
  properties [PROP_TOOLTIP] =
    g_param_spec_string ("tooltip", NULL, NULL,
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:child:
   *
   * The child inside this widget.
   */
  properties [PROP_CHILD] =
    g_param_spec_object ("child",
                         "Child",
                         "Child",
                         GTK_TYPE_WIDGET,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_REORDERABLE] =
    g_param_spec_boolean ("reorderable",
                          "Reorderable",
                          "If the panel may be reordered",
                          TRUE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_NEEDS_ATTENTION] =
    g_param_spec_boolean ("needs-attention",
                          "Needs Attention",
                          "Needs Attention",
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelWidget:save-delegate:
   *
   * The save delegate attached to this widget.
   */
  properties [PROP_SAVE_DELEGATE] =
    g_param_spec_object ("save-delegate",
                         "Save Delegate",
                         "A save delegate to perform a save operation on the page",
                         PANEL_TYPE_SAVE_DELEGATE,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  /**
   * PanelWidget::get-default-focus:
   * @self: a #PanelWidget
   *
   * Gets the default widget to focus within the #PanelWidget. The first
   * handler for this signal is expected to return a widget, or %NULL if
   * there is nothing to focus.
   *
   * Returns: (transfer none) (nullable): a #GtkWidget within #PanelWidget
   *   or %NULL.
   */
  signals [GET_DEFAULT_FOCUS] =
    g_signal_new ("get-default-focus",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelWidgetClass, get_default_focus),
                  g_signal_accumulator_first_wins, NULL,
                  NULL,
                  GTK_TYPE_WIDGET, 0);

  /**
   * PanelWidget::presented:
   *
   * The "presented" signal is emitted when the widget is brought
   * to the front of a frame.
   */
  signals [PRESENTED] =
    g_signal_new ("presented",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelWidgetClass, presented),
                  NULL, NULL,
                  NULL,
                  G_TYPE_NONE, 0);

  gtk_widget_class_set_css_name (widget_class, "panelwidget");

  panel_widget_class_install_action (klass, "maximize", NULL, panel_widget_maximize_action);
  panel_widget_class_install_action (klass, "save", NULL, panel_widget_save_action);

  /* Ensure we have quarks for known types */
  g_quark_from_static_string (PANEL_WIDGET_KIND_ANY);
  g_quark_from_static_string (PANEL_WIDGET_KIND_UNKNOWN);
  g_quark_from_static_string (PANEL_WIDGET_KIND_DOCUMENT);
  g_quark_from_static_string (PANEL_WIDGET_KIND_UTILITY);
}

static void
panel_widget_init (GTypeInstance *instance,
                   gpointer       g_class)
{
  PanelWidget *self = PANEL_WIDGET (instance);
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  panel_widget_action_set_enabled (self, "maximize", FALSE);
  panel_widget_action_set_enabled (self, "save", FALSE);

  priv->kind = g_quark_from_static_string (PANEL_WIDGET_KIND_UNKNOWN);
  priv->reorderable = TRUE;
}

/**
 * panel_widget_get_icon_name:
 * @self: a #PanelWidget
 *
 * Gets the icon name for the widget.
 *
 * Returns: (transfer none) (nullable): the icon name or %NULL
 */
const char *
panel_widget_get_icon_name (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  if (priv->icon_name == NULL && G_IS_THEMED_ICON (priv->icon))
    {
      const char * const *names = g_themed_icon_get_names (G_THEMED_ICON (priv->icon));

      if (names != NULL && names[0] != NULL)
        return names[0];
    }

  return priv->icon_name;
}

/**
 * panel_widget_set_icon_name:
 * @self: a #PanelWidget
 * @icon_name: (transfer none) (nullable): the icon name or %NULL
 *
 * Sets the icon name for the widget.
 */
void
panel_widget_set_icon_name (PanelWidget *self,
                            const char  *icon_name)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (panel_set_str (&priv->icon_name, icon_name))
    {
      g_clear_object (&priv->icon);
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ICON_NAME]);
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ICON]);
    }
}

/**
 * panel_widget_get_icon:
 * @self: a #PanelWidget
 *
 * Gets a #GIcon for the widget.
 *
 * Returns: (transfer none) (nullable): a #GIcon or %NULL
 */
GIcon *
panel_widget_get_icon (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  if (priv->icon == NULL && priv->icon_name != NULL)
    priv->icon = g_themed_icon_new (priv->icon_name);

  return priv->icon;
}

/**
 * panel_widget_set_icon:
 * @self: a #PanelWidget
 * @icon: (transfer none) (nullable): a #GIcon or %NULL
 *
 * Sets a #GIcon for the widget.
 */
void
panel_widget_set_icon (PanelWidget *self,
                       GIcon       *icon)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (!icon || G_IS_ICON (icon));

  if (g_set_object (&priv->icon, icon))
    {
      if (priv->icon_name != NULL)
        {
          g_clear_pointer (&priv->icon_name, g_free);
          g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ICON_NAME]);
        }

      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ICON]);
    }
}

/**
 * panel_widget_get_id:
 * @self: a #PanelWidget
 *
 * Gets the id of the panel widget.
 *
 * Returns: (transfer none): The id of the panel widget.
 */
const char *
panel_widget_get_id (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return priv->id;
}

/**
 * panel_widget_set_id:
 * @self: a #PanelWidget
 * @id: (transfer none): the id to set for the panel widget.
 *
 * Sets the id of the panel widget.
 */
void
panel_widget_set_id (PanelWidget *self,
                     const char  *id)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (panel_set_str (&priv->id, id))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ID]);
}

/**
 * panel_widget_get_modified:
 * @self: a #PanelWidget
 *
 * Gets the modified status of a panel widget
 *
 * Returns: the modified status of the panel widget.
 */
gboolean
panel_widget_get_modified (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  return priv->modified;
}

/**
 * panel_widget_set_modified:
 * @self: a #PanelWidget
 * @modified: the modified status
 *
 * Sets the modified status of a panel widget.
 */
void
panel_widget_set_modified (PanelWidget *self,
                           gboolean     modified)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  modified = !!modified;

  if (priv->modified != modified)
    {
      priv->modified = modified;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_MODIFIED]);
      panel_widget_update_actions (self);
    }
}

/**
 * panel_widget_get_title:
 * @self: a #PanelWidget
 *
 * Gets the title for the widget.
 *
 * Returns: (transfer none) (nullable): the title or %NULL
 */
const char *
panel_widget_get_title (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return priv->title;
}

/**
 * panel_widget_set_title:
 * @self: a #PanelWidget
 * @title: (transfer none) (nullable): the title or %NULL
 *
 * Sets the title for the widget.
 */
void
panel_widget_set_title (PanelWidget *self,
                        const char  *title)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (panel_set_str (&priv->title, title))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_TITLE]);
}

/**
 * panel_widget_get_tooltip:
 * @self: a #PanelWidget
 *
 * Gets the tooltip for the widget.
 *
 * Returns: (transfer none) (nullable): the tooltip or %NULL
 */
const char *
panel_widget_get_tooltip (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return priv->tooltip;
}

/**
 * panel_widget_set_tooltip:
 * @self: a #PanelWidget
 * @tooltip: (transfer none) (nullable): the tooltip or %NULL
 *
 * Sets the tooltip for the widget to be displayed in tabs.
 */
void
panel_widget_set_tooltip (PanelWidget *self,
                          const char  *tooltip)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (panel_set_str (&priv->tooltip, tooltip))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_TOOLTIP]);
}

/**
 * panel_widget_get_child:
 * @self: a #PanelWidget
 *
 * Gets the child widget of the panel.
 *
 * Returns: (transfer none) (nullable): a #GtkWidget or %NULL
 */
GtkWidget *
panel_widget_get_child (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return priv->child;
}

/**
 * panel_widget_set_child:
 * @self: a #PanelWidget
 * @child: (nullable): a #GtkWidget or %NULL
 *
 * Sets the child widget of the panel.
 */
void
panel_widget_set_child (PanelWidget *self,
                        GtkWidget   *child)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (!child || GTK_IS_WIDGET (child));

  if (priv->child == child)
    return;

  if (priv->child)
    gtk_widget_unparent (priv->child);
  priv->child = child;
  if (priv->child)
    gtk_widget_set_parent (priv->child, GTK_WIDGET (self));

  g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CHILD]);
}

gboolean
panel_widget_get_reorderable (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  return priv->reorderable;
}

void
panel_widget_set_reorderable (PanelWidget *self,
                              gboolean     reorderable)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  reorderable = !!reorderable;

  if (reorderable != priv->reorderable)
    {
      priv->reorderable = reorderable;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_REORDERABLE]);
    }
}

gboolean
panel_widget_get_can_maximize (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  return priv->can_maximize;
}

void
panel_widget_set_can_maximize (PanelWidget *self,
                               gboolean     can_maximize)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  can_maximize = !!can_maximize;

  if (priv->can_maximize != can_maximize)
    {
      priv->can_maximize = can_maximize;
      panel_widget_update_actions (self);
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CAN_MAXIMIZE]);
    }
}

void
panel_widget_maximize (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);
  GtkWidget *dock;
  GtkWidget *dock_child;
  GtkWidget *frame;

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (priv->maximized)
    return;

  if (!panel_widget_get_can_maximize (self))
    return;

  if (!(frame = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME)) ||
      !(dock_child = gtk_widget_get_ancestor (frame, PANEL_TYPE_DOCK_CHILD)) ||
      !(dock = gtk_widget_get_ancestor (dock_child, PANEL_TYPE_DOCK)))
    return;

  priv->maximized = TRUE;

  panel_widget_update_actions (self);

  g_object_ref (self);

  g_set_weak_pointer (&priv->maximize_frame, frame);
  g_set_weak_pointer (&priv->maximize_dock_child, dock_child);

  panel_frame_remove (PANEL_FRAME (frame), self);

  _panel_dock_set_maximized (PANEL_DOCK (dock), self);

  g_object_unref (self);
}

void
panel_widget_unmaximize (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);
  GtkWidget *dock;

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (!priv->maximized)
    return;

  if (!(dock = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_DOCK)))
    return;

  priv->maximized = FALSE;

  panel_widget_update_actions (self);

  g_object_ref (self);

  _panel_dock_set_maximized (PANEL_DOCK (dock), NULL);
  _panel_dock_add_widget (PANEL_DOCK (dock),
                          PANEL_DOCK_CHILD (priv->maximize_dock_child),
                          PANEL_FRAME (priv->maximize_frame),
                          self);

  g_clear_weak_pointer (&priv->maximize_frame);
  g_clear_weak_pointer (&priv->maximize_dock_child);

  g_object_unref (self);
}

const char *
panel_widget_get_kind (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return g_quark_to_string (priv->kind);
}

/**
 * panel_widget_set_kind:
 * @self: a #PanelWidget
 * @kind: (nullable): the kind of this widget
 *
 * Sets the kind of the widget.
 */
void
panel_widget_set_kind (PanelWidget *self,
                       const char  *kind)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);
  GQuark qkind;

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if (kind == NULL)
    kind = PANEL_WIDGET_KIND_UNKNOWN;
  qkind = g_quark_from_static_string (kind);

  if (qkind != priv->kind)
    {
      priv->kind = qkind;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_KIND]);
    }
}

gboolean
panel_widget_get_needs_attention (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  return priv->needs_attention;
}

void
panel_widget_set_needs_attention (PanelWidget *self,
                                  gboolean     needs_attention)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  needs_attention = !!needs_attention;

  if (priv->needs_attention != needs_attention)
    {
      priv->needs_attention = needs_attention;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_NEEDS_ATTENTION]);
    }
}

gboolean
panel_widget_get_busy (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  return priv->busy_count > 0;
}

void
panel_widget_mark_busy (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  priv->busy_count++;

  if (priv->busy_count == 1)
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_BUSY]);
}

void
panel_widget_unmark_busy (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  priv->busy_count--;

  if (priv->busy_count == 0)
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_BUSY]);
}

/**
 * panel_widget_get_menu_model:
 * @self: a #PanelWidget
 *
 * Gets the #GMenuModel for the widget.
 *
 * #PanelFrameHeader may use this model to display additional options
 * for the page to the user via menus.
 *
 * Returns: (transfer none) (nullable): a #GMenuModel
 */
GMenuModel *
panel_widget_get_menu_model (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return priv->menu_model;
}

/**
 * panel_widget_set_menu_model:
 * @self: a #PanelWidget
 * @menu_model: (transfer none) (nullable): a #GMenuModel
 *
 * Sets the #GMenuModel for the widget.
 *
 * #PanelFrameHeader may use this model to display additional options
 * for the page to the user via menus.
 */
void
panel_widget_set_menu_model (PanelWidget *self,
                             GMenuModel  *menu_model)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (!menu_model || G_IS_MENU_MODEL (menu_model));

  if (g_set_object (&priv->menu_model, menu_model))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_MENU_MODEL]);
}

void
panel_widget_raise (PanelWidget *self)
{
  GtkWidget *frame;

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if ((frame = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME)))
    {
      GtkWidget *dock_child;
      GtkWidget *dock;

      panel_frame_set_visible_child (PANEL_FRAME (frame), self);

      if ((dock_child = gtk_widget_get_ancestor (frame, PANEL_TYPE_DOCK_CHILD)) &&
          (dock = gtk_widget_get_ancestor (dock_child, PANEL_TYPE_DOCK)))
        {
          switch (panel_dock_child_get_area (PANEL_DOCK_CHILD (dock_child)))
            {
            case PANEL_AREA_END:
              panel_dock_set_reveal_end (PANEL_DOCK (dock), TRUE);
              break;

            case PANEL_AREA_START:
              panel_dock_set_reveal_start (PANEL_DOCK (dock), TRUE);
              break;

            case PANEL_AREA_TOP:
              panel_dock_set_reveal_top (PANEL_DOCK (dock), TRUE);
              break;

            case PANEL_AREA_BOTTOM:
              panel_dock_set_reveal_bottom (PANEL_DOCK (dock), TRUE);
              break;

            case PANEL_AREA_CENTER:
            default:
              break;
            }
        }
    }
}

/**
 * panel_widget_get_default_focus:
 * @self: a #PanelWidget
 *
 * Discovers the widget that should be focused as the default widget
 * for the #PanelWidget.
 *
 * For example, if you want to focus a text editor by default, you might
 * return the #GtkTextView inside your widgetry.
 *
 * Returns: (transfer none) (nullable): the default widget to focus within
 *   the #PanelWidget.
 */
GtkWidget *
panel_widget_get_default_focus (PanelWidget *self)
{
  GtkWidget *default_focus = NULL;

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  g_signal_emit (self, signals [GET_DEFAULT_FOCUS], 0, &default_focus);

  g_return_val_if_fail (default_focus == NULL ||
                        GTK_WIDGET (self) == default_focus ||
                        gtk_widget_is_ancestor (default_focus, GTK_WIDGET (self)),
                        NULL);

  return default_focus;
}

gboolean
panel_widget_focus_default (PanelWidget *self)
{
  GtkWidget *default_focus;

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  if ((default_focus = panel_widget_get_default_focus (self)))
    return gtk_widget_grab_focus (default_focus);

  return FALSE;
}

static void
panel_widget_add_child (GtkBuildable *buildable,
                        GtkBuilder   *builder,
                        GObject      *child,
                        const char   *type)
{
  g_assert (PANEL_IS_WIDGET (buildable));
  g_assert (GTK_IS_BUILDER (builder));
  g_assert (G_IS_OBJECT (child));

  if (GTK_IS_WIDGET (child))
    panel_widget_set_child (PANEL_WIDGET (buildable), GTK_WIDGET (child));
}

static void
panel_widget_class_init_buildable (GtkBuildableIface *iface)
{
  iface->add_child = panel_widget_add_child;
}

/**
 * panel_widget_get_save_delegate:
 * @self: a #PanelWidget
 *
 * Gets the #PanelWidget:save-delegate property.
 *
 * The save delegate may be used to perform save operations on the
 * content within the widget.
 *
 * Document editors might use this to save the file to disk.
 *
 * Returns: (transfer none) (nullable): a #PanelSaveDelegate or %NULL
 */
PanelSaveDelegate *
panel_widget_get_save_delegate (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  return priv->save_delegate;
}

static void
panel_widget_save_delegate_notify_is_draft_cb (PanelWidget       *self,
                                               GParamSpec        *pspec,
                                               PanelSaveDelegate *save_delegate)
{
  g_assert (PANEL_IS_WIDGET (self));
  g_assert (PANEL_IS_SAVE_DELEGATE (save_delegate));

  panel_widget_update_actions (self);
}

/**
 * panel_widget_set_save_delegate:
 * @self: a #PanelWidget
 * @save_delegate: (transfer none) (nullable): a #PanelSaveDelegate or %NULL
 *
 * Sets the #PanelWidget:save-delegate property.
 *
 * The save delegate may be used to perform save operations on the
 * content within the widget.
 *
 * Document editors might use this to save the file to disk.
 */
void
panel_widget_set_save_delegate (PanelWidget       *self,
                                PanelSaveDelegate *save_delegate)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (!save_delegate || PANEL_IS_SAVE_DELEGATE (save_delegate));

  if (g_set_object (&priv->save_delegate, save_delegate))
    {
      g_signal_connect_object (save_delegate,
                               "notify::is-draft",
                               G_CALLBACK (panel_widget_save_delegate_notify_is_draft_cb),
                               self,
                               G_CONNECT_SWAPPED);
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_SAVE_DELEGATE]);
      panel_widget_update_actions (self);
    }
}

gboolean
_panel_widget_can_discard (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  if (priv->save_delegate != NULL &&
      !panel_widget_get_modified (self) &&
      panel_save_delegate_get_is_draft (priv->save_delegate))
    return TRUE;

  return FALSE;
}

gboolean
_panel_widget_can_save (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WIDGET (self), FALSE);

  if (priv->saving)
    return FALSE;

  if (priv->force_close)
    return FALSE;

  if (priv->save_delegate == NULL)
    return FALSE;

  if (!priv->modified)
    {
      /* We want to allow saving drafts, even if they're empty */
      if (!panel_save_delegate_get_is_draft (priv->save_delegate))
        return FALSE;
    }

  return TRUE;
}

void
panel_widget_close (PanelWidget *self)
{
  GtkWidget *frame;

  g_return_if_fail (PANEL_IS_WIDGET (self));

  if ((frame = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME)))
    _panel_frame_request_close (PANEL_FRAME (frame), self);
}

/**
 * panel_widget_force_close:
 * @self: a #PanelWidget
 *
 * Closes the widget without any save dialogs.
 */
void
panel_widget_force_close (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WIDGET (self));

  priv->force_close = TRUE;

  panel_widget_close (self);
}

void
_panel_widget_emit_presented (PanelWidget *self)
{
  g_return_if_fail (PANEL_IS_WIDGET (self));

  g_signal_emit (self, signals [PRESENTED], 0);
}

PanelActionMuxer *
_panel_widget_get_action_muxer (PanelWidget *self)
{
  PanelWidgetPrivate *priv = panel_widget_get_instance_private (self);

  if (priv->action_muxer == NULL)
    priv->action_muxer = panel_action_muxer_new ();

  return priv->action_muxer;
}

void
panel_widget_insert_action_group (PanelWidget  *self,
                                  const char   *prefix,
                                  GActionGroup *group)
{
  PanelActionMuxer *muxer;

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (prefix != NULL);

  if ((muxer = _panel_widget_get_action_muxer (self)))
    panel_action_muxer_insert_action_group (muxer, prefix, group);
}

static void
panel_widget_class_add_action (PanelWidgetClass *widget_class,
                               PanelAction      *action)
{
  PanelWidgetClassPrivate *class_priv = panel_widget_class_get_private (widget_class);

  g_assert (PANEL_IS_WIDGET_CLASS (widget_class));
  g_assert (action != NULL);
  g_assert (action->next == NULL);
  g_assert (action->position == 0);

  /* Precalculate action "position". To be stable this is the
   * number of items from the end.
   */
  for (const PanelAction *iter = class_priv->actions;
       iter != NULL;
       iter = iter->next)
    action->position++;

  action->next = class_priv->actions;
  class_priv->actions = action;
}

/**
 * panel_widget_class_install_action:
 * @widget_class: a `PanelWidgetClass`
 * @action_name: a prefixed action name, such as "clipboard.paste"
 * @parameter_type: (nullable): the parameter type
 * @activate: (scope notified): callback to use when the action is activated
 *
 * This should be called at class initialization time to specify
 * actions to be added for all instances of this class.
 *
 * Actions installed by this function are stateless. The only state
 * they have is whether they are enabled or not.
 */
void
panel_widget_class_install_action (PanelWidgetClass            *widget_class,
                                   const char                  *action_name,
                                   const char                  *parameter_type,
                                   GtkWidgetActionActivateFunc  activate)
{
  PanelAction *action;

  g_return_if_fail (PANEL_IS_WIDGET_CLASS (widget_class));
  g_return_if_fail (action_name != NULL);
  g_return_if_fail (activate != NULL);

  action = g_new0 (PanelAction, 1);
  action->owner = G_TYPE_FROM_CLASS (widget_class);
  action->name = g_intern_string (action_name);
  if (parameter_type != NULL)
    action->parameter_type = g_variant_type_new (parameter_type);
  action->activate = (PanelActionActivateFunc)activate;

  panel_widget_class_add_action (widget_class, action);
}

static const GVariantType *
determine_type (GParamSpec *pspec)
{
  if (G_TYPE_IS_ENUM (pspec->value_type))
    return G_VARIANT_TYPE_STRING;

  switch (pspec->value_type)
    {
    case G_TYPE_BOOLEAN:
      return G_VARIANT_TYPE_BOOLEAN;

    case G_TYPE_INT:
      return G_VARIANT_TYPE_INT32;

    case G_TYPE_UINT:
      return G_VARIANT_TYPE_UINT32;

    case G_TYPE_DOUBLE:
    case G_TYPE_FLOAT:
      return G_VARIANT_TYPE_DOUBLE;

    case G_TYPE_STRING:
      return G_VARIANT_TYPE_STRING;

    default:
      g_critical ("Unable to use panel_widget_class_install_property_action with property '%s:%s' of type '%s'",
                  g_type_name (pspec->owner_type), pspec->name, g_type_name (pspec->value_type));
      return NULL;
    }
}

/**
 * panel_widget_class_install_property_action:
 * @widget_class: a `GtkWidgetClass`
 * @action_name: name of the action
 * @property_name: name of the property in instances of @widget_class
 *   or any parent class.
 *
 * Installs an action called @action_name on @widget_class and
 * binds its state to the value of the @property_name property.
 *
 * This function will perform a few santity checks on the property selected
 * via @property_name. Namely, the property must exist, must be readable,
 * writable and must not be construct-only. There are also restrictions
 * on the type of the given property, it must be boolean, int, unsigned int,
 * double or string. If any of these conditions are not met, a critical
 * warning will be printed and no action will be added.
 *
 * The state type of the action matches the property type.
 *
 * If the property is boolean, the action will have no parameter and
 * toggle the property value. Otherwise, the action will have a parameter
 * of the same type as the property.
 */
void
panel_widget_class_install_property_action (PanelWidgetClass *widget_class,
                                            const char       *action_name,
                                            const char       *property_name)
{
  const GVariantType *state_type;
  PanelAction *action;
  GParamSpec *pspec;

  g_return_if_fail (GTK_IS_WIDGET_CLASS (widget_class));

  if (!(pspec = g_object_class_find_property (G_OBJECT_CLASS (widget_class), property_name)))
    {
      g_critical ("Attempted to use non-existent property '%s:%s' for panel_widget_class_install_property_action",
                  G_OBJECT_CLASS_NAME (widget_class), property_name);
      return;
    }

  if (~pspec->flags & G_PARAM_READABLE || ~pspec->flags & G_PARAM_WRITABLE || pspec->flags & G_PARAM_CONSTRUCT_ONLY)
    {
      g_critical ("Property '%s:%s' used with panel_widget_class_install_property_action must be readable, writable, and not construct-only",
                  G_OBJECT_CLASS_NAME (widget_class), property_name);
      return;
    }

  state_type = determine_type (pspec);

  if (!state_type)
    return;

  action = g_new0 (PanelAction, 1);
  action->owner = G_TYPE_FROM_CLASS (widget_class);
  action->name = g_intern_string (action_name);
  action->pspec = pspec;
  action->state_type = state_type;
  if (action->pspec->value_type != G_TYPE_BOOLEAN)
    action->parameter_type = action->state_type;

  panel_widget_class_add_action (widget_class, action);
}

void
panel_widget_action_set_enabled (PanelWidget *self,
                                 const char  *action_name,
                                 gboolean     enabled)
{
  PanelWidgetClassPrivate *class_priv;
  PanelActionMuxer *muxer;

  g_return_if_fail (PANEL_IS_WIDGET (self));
  g_return_if_fail (action_name != NULL);

  class_priv = panel_widget_class_get_private (PANEL_WIDGET_GET_CLASS (self));
  muxer = _panel_widget_get_action_muxer (self);

  for (const PanelAction *iter = class_priv->actions; iter; iter = iter->next)
    {
      if (g_strcmp0 (iter->name, action_name) == 0)
        {
          panel_action_muxer_set_enabled (muxer, iter, enabled);
          break;
        }
    }
}

/**
 * panel_widget_get_position:
 * @self: a #PanelWidget
 *
 * Gets teh position of the widget within the dock.
 *
 * Returns: (transfer full) (nullable): a #PanelPosition or %NULL if the
 *   widget isn't within a #PanelFrame.
 */
PanelPosition *
panel_widget_get_position (PanelWidget *self)
{
  PanelFrame *frame;
  PanelPosition *position;
  guint n_pages;

  g_return_val_if_fail (PANEL_IS_WIDGET (self), NULL);

  if (!(frame = PANEL_FRAME (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME))))
    return NULL;

  position = panel_frame_get_position (frame);
  n_pages = panel_frame_get_n_pages (frame);

  for (guint i = 0; i < n_pages; i++)
    {
      if (panel_frame_get_page (frame, i) == self)
        {
          panel_position_set_depth (position, i);
          break;
        }
    }

  return g_steal_pointer (&position);
}
