/* panel-workspace.c
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

#include "panel-action-muxer-private.h"
#include "panel-inhibitor-private.h"
#include "panel-workbench-private.h"
#include "panel-util-private.h"

typedef struct
{
  char *id;
  PanelActionMuxer *action_muxer;
} PanelWorkspacePrivate;

typedef struct
{
  const PanelAction *actions;
} PanelWorkspaceClassPrivate;

enum {
  PROP_0,
  PROP_ID,
  N_PROPS
};

G_DEFINE_TYPE_WITH_CODE (PanelWorkspace, panel_workspace, ADW_TYPE_APPLICATION_WINDOW,
                         G_ADD_PRIVATE (PanelWorkspace)
                         g_type_add_class_private (g_define_type_id,
                                                   sizeof (PanelWorkspaceClassPrivate));)

static GParamSpec *properties [N_PROPS];

static inline gpointer
panel_workspace_class_get_private (PanelWorkspaceClass *workspace_class)
{
  return G_TYPE_CLASS_GET_PRIVATE (workspace_class,
                                   PANEL_TYPE_WORKSPACE,
                                   PanelWorkspaceClassPrivate);
}

static void
panel_workspace_dispose (GObject *object)
{
  PanelWorkspace *self = (PanelWorkspace *)object;
  PanelWorkspacePrivate *priv = panel_workspace_get_instance_private (self);
  GtkWindowGroup *window_group;

  window_group = gtk_window_get_group (GTK_WINDOW (self));

  if (PANEL_IS_WORKBENCH (window_group))
    panel_workbench_remove_workspace (PANEL_WORKBENCH (window_group), self);

  g_clear_object (&priv->action_muxer);
  g_clear_pointer (&priv->id, g_free);

  G_OBJECT_CLASS (panel_workspace_parent_class)->dispose (object);
}

static void
panel_workspace_get_property (GObject    *object,
                              guint       prop_id,
                              GValue     *value,
                              GParamSpec *pspec)
{
  PanelWorkspace *self = PANEL_WORKSPACE (object);

  switch (prop_id)
    {
    case PROP_ID:
      g_value_set_string (value, panel_workspace_get_id (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_workspace_set_property (GObject      *object,
                              guint         prop_id,
                              const GValue *value,
                              GParamSpec   *pspec)
{
  PanelWorkspace *self = PANEL_WORKSPACE (object);

  switch (prop_id)
    {
    case PROP_ID:
      panel_workspace_set_id (self, g_value_get_string (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_workspace_class_init (PanelWorkspaceClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->dispose = panel_workspace_dispose;
  object_class->get_property = panel_workspace_get_property;
  object_class->set_property = panel_workspace_set_property;

  /**
   * PanelWorkspace:id:
   *
   * The "id" of the workspace.
   *
   * This is generally used by applications to help destinguish between
   * types of workspaces, particularly when saving session state.
   *
   * Since: 1.4
   */
  properties[PROP_ID] =
    g_param_spec_string ("id", NULL, NULL,
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);
}

static void
panel_workspace_init (PanelWorkspace *self)
{
}

const char *
panel_workspace_get_id (PanelWorkspace *self)
{
  PanelWorkspacePrivate *priv = panel_workspace_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WORKSPACE (self), NULL);

  return priv->id;
}

void
panel_workspace_set_id (PanelWorkspace *self,
                        const char     *id)
{
  PanelWorkspacePrivate *priv = panel_workspace_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WORKSPACE (self));

  if (panel_set_str (&priv->id, id))
    g_object_notify_by_pspec (G_OBJECT (self), properties[PROP_ID]);
}

static void
panel_workspace_class_add_action (PanelWorkspaceClass *workspace_class,
                                  PanelAction         *action)
{
  PanelWorkspaceClassPrivate *class_priv = panel_workspace_class_get_private (workspace_class);

  g_assert (PANEL_IS_WORKSPACE_CLASS (workspace_class));
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
 * panel_workspace_class_install_action:
 * @workspace_class: a `PanelWorkspaceClass`
 * @action_name: a prefixed action name, such as "project.open"
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
panel_workspace_class_install_action (PanelWorkspaceClass     *workspace_class,
                                      const char              *action_name,
                                      const char              *parameter_type,
                                      PanelActionActivateFunc  activate)
{
  PanelAction *action;

  g_return_if_fail (PANEL_IS_WORKSPACE_CLASS (workspace_class));
  g_return_if_fail (action_name != NULL);
  g_return_if_fail (activate != NULL);

  action = g_new0 (PanelAction, 1);
  action->owner = G_TYPE_FROM_CLASS (workspace_class);
  action->name = g_intern_string (action_name);
  if (parameter_type != NULL)
    action->parameter_type = g_variant_type_new (parameter_type);
  action->activate = (PanelActionActivateFunc)activate;

  panel_workspace_class_add_action (workspace_class, action);
}

/**
 * panel_workspace_find_from_widget:
 * @widget: a #GtkWidget
 *
 * Finds the workspace that contains @widget.
 *
 * Returns: (transfer none) (nullable): a #PanelWorkspace or %NULL
 *
 * Since: 1.4
 */
PanelWorkspace *
panel_workspace_find_from_widget (GtkWidget *widget)
{
  GtkWindow *transient_for;
  GtkRoot *root;

  g_return_val_if_fail (GTK_IS_WIDGET (widget), NULL);

  root = gtk_widget_get_root (widget);

  if (!GTK_IS_WINDOW (root))
    return NULL;

  if (PANEL_IS_WORKSPACE (root))
    return PANEL_WORKSPACE (root);

  transient_for = gtk_window_get_transient_for (GTK_WINDOW (root));

  if (transient_for != NULL)
    return panel_workspace_find_from_widget (GTK_WIDGET (transient_for));

  return NULL;
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
      g_critical ("Unable to use panel_workspace_class_install_property_action with property '%s:%s' of type '%s'",
                  g_type_name (pspec->owner_type), pspec->name, g_type_name (pspec->value_type));
      return NULL;
    }
}

