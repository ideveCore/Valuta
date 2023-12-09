/* panel-settings.c
 *
 * Copyright 2015-2019 Christian Hergert <christian@hergert.me>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include "config.h"

#include <glib/gi18n.h>

#include <stdlib.h>

#include "panel-marshal.h"
#include "panel-settings.h"
#include "panel-layered-settings.h"
#include "panel-util-private.h"

/**
 * SECTION:panel-settings
 * @title: PanelSettings
 * @short_description: Settings with identifier-specific overrides
 *
 * This provides a #GSettings-like object that can have overrides for
 * specific identifiers.
 *
 * Typically, this is used for features like per-project overrides where
 * the #PanelSettings:identifier is a unique identifer for a project.
 *
 * It uses layers of #GSettings internally to retrieve modified settings
 * at the override level, then falling back to the default path (which
 * may or may not have a user-value itself).
 */

struct _PanelSettings
{
  GObject               parent_instance;
  PanelLayeredSettings *layered_settings;
  char                 *schema_id;
  char                 *schema_id_prefix;
  char                 *schema_id_prefix_nodot;
  char                 *identifier;
  char                 *path;
  char                 *path_prefix;
  char                 *path_suffix;
};

static void action_group_iface_init (GActionGroupInterface *iface);

G_DEFINE_FINAL_TYPE_WITH_CODE (PanelSettings, panel_settings, G_TYPE_OBJECT,
                               G_IMPLEMENT_INTERFACE (G_TYPE_ACTION_GROUP, action_group_iface_init))

enum {
  PROP_0,
  PROP_PATH,
  PROP_PATH_PREFIX,
  PROP_PATH_SUFFIX,
  PROP_IDENTIFIER,
  PROP_SCHEMA_ID,
  PROP_SCHEMA_ID_PREFIX,
  N_PROPS
};

enum {
  CHANGED,
  N_SIGNALS
};

static GParamSpec *properties [N_PROPS];
static guint signals [N_SIGNALS];

static const GVariantType *
_g_variant_type_intern (const GVariantType *type)
{
  char *str = NULL;

  if (type == NULL)
    return NULL;

  str = g_variant_type_dup_string (type);
  
  const GVariantType *interned_type = G_VARIANT_TYPE (g_intern_string (str));
  
  g_clear_pointer (&str, g_free);

  return interned_type;
}

static void
panel_settings_set_schema_id (PanelSettings *self,
                              const char    *schema_id)
{
  g_assert (PANEL_IS_SETTINGS (self));
  g_assert (schema_id != NULL);

  if (panel_set_str (&self->schema_id, schema_id))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_SCHEMA_ID]);
}

static void
panel_settings_layered_settings_changed_cb (PanelSettings        *self,
                                            const char           *key,
                                            PanelLayeredSettings *layered_settings)
{
  GVariant *value = NULL;

  g_assert (key != NULL);
  g_assert (PANEL_IS_LAYERED_SETTINGS (layered_settings));

  g_signal_emit (self, signals [CHANGED], g_quark_from_string (key), key);

  value = panel_layered_settings_get_value (self->layered_settings, key);
  g_action_group_action_state_changed (G_ACTION_GROUP (self), key, value);

  g_clear_pointer (&value, g_variant_unref);
}

