/* panel-session-item.c
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

#include "panel-session-item-private.h"
#include "panel-util-private.h"

struct _PanelSessionItem
{
  GObject parent_instance;
  PanelPosition *position;
  char *module_name;
  char *id;
  char *workspace;
  char *type_hint;
  GHashTable *metadata;
};

enum {
  PROP_0,
  PROP_ID,
  PROP_MODULE_NAME,
  PROP_POSITION,
  PROP_TYPE_HINT,
  PROP_WORKSPACE,
  N_PROPS
};

G_DEFINE_FINAL_TYPE (PanelSessionItem, panel_session_item, G_TYPE_OBJECT)

static GParamSpec *properties [N_PROPS];

static void
panel_session_item_dispose (GObject *object)
{
  PanelSessionItem *self = (PanelSessionItem *)object;

  g_clear_object (&self->position);

  g_clear_pointer (&self->id, g_free);
  g_clear_pointer (&self->module_name, g_free);
  g_clear_pointer (&self->type_hint, g_free);
  g_clear_pointer (&self->workspace, g_free);
  g_clear_pointer (&self->metadata, g_hash_table_unref);

  G_OBJECT_CLASS (panel_session_item_parent_class)->dispose (object);
}

static void
panel_session_item_get_property (GObject    *object,
                                 guint       prop_id,
                                 GValue     *value,
                                 GParamSpec *pspec)
{
  PanelSessionItem *self = PANEL_SESSION_ITEM (object);

  switch (prop_id)
    {
    case PROP_ID:
      g_value_set_string (value, panel_session_item_get_id (self));
      break;

    case PROP_MODULE_NAME:
      g_value_set_string (value, panel_session_item_get_module_name (self));
      break;

    case PROP_POSITION:
      g_value_set_object (value, panel_session_item_get_position (self));
      break;

    case PROP_TYPE_HINT:
      g_value_set_string (value, panel_session_item_get_type_hint (self));
      break;

    case PROP_WORKSPACE:
      g_value_set_string (value, panel_session_item_get_workspace (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_session_item_set_property (GObject      *object,
                                 guint         prop_id,
                                 const GValue *value,
                                 GParamSpec   *pspec)
{
  PanelSessionItem *self = PANEL_SESSION_ITEM (object);

  switch (prop_id)
    {
    case PROP_ID:
      panel_session_item_set_id (self, g_value_get_string (value));
      break;

    case PROP_MODULE_NAME:
      panel_session_item_set_module_name (self, g_value_get_string (value));
      break;

    case PROP_POSITION:
      panel_session_item_set_position (self, g_value_get_object (value));
      break;

    case PROP_TYPE_HINT:
      panel_session_item_set_type_hint (self, g_value_get_string (value));
      break;

    case PROP_WORKSPACE:
      panel_session_item_set_workspace (self, g_value_get_string (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_session_item_class_init (PanelSessionItemClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->dispose = panel_session_item_dispose;
  object_class->get_property = panel_session_item_get_property;
  object_class->set_property = panel_session_item_set_property;

  properties [PROP_ID] =
    g_param_spec_string ("id", NULL, NULL, NULL,
                         (G_PARAM_READWRITE |
                          G_PARAM_EXPLICIT_NOTIFY |
                          G_PARAM_STATIC_STRINGS));

  properties [PROP_MODULE_NAME] =
    g_param_spec_string ("module-name", NULL, NULL, NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties [PROP_POSITION] =
    g_param_spec_object ("position", NULL, NULL,
                         PANEL_TYPE_POSITION,
                         (G_PARAM_READWRITE |
                          G_PARAM_EXPLICIT_NOTIFY |
                          G_PARAM_STATIC_STRINGS));

  properties [PROP_TYPE_HINT] =
    g_param_spec_string ("type-hint", NULL, NULL, NULL,
                         (G_PARAM_READWRITE |
                          G_PARAM_EXPLICIT_NOTIFY |
                          G_PARAM_STATIC_STRINGS));

  properties [PROP_WORKSPACE] =
    g_param_spec_string ("workspace", NULL, NULL, NULL,
                         (G_PARAM_READWRITE |
                          G_PARAM_EXPLICIT_NOTIFY |
                          G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);
}

static void
panel_session_item_init (PanelSessionItem *self)
{
}

/**
 * panel_session_item_get_id:
 * @self: a #PanelSessionItem
 *
 * Gets the id for the session item, if any.
 *
 * Returns: (nullable): a string containing the id; otherwise %NULL
 */
