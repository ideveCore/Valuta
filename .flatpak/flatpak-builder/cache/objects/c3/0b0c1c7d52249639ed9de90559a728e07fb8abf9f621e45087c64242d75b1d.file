/* panel-gsettings-action-group.c
 *
 * Copyright 2022-2023 Christian Hergert <chergert@redhat.com>
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

#include "panel-gsettings-action-group.h"

struct _PanelGSettingsActionGroup
{
  GObject           parent_instance;
  GSettings        *settings;
  GSettingsSchema  *schema;
  char            **keys;
};

static void action_group_iface_init (GActionGroupInterface *iface);

G_DEFINE_FINAL_TYPE_WITH_CODE (PanelGSettingsActionGroup, panel_gsettings_action_group, G_TYPE_OBJECT,
                               G_IMPLEMENT_INTERFACE (G_TYPE_ACTION_GROUP, action_group_iface_init))

enum {
  PROP_0,
  PROP_SETTINGS,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

/**
 * panel_gsettings_action_group_new:
 * @settings: a #GSettings
 *
 * Creates a new #GActionGroup that exports @settings.
 *
 * Returns: (transfer full): an #PanelGSettingsActionGroup
 */
GActionGroup *
panel_gsettings_action_group_new (GSettings *settings)
{
  g_return_val_if_fail (G_IS_SETTINGS (settings), NULL);

  return g_object_new (PANEL_TYPE_GSETTINGS_ACTION_GROUP,
                       "settings", settings,
                       NULL);
}

static void
panel_gsettings_action_group_set_settings (PanelGSettingsActionGroup *self,
                                           GSettings                 *settings)
{
  g_assert (PANEL_IS_GSETTINGS_ACTION_GROUP (self));
  g_assert (self->settings == NULL);
  g_assert (self->schema == NULL);
  g_assert (self->keys == NULL);
  g_assert (G_IS_SETTINGS (settings));

  if (g_set_object (&self->settings, settings))
    {
      g_object_get (self->settings,
                    "settings-schema", &self->schema,
                    NULL);
      self->keys = g_settings_schema_list_keys (self->schema);
    }
}

static void
panel_gsettings_action_group_dispose (GObject *object)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)object;

  g_clear_object (&self->settings);
  g_clear_pointer (&self->schema, g_settings_schema_unref);

  G_OBJECT_CLASS (panel_gsettings_action_group_parent_class)->dispose (object);
}

static void
panel_gsettings_action_group_get_property (GObject    *object,
                                           guint       prop_id,
                                           GValue     *value,
                                           GParamSpec *pspec)
{
  PanelGSettingsActionGroup *self = PANEL_GSETTINGS_ACTION_GROUP (object);

  switch (prop_id)
    {
    case PROP_SETTINGS:
      g_value_set_object (value, self->settings);
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_gsettings_action_group_set_property (GObject      *object,
                                           guint         prop_id,
                                           const GValue *value,
                                           GParamSpec   *pspec)
{
  PanelGSettingsActionGroup *self = PANEL_GSETTINGS_ACTION_GROUP (object);

  switch (prop_id)
    {
    case PROP_SETTINGS:
      panel_gsettings_action_group_set_settings (self, g_value_get_object (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_gsettings_action_group_class_init (PanelGSettingsActionGroupClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->dispose = panel_gsettings_action_group_dispose;
  object_class->get_property = panel_gsettings_action_group_get_property;
  object_class->set_property = panel_gsettings_action_group_set_property;

  properties [PROP_SETTINGS] =
    g_param_spec_object ("settings", NULL, NULL,
                         G_TYPE_SETTINGS,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);
}

static void
panel_gsettings_action_group_init (PanelGSettingsActionGroup *self)
{
}

static gboolean
panel_gsettings_action_group_has_action (GActionGroup *group,
                                         const char   *action_name)
{
  return g_strv_contains ((const char * const *)PANEL_GSETTINGS_ACTION_GROUP (group)->keys, action_name);
}

static char **
panel_gsettings_action_group_list_actions (GActionGroup *group)
{
  return g_strdupv (PANEL_GSETTINGS_ACTION_GROUP (group)->keys);
}

static gboolean
panel_gsettings_action_group_get_action_enabled (GActionGroup *group,
                                                 const char   *action_name)
{
  return g_settings_is_writable (PANEL_GSETTINGS_ACTION_GROUP (group)->settings, action_name);
}

static GVariant *
panel_gsettings_action_group_get_action_state (GActionGroup *group,
                                               const char   *action_name)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)group;
  return g_settings_get_value (self->settings, action_name);
}

static GVariant *
panel_gsettings_action_group_get_action_state_hint (GActionGroup *group,
                                                    const char   *action_name)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)group;
  GSettingsSchemaKey *key = g_settings_schema_get_key (self->schema, action_name);
  GVariant *range = g_settings_schema_key_get_range (key);
  g_clear_pointer (&key, g_settings_schema_key_unref);
  return range;
}

static void
panel_gsettings_action_group_change_action_state (GActionGroup *group,
                                                  const char   *action_name,
                                                  GVariant     *value)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)group;
  GSettingsSchemaKey *key = g_settings_schema_get_key (self->schema, action_name);

  if (g_variant_is_of_type (value, g_settings_schema_key_get_value_type (key)) &&
      g_settings_schema_key_range_check (key, value))
    {
      GVariant *hold = g_variant_ref_sink (value);

      g_settings_set_value (self->settings, action_name, hold);
      g_action_group_action_state_changed (group, action_name, hold);

      g_clear_pointer (&hold, g_variant_unref);
    }

  g_clear_pointer (&key, g_settings_schema_key_unref);
}

