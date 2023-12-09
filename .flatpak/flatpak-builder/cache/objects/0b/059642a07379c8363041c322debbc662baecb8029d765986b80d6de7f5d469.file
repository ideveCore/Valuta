/* panel-workbench.c
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
#include "panel-workbench-private.h"
#include "panel-util-private.h"

typedef struct
{
  char *id;
  GQueue workspaces;
  PanelActionMuxer *action_muxer;
} PanelWorkbenchPrivate;

typedef struct
{
  const PanelAction *actions;
} PanelWorkbenchClassPrivate;

enum {
  PROP_0,
  PROP_ID,
  N_PROPS
};

enum {
  ACTIVATE,
  N_SIGNALS
};

G_DEFINE_TYPE_WITH_CODE (PanelWorkbench, panel_workbench, GTK_TYPE_WINDOW_GROUP,
                         G_ADD_PRIVATE (PanelWorkbench)
                         g_type_add_class_private (g_define_type_id,
                                                   sizeof (PanelWorkbenchClassPrivate));)

static GParamSpec *properties[N_PROPS];
static guint signals[N_SIGNALS];

static inline gpointer
panel_workbench_class_get_private (PanelWorkbenchClass *workbench_class)
{
  return G_TYPE_CLASS_GET_PRIVATE (workbench_class,
                                   PANEL_TYPE_WORKBENCH,
                                   PanelWorkbenchClassPrivate);
}

static void
panel_workbench_dispose (GObject *object)
{
  PanelWorkbench *self = (PanelWorkbench *)object;
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);

  while (priv->workspaces.head != NULL)
    panel_workbench_remove_workspace (self, g_queue_peek_head (&priv->workspaces));

  g_clear_object (&priv->action_muxer);
  g_clear_pointer (&priv->id, g_free);

  G_OBJECT_CLASS (panel_workbench_parent_class)->dispose (object);
}

static void
panel_workbench_get_property (GObject    *object,
                              guint       prop_id,
                              GValue     *value,
                              GParamSpec *pspec)
{
  PanelWorkbench *self = PANEL_WORKBENCH (object);

  switch (prop_id)
    {
    case PROP_ID:
      g_value_set_string (value, panel_workbench_get_id (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_workbench_set_property (GObject      *object,
                              guint         prop_id,
                              const GValue *value,
                              GParamSpec   *pspec)
{
  PanelWorkbench *self = PANEL_WORKBENCH (object);

  switch (prop_id)
    {
    case PROP_ID:
      panel_workbench_set_id (self, g_value_get_string (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_workbench_class_init (PanelWorkbenchClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->dispose = panel_workbench_dispose;
  object_class->get_property = panel_workbench_get_property;
  object_class->set_property = panel_workbench_set_property;

  signals[ACTIVATE] =
    g_signal_new ("activate",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST,
                  G_STRUCT_OFFSET (PanelWorkbenchClass, activate),
                  NULL, NULL,
                  NULL,
                  G_TYPE_NONE, 0);

  /**
   * PanelWorkbench:id:
   *
   * The "id" of the workbench.
   *
   * This is generally used by applications to help destinguish between
   * projects, so that the project-id matches the workbench-id.
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
panel_workbench_init (PanelWorkbench *self)
{
}

PanelWorkbench *
panel_workbench_new (void)
{
  return g_object_new (PANEL_TYPE_WORKBENCH, NULL);
}

const char *
panel_workbench_get_id (PanelWorkbench *self)
{
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);

  g_return_val_if_fail (PANEL_IS_WORKBENCH (self), NULL);

  return priv->id;
}

void
panel_workbench_set_id (PanelWorkbench *self,
                        const char     *id)
{
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WORKBENCH (self));

  if (panel_set_str (&priv->id, id))
    g_object_notify_by_pspec (G_OBJECT (self), properties[PROP_ID]);
}

static void
panel_workbench_class_add_action (PanelWorkbenchClass *workbench_class,
                                  PanelAction         *action)
{
  PanelWorkbenchClassPrivate *class_priv = panel_workbench_class_get_private (workbench_class);

  g_assert (PANEL_IS_WORKBENCH_CLASS (workbench_class));
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
 * panel_workbench_class_install_action:
 * @workbench_class: a `PanelWorkspaceClass`
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
panel_workbench_class_install_action (PanelWorkbenchClass     *workbench_class,
                                      const char              *action_name,
                                      const char              *parameter_type,
                                      PanelActionActivateFunc  activate)
{
  PanelAction *action;

  g_return_if_fail (PANEL_IS_WORKBENCH_CLASS (workbench_class));
  g_return_if_fail (action_name != NULL);
  g_return_if_fail (activate != NULL);

  action = g_new0 (PanelAction, 1);
  action->owner = G_TYPE_FROM_CLASS (workbench_class);
  action->name = g_intern_string (action_name);
  if (parameter_type != NULL)
    action->parameter_type = g_variant_type_new (parameter_type);
  action->activate = (PanelActionActivateFunc)activate;

  panel_workbench_class_add_action (workbench_class, action);
}

/**
 * panel_workbench_foreach_workspace:
 * @self: a #PanelWorkbench
 * @foreach_func: (scope call): a function to call for each workspace
 * @foreach_func_data: the data for the @foreach_func
 *
 * Calls @foreach_func for each workspace in the workbench.
 *
 * Since: 1.4
 */