char *
panel_settings_resolve_schema_path (const char *schema_id_prefix,
                                    const char *schema_id,
                                    const char *identifier,
                                    const char *path_prefix,
                                    const char *path_suffix)
{
  GSettingsSchema *schema = NULL;
  GSettingsSchemaSource *source;
  char *real_path_suffix = NULL;
  char *escaped = NULL;
  const char *schema_path;
  const char *suffix;

  g_return_val_if_fail (schema_id_prefix != NULL, NULL);
  g_return_val_if_fail (g_str_has_suffix (schema_id_prefix, "."), NULL);
  g_return_val_if_fail (schema_id != NULL, NULL);
  g_return_val_if_fail (path_prefix != NULL, NULL);
  g_return_val_if_fail (g_str_has_suffix (path_prefix, "/"), NULL);
  g_return_val_if_fail ((g_str_has_prefix (schema_id, schema_id_prefix) ||
                         g_str_equal (schema_id, schema_id_prefix)),
                        NULL);

  /* Normalize our path suffix if we were provided one */
  if (path_suffix != NULL && !g_str_has_suffix (path_suffix, "/"))
    path_suffix = real_path_suffix = g_strconcat (path_suffix, "/", NULL);

  source = g_settings_schema_source_get_default ();

  if (!(schema = g_settings_schema_source_lookup (source, schema_id, TRUE)))
    {
      g_critical ("Failed to locate schema %s", schema_id);
      g_clear_pointer (&escaped, g_free);
      g_clear_pointer (&real_path_suffix, g_free);
      g_clear_pointer (&schema, g_settings_schema_unref);
      return NULL;
    }

  if ((schema_path = g_settings_schema_get_path (schema)))
    {
      if (identifier != NULL)
        g_critical ("Attempt to resolve non-relocatable schema %s with identifier %s",
                    schema_id, identifier);
      g_clear_pointer (&escaped, g_free);
      g_clear_pointer (&real_path_suffix, g_free);
      g_clear_pointer (&schema, g_settings_schema_unref);
      return g_strdup (schema_path);
    }

  suffix = schema_id + strlen (schema_id_prefix);
  escaped = g_strdelimit (g_strdup (suffix), ".", '/');

  char *result;

  if (identifier != NULL)
    {
      result = g_strconcat (path_prefix, identifier, "/", escaped, "/", path_suffix, NULL);
    }
  else
    {
      result = g_strconcat (path_prefix, escaped, "/", path_suffix, NULL);
    }


  g_clear_pointer (&escaped, g_free);
  g_clear_pointer (&real_path_suffix, g_free);
  g_clear_pointer (&schema, g_settings_schema_unref);
  
  return result;
}

static void
panel_settings_constructed (GObject *object)
{
  PanelSettings *self = (PanelSettings *)object;
  GSettingsSchema *schema = NULL;
  GSettings *app_settings = NULL;
  gboolean relocatable;

  G_OBJECT_CLASS (panel_settings_parent_class)->constructed (object);

  if (self->schema_id == NULL || self->schema_id_prefix == NULL || self->path_prefix == NULL)
    g_error ("You must set %s :schema-id, :schema-id-prefix, and :path-prefix during construction",
             G_OBJECT_TYPE_NAME (self));

  self->schema_id_prefix_nodot = g_strdup (self->schema_id_prefix);
  if (self->schema_id_prefix_nodot[0])
    self->schema_id_prefix_nodot[strlen (self->schema_id_prefix_nodot)-1] = 0;

  if (!g_str_equal (self->schema_id, self->schema_id_prefix_nodot) &&
      !g_str_has_prefix (self->schema_id, self->schema_id_prefix))
    g_error ("You must use a schema prefixed with %s (%s)",
             self->schema_id_prefix, self->schema_id);

  if (self->path != NULL)
    {
      if (!g_str_has_prefix (self->path, self->path_prefix))
        g_error ("You must use a path that begins with %s", self->path_prefix);
      else if (!g_str_has_suffix (self->path, "/"))
        g_error ("Settings paths must end in /");
    }
  else
    {
      if (!(self->path = panel_settings_resolve_schema_path (self->schema_id_prefix,
                                                             self->schema_id,
                                                             NULL,
                                                             self->path_prefix,
                                                             self->path_suffix)))
        g_error ("Failed to generate application path for %s", self->schema_id);
    }

  /* Create settings for the app-level layer, we'll append it last */
  app_settings = g_settings_new_with_path (self->schema_id, self->path);
  g_object_get (app_settings, "settings-schema", &schema, NULL);
  relocatable = g_settings_schema_get_path (schema) == NULL;

  self->layered_settings = panel_layered_settings_new (self->schema_id, self->path);

  g_signal_connect_object (self->layered_settings,
                           "changed",
                           G_CALLBACK (panel_settings_layered_settings_changed_cb),
                           self,
                           G_CONNECT_SWAPPED);

  /* Add project layer if we need one */
  if (relocatable && self->identifier != NULL)
    {
      char *project_path = panel_settings_resolve_schema_path (self->schema_id_prefix,
                                                               self->schema_id,
                                                               self->identifier,
                                                               self->path_prefix,
                                                               self->path_suffix);

      if (project_path)
       {
          GSettings *project_settings = g_settings_new_with_path (self->schema_id, project_path);

          panel_layered_settings_append (self->layered_settings, project_settings);

          g_clear_pointer (&project_path, g_free);
          g_clear_object (&project_settings);
       }
    }

  /* Add our application global (user defaults) settings as fallbacks */
  panel_layered_settings_append (self->layered_settings, app_settings);

  g_clear_object (&app_settings);
  g_clear_pointer (&schema, g_settings_schema_unref);
}