static const GVariantType *
panel_gsettings_action_group_get_action_state_type (GActionGroup *group,
                                                    const char   *action_name)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)group;
  GSettingsSchemaKey *key = g_settings_schema_get_key (self->schema, action_name);
  GVariant *default_value = g_settings_schema_key_get_default_value (key);

  const GVariantType *type = g_variant_get_type (default_value);

  g_clear_pointer (&key, g_settings_schema_key_unref);
  g_clear_pointer (&default_value, g_variant_unref);

  return type;
}

static void
panel_gsettings_action_group_activate_action (GActionGroup *group,
                                              const char   *action_name,
                                              GVariant     *parameter)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)group;
  GSettingsSchemaKey *key = g_settings_schema_get_key (self->schema, action_name);
  GVariant* default_value = g_settings_schema_key_get_default_value (key);

  if (g_variant_is_of_type (default_value, G_VARIANT_TYPE_BOOLEAN))
    {
      GVariant *old;

      if (parameter != NULL)
        goto ret;

      old = panel_gsettings_action_group_get_action_state (group, action_name);
      parameter = g_variant_new_boolean (!g_variant_get_boolean (old));
      g_variant_unref (old);
    }

  g_action_group_change_action_state (group, action_name, parameter);

ret:
  g_clear_pointer (&key, g_settings_schema_key_unref);
  g_clear_pointer (&default_value, g_variant_unref);
}

static const GVariantType *
panel_gsettings_action_group_get_action_parameter_type (GActionGroup *group,
                                                        const char   *action_name)
{
  PanelGSettingsActionGroup *self = (PanelGSettingsActionGroup *)group;
  GSettingsSchemaKey *key = g_settings_schema_get_key (self->schema, action_name);
  GVariant *default_value = g_settings_schema_key_get_default_value (key);
  const GVariantType *type = g_variant_get_type (default_value);

  if (g_variant_type_equal (type, G_VARIANT_TYPE_BOOLEAN))
    type = NULL;

  g_clear_pointer (&default_value, g_variant_unref);
  g_clear_pointer (&key, g_settings_schema_key_unref);

  return type;
}

static void
action_group_iface_init (GActionGroupInterface *iface)
{
  iface->has_action = panel_gsettings_action_group_has_action;
  iface->list_actions = panel_gsettings_action_group_list_actions;
  iface->get_action_parameter_type = panel_gsettings_action_group_get_action_parameter_type;
  iface->get_action_enabled = panel_gsettings_action_group_get_action_enabled;
  iface->get_action_state = panel_gsettings_action_group_get_action_state;
  iface->get_action_state_hint = panel_gsettings_action_group_get_action_state_hint;
  iface->get_action_state_type = panel_gsettings_action_group_get_action_state_type;
  iface->change_action_state = panel_gsettings_action_group_change_action_state;
  iface->activate_action = panel_gsettings_action_group_activate_action;
}