const char *
panel_session_item_get_id (PanelSessionItem *self)
{
  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), NULL);

  return self->id;
}

/**
 * panel_session_item_set_id:
 * @self: a #PanelSessionItem
 * @id: (nullable): an optional identifier for the item
 *
 * Sets the identifier for the item.
 *
 * The identifier should generally be global to the session as it would
 * not be expected to come across multiple items with the same id.
 */
void
panel_session_item_set_id (PanelSessionItem *self,
                           const char       *id)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));

  if (panel_set_str (&self->id, id))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ID]);
}

/**
 * panel_session_item_get_module_name:
 * @self: a #PanelSessionItem
 *
 * Gets the module-name that created an item.
 *
 * Returns: (nullable): a module-name or %NULL
 */
const char *
panel_session_item_get_module_name (PanelSessionItem *self)
{
  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), NULL);

  return self->module_name;
}

/**
 * panel_session_item_set_module_name:
 * @self: a #PanelSessionItem
 * @module_name: (nullable): the module name owning the item
 *
 * Sets the module-name for the session item.
 *
 * This is generally used to help determine which plugin created
 * the item when decoding them at project load time.
 */
void
panel_session_item_set_module_name (PanelSessionItem *self,
                                    const char       *module_name)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));

  if (panel_set_str (&self->module_name, module_name))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_MODULE_NAME]);
}

/**
 * panel_session_item_get_type_hint:
 * @self: a #PanelSessionItem
 *
 * Gets the type hint for an item.
 *
 * Returns: (nullable): a type-hint or %NULL
 */
const char *
panel_session_item_get_type_hint (PanelSessionItem *self)
{
  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), NULL);

  return self->type_hint;
}

/**
 * panel_session_item_set_type_hint:
 * @self: a #PanelSessionItem
 * @type_hint: (nullable): a type hint string for the item
 *
 * Sets the type-hint value for the item.
 *
 * This is generally used to help inflate the right version of
 * an object when loading session items.
 */
void
panel_session_item_set_type_hint (PanelSessionItem *self,
                                  const char       *type_hint)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));

  if (panel_set_str (&self->type_hint, type_hint))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_TYPE_HINT]);
}

/**
 * panel_session_item_get_workspace:
 * @self: a #PanelSessionItem
 *
 * Gets the workspace id for the item.
 *
 * Returns: (nullable): a workspace or %NULL
 */
const char *
panel_session_item_get_workspace (PanelSessionItem *self)
{
  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), NULL);

  return self->workspace;
}

/**
 * panel_session_item_set_workspace:
 * @self: a #PanelSessionItem
 * @workspace: (nullable): a workspace string for the item
 *
 * Sets the workspace id for the item.
 *
 * This is generally used to tie an item to a specific workspace.
 */
void
panel_session_item_set_workspace (PanelSessionItem *self,
                                  const char       *workspace)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));

  if (panel_set_str (&self->workspace, workspace))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_WORKSPACE]);
}

/**
 * panel_session_item_get_position:
 * @self: a #PanelSessionItem
 *
 * Gets the #PanelPosition for the item.
 *
 * Returns: (transfer none) (nullable): a #PanelPosition or %NULL
 */
PanelPosition *
panel_session_item_get_position (PanelSessionItem *self)
{
  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), NULL);

  return self->position;
}

/**
 * panel_session_item_set_position:
 * @self: a #PanelSessionItem
 * @position: (nullable): a #PanelPosition or %NULL
 *
 * Sets the position for @self, if any.
 */
void
panel_session_item_set_position (PanelSessionItem *self,
                                 PanelPosition    *position)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));
  g_return_if_fail (!position || PANEL_IS_POSITION (position));

  if (g_set_object (&self->position, position))
    g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_POSITION]);
}

/**
 * panel_session_item_set_metadata: (skip)
 * @self: a #PanelSessionItem
 *
 * A variadic helper to set metadata.
 *
 * The format should be identical to g_variant_new().
 */
void
panel_session_item_set_metadata (PanelSessionItem *self,
                                 const char        *key,
                                 const char        *format,
                                   ...)
{
  GVariant *value;
  va_list args;

  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));
  g_return_if_fail (key != NULL);

  va_start (args, format);
  value = g_variant_new_va (format, NULL, &args);
  va_end (args);

  g_return_if_fail (value != NULL);

  panel_session_item_set_metadata_value (self, key, value);
}