static void
panel_settings_finalize (GObject *object)
{
  PanelSettings *self = (PanelSettings *)object;

  g_clear_object (&self->layered_settings);

  g_clear_pointer (&self->schema_id, g_free);
  g_clear_pointer (&self->schema_id_prefix, g_free);
  g_clear_pointer (&self->schema_id_prefix_nodot, g_free);
  g_clear_pointer (&self->identifier, g_free);
  g_clear_pointer (&self->path, g_free);
  g_clear_pointer (&self->path_prefix, g_free);
  g_clear_pointer (&self->path_suffix, g_free);

  G_OBJECT_CLASS (panel_settings_parent_class)->finalize (object);
}

static void
panel_settings_get_property (GObject    *object,
                           guint       prop_id,
                           GValue     *value,
                           GParamSpec *pspec)
{
  PanelSettings *self = PANEL_SETTINGS (object);

  switch (prop_id)
    {
    case PROP_PATH:
      g_value_set_string (value, self->path);
      break;

    case PROP_PATH_PREFIX:
      g_value_set_string (value, self->path_prefix);
      break;

    case PROP_PATH_SUFFIX:
      g_value_set_string (value, self->path_suffix);
      break;

    case PROP_IDENTIFIER:
      g_value_set_string (value, self->identifier);
      break;

    case PROP_SCHEMA_ID:
      g_value_set_string (value, panel_settings_get_schema_id (self));
      break;

    case PROP_SCHEMA_ID_PREFIX:
      g_value_set_string (value, self->schema_id_prefix);
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_settings_set_property (GObject      *object,
                           guint         prop_id,
                           const GValue *value,
                           GParamSpec   *pspec)
{
  PanelSettings *self = PANEL_SETTINGS (object);

  switch (prop_id)
    {
    case PROP_PATH:
      self->path = g_value_dup_string (value);
      break;

    case PROP_PATH_PREFIX:
      self->path_prefix = g_value_dup_string (value);
      break;

    case PROP_PATH_SUFFIX:
      self->path_suffix = g_value_dup_string (value);
      break;

    case PROP_IDENTIFIER:
      self->identifier = g_value_dup_string (value);
      break;

    case PROP_SCHEMA_ID:
      panel_settings_set_schema_id (self, g_value_get_string (value));
      break;

    case PROP_SCHEMA_ID_PREFIX:
      self->schema_id_prefix = g_value_dup_string (value);
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_settings_class_init (PanelSettingsClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->constructed = panel_settings_constructed;
  object_class->finalize = panel_settings_finalize;
  object_class->get_property = panel_settings_get_property;
  object_class->set_property = panel_settings_set_property;

  properties [PROP_PATH] =
    g_param_spec_string ("path",
                         "Path",
                         "The path to use for for app settings",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  properties [PROP_PATH_PREFIX] =
    g_param_spec_string ("path-prefix",
                         "Path Suffix",
                         "A path prefix to preprend when generating schema paths",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  properties [PROP_PATH_SUFFIX] =
    g_param_spec_string ("path-suffix",
                         "Path Suffix",
                         "A path suffix to append when generating schema paths",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelSettings:identifier:
   *
   * The "identifier" property is used to make unique paths.
   *
   * This might be a unique "project-id" for example, in an IDE.
   */
  properties [PROP_IDENTIFIER] =
    g_param_spec_string ("identifier",
                         "Identifier",
                         "The identifier used to unique'ify this settings instance",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  properties [PROP_SCHEMA_ID] =
    g_param_spec_string ("schema-id",
                         "Schema ID",
                         "Schema ID",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  properties [PROP_SCHEMA_ID_PREFIX] =
    g_param_spec_string ("schema-id-prefix",
                         "Schema ID Prefix",
                         "The prefix for schema-ids used when generating paths",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_CONSTRUCT_ONLY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  signals [CHANGED] =
    g_signal_new ("changed",
                  G_TYPE_FROM_CLASS (klass),
                  G_SIGNAL_RUN_LAST | G_SIGNAL_DETAILED,
                  0,
                  NULL, NULL,
                  panel_marshal_VOID__STRING,
                  G_TYPE_NONE,
                  1,
                  G_TYPE_STRING | G_SIGNAL_TYPE_STATIC_SCOPE);
  g_signal_set_va_marshaller (signals [CHANGED],
                              G_TYPE_FROM_CLASS (klass),
                              panel_marshal_VOID__STRINGv);
}

static void
panel_settings_init (PanelSettings *self)
{
}

PanelSettings *
panel_settings_new (const char *identifier,
                    const char *schema_id)
{
  g_return_val_if_fail (schema_id != NULL, NULL);

  return g_object_new (PANEL_TYPE_SETTINGS,
                       "identifier", identifier,
                       "schema-id", schema_id,
                       NULL);
}

PanelSettings *
panel_settings_new_with_path (const char *identifier,
                              const char *schema_id,
                              const char *path)
{
  g_return_val_if_fail (schema_id != NULL, NULL);

  return g_object_new (PANEL_TYPE_SETTINGS,
                       "identifier", identifier,
                       "schema-id", schema_id,
                       "path", path,
                       NULL);
}

const char *
panel_settings_get_schema_id (PanelSettings *self)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), NULL);

  return self->schema_id;
}

GVariant *
panel_settings_get_default_value (PanelSettings *self,
                                  const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), NULL);
  g_return_val_if_fail (key != NULL, NULL);

  return panel_layered_settings_get_default_value (self->layered_settings, key);
}

/**
 * panel_settings_get_user_value:
 * @self: a #PanelSettings
 * @key: the key to get the user value for
 *
 * Returns: (nullable) (transfer full): the user's value, if set
 */
GVariant *
panel_settings_get_user_value (PanelSettings *self,
                               const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), NULL);
  g_return_val_if_fail (key != NULL, NULL);

  return panel_layered_settings_get_user_value (self->layered_settings, key);
}

GVariant *
panel_settings_get_value (PanelSettings *self,
                          const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), NULL);
  g_return_val_if_fail (key != NULL, NULL);

  return panel_layered_settings_get_value (self->layered_settings, key);
}

void
panel_settings_set_value (PanelSettings *self,
                          const char    *key,
                          GVariant      *value)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);

  return panel_layered_settings_set_value (self->layered_settings, key, value);
}

