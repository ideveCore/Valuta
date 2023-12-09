/* panel-session.c
 *
 * Copyright 2022 Christian Hergert <chergert@redhat.com>
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

#include <gio/gio.h>

#include "panel-session.h"
#include "panel-session-item-private.h"

struct _PanelSession
{
  GObject    parent_instance;
  GPtrArray *items;
};

G_DEFINE_FINAL_TYPE (PanelSession, panel_session, G_TYPE_OBJECT)

static void
panel_session_dispose (GObject *object)
{
  PanelSession *self = (PanelSession *)object;

  g_clear_pointer (&self->items, g_ptr_array_unref);

  G_OBJECT_CLASS (panel_session_parent_class)->dispose (object);
}

static void
panel_session_class_init (PanelSessionClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->dispose = panel_session_dispose;
}

static void
panel_session_init (PanelSession *self)
{
  self->items = g_ptr_array_new_with_free_func (g_object_unref);
}

/**
 * panel_session_to_variant:
 * @self: a #PanelSession
 *
 * Serializes a #PanelSession as a #GVariant
 *
 * The result of this function may be passed to
 * panel_session_new_from_variant() to recreate a #PanelSession.
 *
 * The resulting variant will not be floating.
 *
 * Returns: (transfer full): a #GVariant
 */
GVariant *
panel_session_to_variant (PanelSession *self)
{
  GVariantBuilder builder;

  g_return_val_if_fail (PANEL_IS_SESSION (self), NULL);

  g_variant_builder_init (&builder, G_VARIANT_TYPE ("a{sv}"));
    g_variant_builder_add_parsed (&builder, "{'version',<%u>}", 1);
    g_variant_builder_open (&builder, G_VARIANT_TYPE ("{sv}"));
      g_variant_builder_add (&builder, "s", "items");
      g_variant_builder_open (&builder, G_VARIANT_TYPE ("v"));
        g_variant_builder_open (&builder, G_VARIANT_TYPE ("av"));
        for (guint i = 0; i < self->items->len; i++)
          {
            PanelSessionItem *item = g_ptr_array_index (self->items, i);

            _panel_session_item_to_variant (item, &builder);
          }
        g_variant_builder_close (&builder);
      g_variant_builder_close (&builder);
    g_variant_builder_close (&builder);
  return g_variant_take_ref (g_variant_builder_end (&builder));
}

static gboolean
panel_session_load_1 (PanelSession  *self,
                      GVariant      *variant,
                      GError       **error)
{
  GVariant *items = NULL;
  gboolean ret = FALSE;

  g_assert (PANEL_IS_SESSION (self));
  g_assert (variant != NULL);
  g_assert (g_variant_is_of_type (variant, G_VARIANT_TYPE_VARDICT));

  if ((items = g_variant_lookup_value (variant, "items", G_VARIANT_TYPE ("av"))))
    {
      gsize n_children = g_variant_n_children (items);

      for (gsize i = 0; i < n_children; i++)
        {
          GVariant *itemv = g_variant_get_child_value (items, i);
          GVariant *infov = g_variant_get_variant (itemv);
          PanelSessionItem *item = _panel_session_item_new_from_variant (infov, error);

          g_clear_pointer (&infov, g_variant_unref);
          g_clear_pointer (&itemv, g_variant_unref);

          if (item == NULL)
            goto cleanup;

          g_ptr_array_add (self->items, g_steal_pointer (&item));
        }

      ret = TRUE;

      goto cleanup;
    }

  g_set_error_literal (error,
                       G_IO_ERROR,
                       G_IO_ERROR_INVALID_DATA,
                       "items missing from variant");

cleanup:
  g_clear_pointer (&items, g_variant_unref);

  return ret;
}

static gboolean
panel_session_load (PanelSession  *self,
                    GVariant      *variant,
                    GError       **error)
{
  guint version = 0;

  g_assert (PANEL_IS_SESSION (self));
  g_assert (variant != NULL);
  g_assert (g_variant_is_of_type (variant, G_VARIANT_TYPE_VARDICT));

  if (g_variant_lookup (variant, "version", "u", &version))
    {
      if (version == 1)
        return panel_session_load_1 (self, variant, error);
    }

  g_set_error_literal (error,
                       G_IO_ERROR,
                       G_IO_ERROR_INVALID_DATA,
                       "Invalid version number in serialized session");

  return FALSE;
}