/**
 * panel_session_item_has_metadata:
 * @self: a #PanelSessionItem
 * @key: the name of the metadata
 * @value_type: (out) (nullable): a location for a #GVariantType or %NULL
 *
 * If the item contains a metadata value for @key.
 *
 * Checks if a value exists for a metadata key and retrieves the #GVariantType
 * for that key.
 *
 * Returns: %TRUE if @self contains metadata named @key and @value_type is set
 *   to the value's #GVariantType. Otherwise %FALSE and @value_type is unchanged.
 */
gboolean
panel_session_item_has_metadata (PanelSessionItem     *self,
                                 const char            *key,
                                 const GVariantType   **value_type)
{
  GVariant *value;
  gboolean ret = FALSE;

  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), FALSE);
  g_return_val_if_fail (key != NULL, FALSE);

  if ((value = panel_session_item_get_metadata_value (self, key, NULL)))
    {
      g_assert (!g_variant_is_floating (value));

      if (value_type != NULL)
        *value_type = g_variant_get_type (value);

      ret = TRUE;

      g_variant_unref (value);
    }

  return ret;
}

/**
 * panel_session_item_has_metadata_with_type:
 * @self: a #PanelSessionItem
 * @key: the metadata key
 * @expected_type: the #GVariantType to check for @key
 *
 * Checks if the item contains metadata @key with @expected_type.
 *
 * Returns: %TRUE if a value was found for @key matching @expected_typed;
 *   otherwise %FALSE is returned.
 */
gboolean
panel_session_item_has_metadata_with_type (PanelSessionItem    *self,
                                           const char           *key,
                                           const GVariantType   *expected_type)
{
  const GVariantType *value_type = NULL;

  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), FALSE);
  g_return_val_if_fail (key != NULL, FALSE);
  g_return_val_if_fail (expected_type != NULL, FALSE);

  if (panel_session_item_has_metadata (self, key, &value_type))
    return g_variant_type_equal (value_type, expected_type);

  return FALSE;
}

/**
 * panel_session_item_get_metadata: (skip)
 * @self: a #PanelSessionItem
 * @key: the key for the metadata value
 * @format: the format of the value
 *
 * Extract a metadata value matching @format.
 *
 * @format must not reference the #GVariant, which means you need to make
 * copies of data, such as "s" instead of "&s".
 *
 * Returns: %TRUE if @key was found with @format and parameters were set.
 */
gboolean
panel_session_item_get_metadata (PanelSessionItem *self,
                                 const char        *key,
                                 const char        *format,
                                   ...)
{
  GVariant *value;
  va_list args;

  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), FALSE);
  g_return_val_if_fail (key != NULL, FALSE);
  g_return_val_if_fail (format != NULL, FALSE);
  g_return_val_if_fail (g_variant_type_string_is_valid (format), FALSE);

  if (!(value = panel_session_item_get_metadata_value (self, key, NULL)))
    return FALSE;

  if (!g_variant_check_format_string (value, format, TRUE))
    return FALSE;

  va_start (args, format);
  g_variant_get_va (value, format, NULL, &args);
  va_end (args);

  g_variant_unref (value);

  return TRUE;
}

/**
 * panel_session_item_get_metadata_value:
 * @self: a #PanelSessionItem
 * @key: the metadata key
 * @expected_type: (nullable): a #GVariantType or %NULL
 *
 * Retrieves the metadata value for @key.
 *
 * If @expected_type is non-%NULL, any non-%NULL value returned from this
 * function will match @expected_type.
 *
 * Returns: (transfer full) (nullable): a non-floating #GVariant which should
 *   be released with g_variant_unref(); otherwise %NULL.
 */
GVariant *
panel_session_item_get_metadata_value (PanelSessionItem     *self,
                                       const char           *key,
                                       const GVariantType   *expected_type)
{
  GVariant *ret;

  g_return_val_if_fail (PANEL_IS_SESSION_ITEM (self), NULL);
  g_return_val_if_fail (key != NULL, NULL);

  if (self->metadata == NULL)
    return NULL;

  if ((ret = g_hash_table_lookup (self->metadata, key)))
    {
      if (expected_type == NULL || g_variant_is_of_type (ret, expected_type))
        return g_variant_ref (ret);
    }

  return NULL;
}

/**
 * panel_session_item_set_metadata_value:
 * @self: a #PanelSessionItem
 * @key: the metadata key
 * @value: (nullable): the value for @key or %NULL
 *
 * Sets the value for metadata @key.
 *
 * If @value is %NULL, the metadata key is unset.
 */