gboolean
panel_settings_get_boolean (PanelSettings *self,
                            const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), FALSE);
  g_return_val_if_fail (key != NULL, FALSE);

  return panel_layered_settings_get_boolean (self->layered_settings, key);
}

double
panel_settings_get_double (PanelSettings *self,
                           const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), 0.0);
  g_return_val_if_fail (key != NULL, 0.0);

  return panel_layered_settings_get_double (self->layered_settings, key);
}

int
panel_settings_get_int (PanelSettings *self,
                        const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), 0);
  g_return_val_if_fail (key != NULL, 0);

  return panel_layered_settings_get_int (self->layered_settings, key);
}

char *
panel_settings_get_string (PanelSettings *self,
                           const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), NULL);
  g_return_val_if_fail (key != NULL, NULL);

  return panel_layered_settings_get_string (self->layered_settings, key);
}

guint
panel_settings_get_uint (PanelSettings *self,
                         const char    *key)
{
  g_return_val_if_fail (PANEL_IS_SETTINGS (self), 0);
  g_return_val_if_fail (key != NULL, 0);

  return panel_layered_settings_get_uint (self->layered_settings, key);
}

void
panel_settings_set_boolean (PanelSettings *self,
                            const char    *key,
                            gboolean       val)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);

  panel_layered_settings_set_boolean (self->layered_settings, key, val);
}