/**
 * panel_workspace_class_install_property_action:
 * @workspace_class: a `GtkWorkspaceClass`
 * @action_name: name of the action
 * @property_name: name of the property in instances of @workspace_class
 *   or any parent class.
 *
 * Installs an action called @action_name on @workspace_class and
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
 *
 * Since: 1.4
 */
void
panel_workspace_class_install_property_action (PanelWorkspaceClass *workspace_class,
                                               const char          *action_name,
                                               const char          *property_name)
{
  const GVariantType *state_type;
  PanelAction *action;
  GParamSpec *pspec;

  g_return_if_fail (GTK_IS_WIDGET_CLASS (workspace_class));

  if (!(pspec = g_object_class_find_property (G_OBJECT_CLASS (workspace_class), property_name)))
    {
      g_critical ("Attempted to use non-existent property '%s:%s' for panel_workspace_class_install_property_action",
                  G_OBJECT_CLASS_NAME (workspace_class), property_name);
      return;
    }

  if (~pspec->flags & G_PARAM_READABLE || ~pspec->flags & G_PARAM_WRITABLE || pspec->flags & G_PARAM_CONSTRUCT_ONLY)
    {
      g_critical ("Property '%s:%s' used with panel_workspace_class_install_property_action must be readable, writable, and not construct-only",
                  G_OBJECT_CLASS_NAME (workspace_class), property_name);
      return;
    }

  state_type = determine_type (pspec);

  if (!state_type)
    return;

  action = g_new0 (PanelAction, 1);
  action->owner = G_TYPE_FROM_CLASS (workspace_class);
  action->name = g_intern_string (action_name);
  action->pspec = pspec;
  action->state_type = state_type;
  if (action->pspec->value_type != G_TYPE_BOOLEAN)
    action->parameter_type = action->state_type;

  panel_workspace_class_add_action (workspace_class, action);
}

PanelActionMuxer *
_panel_workspace_get_action_muxer (PanelWorkspace *self)
{
  PanelWorkspacePrivate *priv = panel_workspace_get_instance_private (self);

  if (priv->action_muxer == NULL)
    priv->action_muxer = panel_action_muxer_new ();

  return priv->action_muxer;
}

void
panel_workspace_action_set_enabled (PanelWorkspace *self,
                                    const char     *action_name,
                                    gboolean        enabled)
{
  PanelWorkspaceClassPrivate *class_priv;
  PanelActionMuxer *muxer;

  g_return_if_fail (PANEL_IS_WORKBENCH (self));
  g_return_if_fail (action_name != NULL);

  class_priv = panel_workspace_class_get_private (PANEL_WORKSPACE_GET_CLASS (self));
  muxer = _panel_workspace_get_action_muxer (self);

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
 * panel_workspace_get_workbench:
 * @self: a #PanelWorkspace
 *
 * Gets the #PanelWorkbench @self is a part of.
 *
 * Returns: (transfer none) (nullable): a #PanelWorkbench, or %NULL
 *
 * Since: 1.4
 */
PanelWorkbench *
panel_workspace_get_workbench (PanelWorkspace *self)
{
  GtkWindowGroup *window_group;

  g_return_val_if_fail (PANEL_IS_WORKSPACE (self), NULL);

  window_group = gtk_window_get_group (GTK_WINDOW (self));

  if (PANEL_IS_WORKBENCH (window_group))
    return PANEL_WORKBENCH (window_group);

  return NULL;
}

/**
 * panel_workspace_inhibit:
 * @self: a #PanelWorkspace
 * @flags: the inhibit flags
 * @reason: the reason for the inhibit
 *
 * Inhibits one or more particular actions in the session.
 *
 * When the resulting #PanelInhibitor releases it's last reference
 * the inhibitor will be dismissed. Alternatively, you may force the
 * release of the inhibit using panel_inhibitor_uninhibit().
 *
 * Returns: (transfer full) (nullable): a #PanelInhibitor or %NULL
 *
 * Since: 1.4
 */
PanelInhibitor *
panel_workspace_inhibit (PanelWorkspace             *self,
                         GtkApplicationInhibitFlags  flags,
                         const char                 *reason)
{
  GApplication *application;
  guint cookie;

  g_return_val_if_fail (PANEL_IS_WORKSPACE (self), NULL);
  g_return_val_if_fail (flags != 0, NULL);

  application = g_application_get_default ();
  if (!GTK_IS_APPLICATION (application))
    g_return_val_if_reached (NULL);

  cookie = gtk_application_inhibit (GTK_APPLICATION (application),
                                    GTK_WINDOW (self),
                                    flags,
                                    reason);

  if (cookie == 0)
    return NULL;

  return _panel_inhibitor_new (GTK_APPLICATION (application), cookie);
}