PanelSession *
panel_session_new (void)
{
  return g_object_new (PANEL_TYPE_SESSION, NULL);
}

/**
 * panel_session_new_from_variant:
 * @variant: a #GVariant from panel_session_to_variant()
 * @error: a location for a #GError, or %NULL
 *
 * Creates a new #PanelSession from a #GVariant.
 *
 * This creates a new #PanelSession instance from a previous session
 * which had been serialized to @variant.
 *
 * Returns: (transfer full): a #PanelSession
 *
 * Since: 1.4
 */
PanelSession *
panel_session_new_from_variant (GVariant  *variant,
                                GError   **error)
{
  PanelSession *self;

  g_return_val_if_fail (variant != NULL, NULL);
  g_return_val_if_fail (g_variant_is_of_type (variant, G_VARIANT_TYPE_VARDICT), NULL);

  self = g_object_new (PANEL_TYPE_SESSION, NULL);

  if (!panel_session_load (self, variant, error))
    g_clear_object (&self);

  return self;
}

guint
panel_session_get_n_items (PanelSession *self)
{
  g_return_val_if_fail (PANEL_IS_SESSION (self), 0);

  return self->items->len;
}

/**
 * panel_session_get_item:
 * @self: a #PanelSession
 * @position: the index of the item
 *
 * Gets the item at @position.
 *
 * Returns: (transfer none) (nullable): The #PanelSessionItem at @position
 *   or %NULL if there is no item at that position.
 *
 * Since: 1.4
 */
PanelSessionItem *
panel_session_get_item (PanelSession *self,
                        guint         position)
{
  g_return_val_if_fail (PANEL_IS_SESSION (self), NULL);

  if (position >= self->items->len)
    return NULL;

  return g_ptr_array_index (self->items, position);
}

void
panel_session_remove (PanelSession     *self,
                      PanelSessionItem *item)
{
  guint position;

  g_return_if_fail (PANEL_IS_SESSION (self));
  g_return_if_fail (PANEL_IS_SESSION_ITEM (item));

  if (g_ptr_array_find (self->items, item, &position))
    panel_session_remove_at (self, position);
}

void
panel_session_remove_at (PanelSession *self,
                         guint         position)
{
  g_return_if_fail (PANEL_IS_SESSION (self));
  g_return_if_fail (position < self->items->len);

  g_ptr_array_remove_index (self->items, position);
}

void
panel_session_append (PanelSession     *self,
                      PanelSessionItem *item)
{
  g_return_if_fail (PANEL_IS_SESSION (self));
  g_return_if_fail (PANEL_IS_SESSION_ITEM (item));

  g_ptr_array_add (self->items, g_object_ref (item));
}

void
panel_session_prepend (PanelSession     *self,
                       PanelSessionItem *item)
{
  g_return_if_fail (PANEL_IS_SESSION (self));
  g_return_if_fail (PANEL_IS_SESSION_ITEM (item));

  g_ptr_array_insert (self->items, 0, g_object_ref (item));
}

void
panel_session_insert (PanelSession     *self,
                      guint             position,
                      PanelSessionItem *item)
{
  g_return_if_fail (PANEL_IS_SESSION (self));
  g_return_if_fail (PANEL_IS_SESSION_ITEM (item));

  g_ptr_array_insert (self->items, position, g_object_ref (item));
}

/**
 * panel_session_lookup_by_id:
 * @self: a #PanelSession
 * @id: the id of the item
 *
 * Gets a session item matching @id.
 *
 * Returns: (transfer full) (nullable): an #PanelSessionItem or %NULL
 *
 * Since: 1.4
 */
PanelSessionItem *
panel_session_lookup_by_id (PanelSession *self,
                            const char   *id)
{
  g_return_val_if_fail (PANEL_IS_SESSION (self), NULL);

  for (guint i = 0; i < self->items->len; i++)
    {
      PanelSessionItem *item = g_ptr_array_index (self->items, i);

      if (g_strcmp0 (id, panel_session_item_get_id (item)) == 0)
        return g_object_ref (item);
    }

  return NULL;
}