void
panel_settings_set_double (PanelSettings *self,
                           const char    *key,
                           double         val)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);

  panel_layered_settings_set_double (self->layered_settings, key, val);
}

void
panel_settings_set_int (PanelSettings *self,
                        const char    *key,
                        int            val)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);

  panel_layered_settings_set_int (self->layered_settings, key, val);
}

void
panel_settings_set_string (PanelSettings *self,
                           const char    *key,
                           const char    *val)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);

  panel_layered_settings_set_string (self->layered_settings, key, val);
}

void
panel_settings_set_uint (PanelSettings *self,
                         const char    *key,
                         guint          val)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);

  panel_layered_settings_set_uint (self->layered_settings, key, val);
}

void
panel_settings_bind (PanelSettings        *self,
                     const char           *key,
                     gpointer              object,
                     const char           *property,
                     GSettingsBindFlags    flags)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);
  g_return_if_fail (G_IS_OBJECT (object));
  g_return_if_fail (property != NULL);

  panel_layered_settings_bind (self->layered_settings, key, object, property, flags);
}

/**
 * panel_settings_bind_with_mapping:
 * @self: An #PanelSettings
 * @key: The settings key
 * @object: the object to bind to
 * @property: the property of @object to bind to
 * @flags: flags for the binding
 * @get_mapping: (allow-none) (scope notified): variant to value mapping
 * @set_mapping: (allow-none) (scope notified): value to variant mapping
 * @user_data: user data for @get_mapping and @set_mapping
 * @destroy: destroy function to cleanup @user_data.
 *
 * Like panel_settings_bind() but allows transforming to and from settings storage using
 * @get_mapping and @set_mapping transformation functions.
 *
 * Call panel_settings_unbind() to unbind the mapping.
 */
void
panel_settings_bind_with_mapping (PanelSettings             *self,
                                  const char                *key,
                                  gpointer                   object,
                                  const char                *property,
                                  GSettingsBindFlags         flags,
                                  GSettingsBindGetMapping    get_mapping,
                                  GSettingsBindSetMapping    set_mapping,
                                  gpointer                   user_data,
                                  GDestroyNotify             destroy)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (key != NULL);
  g_return_if_fail (G_IS_OBJECT (object));
  g_return_if_fail (property != NULL);

  panel_layered_settings_bind_with_mapping (self->layered_settings, key, object, property, flags,
                                          get_mapping, set_mapping, user_data, destroy);
}

void
panel_settings_unbind (PanelSettings *self,
                       const char    *property)
{
  g_return_if_fail (PANEL_IS_SETTINGS (self));
  g_return_if_fail (property != NULL);

  panel_layered_settings_unbind (self->layered_settings, property);
}

static gboolean
panel_settings_has_action (GActionGroup *group,
                           const char   *action_name)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  GStrv keys = panel_layered_settings_list_keys (self->layered_settings);
  gboolean result = g_strv_contains ((const char * const *)keys, action_name);

  g_clear_pointer (&keys, g_strfreev);
  return result;
}

static char **
panel_settings_list_actions (GActionGroup *group)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  return panel_layered_settings_list_keys (self->layered_settings);
}

static gboolean
panel_settings_get_action_enabled (GActionGroup *group,
                                   const char   *action_name)
{
  return TRUE;
}

static GVariant *
panel_settings_get_action_state (GActionGroup *group,
                                 const char   *action_name)
{
  PanelSettings *self = PANEL_SETTINGS (group);

  return panel_layered_settings_get_value (self->layered_settings, action_name);
}