void
panel_workbench_foreach_workspace (PanelWorkbench        *self,
                                   PanelWorkspaceForeach  foreach_func,
                                   gpointer               foreach_func_data)
{
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);
  GList *iter;

  g_return_if_fail (PANEL_IS_WORKBENCH (self));
  g_return_if_fail (foreach_func != NULL);

  iter = priv->workspaces.head;

  while (iter != NULL)
    {
      PanelWorkspace *workspace;

      workspace = iter->data;
      iter = iter->next;

      foreach_func (workspace, foreach_func_data);
    }
}

static void
panel_workbench_find_workspace_typed_cb (PanelWorkspace *workspace,
                                         gpointer        data)
{
  struct {
    PanelWorkspace *workspace;
    GType type;
  } *find_by_type = data;

  if (find_by_type->workspace == NULL &&
      g_type_is_a (G_OBJECT_TYPE (workspace), find_by_type->type))
    find_by_type->workspace = workspace;
}

/**
 * panel_workbench_find_workspace_typed:
 * @self: a #PanelWorkbench
 *
 * Locates a workspace in @self with a type matching @type.
 *
 * Returns: (transfer none) (nullable): a #PanelWorkspace or %NULL
 *
 * Since: 1.4
 */
PanelWorkspace *
panel_workbench_find_workspace_typed (PanelWorkbench *self,
                                      GType           type)
{
  struct {
    PanelWorkspace *workspace;
    GType type;
  } find_by_type;

  g_return_val_if_fail (PANEL_IS_WORKBENCH (self), NULL);
  g_return_val_if_fail (g_type_is_a (type, PANEL_TYPE_WORKSPACE), NULL);

  find_by_type.workspace = NULL;
  find_by_type.type = type;

  panel_workbench_foreach_workspace (self,
                                     panel_workbench_find_workspace_typed_cb,
                                     &find_by_type);

  return find_by_type.workspace;
}

/**
 * panel_workbench_find_from_widget:
 * @widget: a #GtkWidget
 *
 * Finds the workbench that contains @widget.
 *
 * Returns: (transfer none) (nullable): a #PanelWorkbench or %NULL
 *
 * Since: 1.4
 */
PanelWorkbench *
panel_workbench_find_from_widget (GtkWidget *widget)
{
  GtkWindowGroup *window_group;
  GtkRoot *root;

  g_return_val_if_fail (GTK_IS_WIDGET (widget), NULL);

  root = gtk_widget_get_root (widget);

  if (!GTK_IS_WINDOW (root))
    return NULL;

  window_group = gtk_window_get_group (GTK_WINDOW (root));

  if (!PANEL_IS_WORKBENCH (window_group))
    {
      GtkWindow *transient_for = gtk_window_get_transient_for (GTK_WINDOW (root));

      if (transient_for != NULL)
        return panel_workbench_find_from_widget (GTK_WIDGET (transient_for));
    }

  return NULL;
}

void
panel_workbench_activate (PanelWorkbench *self)
{
  g_return_if_fail (PANEL_IS_WORKBENCH (self));

  g_signal_emit (self, signals[ACTIVATE], 0);
}

void
panel_workbench_add_workspace (PanelWorkbench *self,
                               PanelWorkspace *workspace)
{
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);
  PanelActionMuxer *action_muxer;

  g_return_if_fail (PANEL_IS_WORKBENCH (self));
  g_return_if_fail (PANEL_IS_WORKSPACE (workspace));

  gtk_application_add_window (GTK_APPLICATION (g_application_get_default ()),
                              GTK_WINDOW (workspace));

  action_muxer = _panel_workbench_get_action_muxer (self);
  gtk_widget_insert_action_group (GTK_WIDGET (workspace),
                                  "workbench",
                                  G_ACTION_GROUP (action_muxer));
  g_queue_push_tail (&priv->workspaces, g_object_ref (workspace));
  gtk_window_group_add_window (GTK_WINDOW_GROUP (self), GTK_WINDOW (workspace));
}