void
panel_session_item_set_metadata_value (PanelSessionItem *self,
                                       const char       *key,
                                       GVariant         *value)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));
  g_return_if_fail (key != NULL);

  if (value != NULL)
    {
      if G_UNLIKELY (self->metadata == NULL)
        self->metadata = g_hash_table_new_full (g_str_hash,
                                                g_str_equal,
                                                g_free,
                                                (GDestroyNotify)g_variant_unref);
      g_hash_table_insert (self->metadata,
                           g_strdup (key),
                           g_variant_ref_sink (value));
    }
  else
    {
      if (self->metadata != NULL)
        g_hash_table_remove (self->metadata, key);
    }
}

void
_panel_session_item_to_variant (PanelSessionItem  *self,
                                GVariantBuilder   *builder)
{
  g_return_if_fail (PANEL_IS_SESSION_ITEM (self));
  g_return_if_fail (builder != NULL);

  g_variant_builder_open (builder, G_VARIANT_TYPE ("v"));
  g_variant_builder_open (builder, G_VARIANT_TYPE ("a{sv}"));

  if (self->position != NULL)
    g_variant_builder_add_parsed (builder,
                                  "{'position',<%v>}",
                                  panel_position_to_variant (self->position));

  if (self->id != NULL)
    g_variant_builder_add_parsed (builder, "{'id',<%s>}", self->id);

  if (self->module_name != NULL)
    g_variant_builder_add_parsed (builder, "{'module-name',<%s>}", self->module_name);

  if (self->type_hint != NULL)
    g_variant_builder_add_parsed (builder, "{'type-hint',<%s>}", self->type_hint);

  if (self->workspace != NULL)
    g_variant_builder_add_parsed (builder, "{'workspace',<%s>}", self->workspace);

  if (self->metadata != NULL && g_hash_table_size (self->metadata) > 0)
    {
      GHashTableIter iter;
      const char *key;
      GVariant *value;

      g_variant_builder_open (builder, G_VARIANT_TYPE ("{sv}"));
      g_variant_builder_add (builder, "s", "metadata");
      g_variant_builder_open (builder, G_VARIANT_TYPE ("v"));
      g_variant_builder_open (builder, G_VARIANT_TYPE ("a{sv}"));

      g_hash_table_iter_init (&iter, self->metadata);
      while (g_hash_table_iter_next (&iter, (gpointer *)&key, (gpointer *)&value))
        g_variant_builder_add_parsed (builder, "{%s,<%v>}", key, value);

      g_variant_builder_close (builder);
      g_variant_builder_close (builder);
      g_variant_builder_close (builder);
    }

  g_variant_builder_close (builder);
  g_variant_builder_close (builder);
}

PanelSessionItem *
panel_session_item_new (void)
{
  return g_object_new (PANEL_TYPE_SESSION_ITEM, NULL);
}

PanelSessionItem *
_panel_session_item_new_from_variant (GVariant  *variant,
                                    GError   **error)
{
  GVariant *positionv = NULL;
  GVariant *metadatav = NULL;
  PanelSessionItem *self;

  g_return_val_if_fail (variant != NULL, NULL);
  g_return_val_if_fail (g_variant_is_of_type (variant, G_VARIANT_TYPE_VARDICT), NULL);

  self = g_object_new (PANEL_TYPE_SESSION_ITEM, NULL);

  g_variant_lookup (variant, "id", "s", &self->id);
  g_variant_lookup (variant, "module-name", "s", &self->module_name);
  g_variant_lookup (variant, "type-hint", "s", &self->type_hint);
  g_variant_lookup (variant, "workspace", "s", &self->workspace);

  if ((positionv = g_variant_lookup_value (variant, "position", NULL)))
    {
      GVariant *child = g_variant_get_variant (positionv);
      self->position = panel_position_new_from_variant (child);
      g_clear_pointer (&child, g_variant_unref);
    }

  if ((metadatav = g_variant_lookup_value (variant, "metadata", G_VARIANT_TYPE_VARDICT)))
    {
      GVariantIter iter;
      GVariant *value;
      char *key;

      g_variant_iter_init (&iter, metadatav);

      while (g_variant_iter_loop (&iter, "{sv}", &key, &value))
        {
          GVariant *unwrapped = g_variant_get_variant (value);
          panel_session_item_set_metadata_value (self, key, unwrapped);
          g_clear_pointer (&unwrapped, g_variant_unref);
        }
    }

  g_clear_pointer (&positionv, g_variant_unref);
  g_clear_pointer (&metadatav, g_variant_unref);

  return self;
}