static GVariant *
panel_settings_get_action_state_hint (GActionGroup *group,
                                      const char   *action_name)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  GSettingsSchemaKey *key = panel_layered_settings_get_key (self->layered_settings, action_name);
  GVariant *range = g_settings_schema_key_get_range (key);

  g_clear_pointer (&key, g_settings_schema_key_unref);
  return range;
}

static void
panel_settings_change_action_state (GActionGroup *group,
                                    const char   *action_name,
                                    GVariant     *value)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  GSettingsSchemaKey *key = panel_layered_settings_get_key (self->layered_settings, action_name);

  if (g_variant_is_of_type (value, g_settings_schema_key_get_value_type (key)) &&
      g_settings_schema_key_range_check (key, value))
    {
      GVariant* hold = g_variant_ref_sink (value);

      panel_layered_settings_set_value (self->layered_settings, action_name, hold);
      g_action_group_action_state_changed (group, action_name, hold);

      g_clear_pointer (&hold, g_variant_unref);
    }
  g_clear_pointer (&key, g_settings_schema_key_unref);
}

static const GVariantType *
panel_settings_get_action_state_type (GActionGroup *group,
                                      const char   *action_name)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  GSettingsSchemaKey *key = panel_layered_settings_get_key (self->layered_settings, action_name);
  const GVariantType *type = g_settings_schema_key_get_value_type (key);

  g_clear_pointer (&key, g_settings_schema_key_unref);
  return _g_variant_type_intern (type);
}

static void
panel_settings_activate_action (GActionGroup *group,
                                const char   *action_name,
                                GVariant     *parameter)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  GSettingsSchemaKey *key = panel_layered_settings_get_key (self->layered_settings, action_name);
  GVariant *default_value = g_settings_schema_key_get_default_value (key);

  if (g_variant_is_of_type (default_value, G_VARIANT_TYPE_BOOLEAN))
    {
      GVariant *old;

      if (parameter != NULL)
        goto ret;

      old = panel_settings_get_action_state (group, action_name);
      parameter = g_variant_new_boolean (!g_variant_get_boolean (old));
      g_clear_pointer (&old, g_variant_unref);
    }

  g_action_group_change_action_state (group, action_name, parameter);

ret:
  g_clear_pointer (&key, g_settings_schema_key_unref);
  g_clear_pointer (&default_value, g_variant_unref);
}

static const GVariantType *
panel_settings_get_action_parameter_type (GActionGroup *group,
                                          const char   *action_name)
{
  PanelSettings *self = PANEL_SETTINGS (group);
  GSettingsSchemaKey *key = panel_layered_settings_get_key (self->layered_settings, action_name);
  const GVariantType *type = g_settings_schema_key_get_value_type (key);

  if (g_variant_type_equal (type, G_VARIANT_TYPE_BOOLEAN))
    return NULL;

  g_clear_pointer (&key, g_settings_schema_key_unref);
  return _g_variant_type_intern (type);
}

static void
action_group_iface_init (GActionGroupInterface *iface)
{
  iface->has_action = panel_settings_has_action;
  iface->list_actions = panel_settings_list_actions;
  iface->get_action_parameter_type = panel_settings_get_action_parameter_type;
  iface->get_action_enabled = panel_settings_get_action_enabled;
  iface->get_action_state = panel_settings_get_action_state;
  iface->get_action_state_hint = panel_settings_get_action_state_hint;
  iface->get_action_state_type = panel_settings_get_action_state_type;
  iface->change_action_state = panel_settings_change_action_state;
  iface->activate_action = panel_settings_activate_action;
}

PanelSettings *
panel_settings_new_relocatable (const char *identifier,
                                const char *schema_id,
                                const char *schema_id_prefix,
                                const char *path_prefix,
                                const char *path_suffix)
{
  return g_object_new (PANEL_TYPE_SETTINGS,
                       "identifier", identifier,
                       "schema-id", schema_id,
                       "schema-id-prefix", schema_id_prefix,
                       "path-prefix", path_prefix,
                       "path-suffix", path_suffix,
                       NULL);
}