void
panel_workbench_remove_workspace (PanelWorkbench *self,
                                  PanelWorkspace *workspace)
{
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);

  g_return_if_fail (PANEL_IS_WORKBENCH (self));
  g_return_if_fail (PANEL_IS_WORKSPACE (workspace));

  gtk_application_remove_window (GTK_APPLICATION (g_application_get_default ()),
                                 GTK_WINDOW (workspace));

  gtk_widget_insert_action_group (GTK_WIDGET (workspace), "workbench", NULL);
  gtk_window_group_remove_window (GTK_WINDOW_GROUP (self), GTK_WINDOW (workspace));
  if (g_queue_remove (&priv->workspaces, workspace))
    g_object_unref (workspace);
}

void
panel_workbench_focus_workspace (PanelWorkbench *self,
                                 PanelWorkspace *workspace)
{
  g_return_if_fail (PANEL_IS_WORKBENCH (self));
  g_return_if_fail (PANEL_IS_WORKSPACE (workspace));

  /* TODO: We need the last event time to do this properly. Until then,
   * we'll just fake some timing info to workaround wayland issues.
   *
   * NOTE: this may no longer be necessary, but keeping around for good
   * measure as part of the move to libpanel.
   */
  gtk_window_present_with_time (GTK_WINDOW (workspace), g_get_monotonic_time () / 1000L);
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
      g_critical ("Unable to use panel_workbench_class_install_property_action with property '%s:%s' of type '%s'",
                  g_type_name (pspec->owner_type), pspec->name, g_type_name (pspec->value_type));
      return NULL;
    }
}

/**
 * panel_workbench_class_install_property_action:
 * @workbench_class: a `GtkWorkbenchClass`
 * @action_name: name of the action
 * @property_name: name of the property in instances of @workbench_class
 *   or any parent class.
 *
 * Installs an action called @action_name on @workbench_class and
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
panel_workbench_class_install_property_action (PanelWorkbenchClass *workbench_class,
                                               const char          *action_name,
                                               const char          *property_name)
{
  const GVariantType *state_type;
  PanelAction *action;
  GParamSpec *pspec;

  g_return_if_fail (GTK_IS_WIDGET_CLASS (workbench_class));

  if (!(pspec = g_object_class_find_property (G_OBJECT_CLASS (workbench_class), property_name)))
    {
      g_critical ("Attempted to use non-existent property '%s:%s' for panel_workbench_class_install_property_action",
                  G_OBJECT_CLASS_NAME (workbench_class), property_name);
      return;
    }

  if (~pspec->flags & G_PARAM_READABLE || ~pspec->flags & G_PARAM_WRITABLE || pspec->flags & G_PARAM_CONSTRUCT_ONLY)
    {
      g_critical ("Property '%s:%s' used with panel_workbench_class_install_property_action must be readable, writable, and not construct-only",
                  G_OBJECT_CLASS_NAME (workbench_class), property_name);
      return;
    }

  state_type = determine_type (pspec);

  if (!state_type)
    return;

  action = g_new0 (PanelAction, 1);
  action->owner = G_TYPE_FROM_CLASS (workbench_class);
  action->name = g_intern_string (action_name);
  action->pspec = pspec;
  action->state_type = state_type;
  if (action->pspec->value_type != G_TYPE_BOOLEAN)
    action->parameter_type = action->state_type;

  panel_workbench_class_add_action (workbench_class, action);
}

PanelActionMuxer *
_panel_workbench_get_action_muxer (PanelWorkbench *self)
{
  PanelWorkbenchPrivate *priv = panel_workbench_get_instance_private (self);

  if (priv->action_muxer == NULL)
    priv->action_muxer = panel_action_muxer_new ();

  return priv->action_muxer;
}

void
panel_workbench_action_set_enabled (PanelWorkbench *self,
                                    const char     *action_name,
                                    gboolean        enabled)
{
  PanelWorkbenchClassPrivate *class_priv;
  PanelActionMuxer *muxer;

  g_return_if_fail (PANEL_IS_WORKBENCH (self));
  g_return_if_fail (action_name != NULL);

  class_priv = panel_workbench_class_get_private (PANEL_WORKBENCH_GET_CLASS (self));
  muxer = _panel_workbench_get_action_muxer (self);

  for (const PanelAction *iter = class_priv->actions; iter; iter = iter->next)
    {
      if (g_strcmp0 (iter->name, action_name) == 0)
        {
          panel_action_muxer_set_enabled (muxer, iter, enabled);
          break;
        }
    }
}
