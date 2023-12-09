/* panel-joined-menu.c
 *
 * Copyright 2017-2021 Christian Hergert <chergert@redhat.com>
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

#include "panel-joined-menu-private.h"

typedef struct
{
  GMenuModel *model;
  gulong      items_changed_handler;
} Menu;

struct _PanelJoinedMenu
{
  GMenuModel  parent_instance;
  GArray     *menus;
};

G_DEFINE_TYPE (PanelJoinedMenu, panel_joined_menu, G_TYPE_MENU_MODEL)

static void
clear_menu (gpointer data)
{
  Menu *menu = data;

  g_signal_handler_disconnect (menu->model, menu->items_changed_handler);
  menu->items_changed_handler = 0;
  g_clear_object (&menu->model);
}

static gint
panel_joined_menu_get_offset_at_index (PanelJoinedMenu *self,
                                       gint             index)
{
  gint offset = 0;

  for (guint i = 0; i < index; i++)
    offset += g_menu_model_get_n_items (g_array_index (self->menus, Menu, i).model);

  return offset;
}

static gint
panel_joined_menu_get_offset_at_model (PanelJoinedMenu *self,
                                       GMenuModel      *model)
{
  gint offset = 0;

  for (guint i = 0; i < self->menus->len; i++)
    {
      const Menu *menu = &g_array_index (self->menus, Menu, i);

      if (menu->model == model)
        break;

      offset += g_menu_model_get_n_items (menu->model);
    }

  return offset;
}

static gboolean
panel_joined_menu_is_mutable (GMenuModel *model)
{
  return TRUE;
}

static gint
panel_joined_menu_get_n_items (GMenuModel *model)
{
  PanelJoinedMenu *self = (PanelJoinedMenu *)model;

  if (self->menus->len == 0)
    return 0;

  return panel_joined_menu_get_offset_at_index (self, self->menus->len);
}

static const Menu *
panel_joined_menu_get_item (PanelJoinedMenu *self,
                            gint            *item_index)
{
  g_assert (PANEL_IS_JOINED_MENU (self));

  for (guint i = 0; i < self->menus->len; i++)
    {
      const Menu *menu = &g_array_index (self->menus, Menu, i);
      gint n_items = g_menu_model_get_n_items (menu->model);

      if (n_items > *item_index)
        return menu;

      (*item_index) -= n_items;
    }

  g_assert_not_reached ();

  return NULL;
}

static void
panel_joined_menu_get_item_attributes (GMenuModel  *model,
                                       gint         item_index,
                                       GHashTable **attributes)
{
  const Menu *menu = panel_joined_menu_get_item (PANEL_JOINED_MENU (model), &item_index);
  G_MENU_MODEL_GET_CLASS (menu->model)->get_item_attributes (menu->model, item_index, attributes);
}

static GMenuAttributeIter *
panel_joined_menu_iterate_item_attributes (GMenuModel *model,
                                           gint        item_index)
{
  const Menu *menu = panel_joined_menu_get_item (PANEL_JOINED_MENU (model), &item_index);
  return G_MENU_MODEL_GET_CLASS (menu->model)->iterate_item_attributes (menu->model, item_index);
}

static GVariant *
panel_joined_menu_get_item_attribute_value (GMenuModel         *model,
                                            gint                item_index,
                                            const gchar        *attribute,
                                            const GVariantType *expected_type)
{
  const Menu *menu = panel_joined_menu_get_item (PANEL_JOINED_MENU (model), &item_index);
  return G_MENU_MODEL_GET_CLASS (menu->model)->get_item_attribute_value (menu->model, item_index, attribute, expected_type);
}

static void
panel_joined_menu_get_item_links (GMenuModel  *model,
                                  gint         item_index,
                                  GHashTable **links)
{
  const Menu *menu = panel_joined_menu_get_item (PANEL_JOINED_MENU (model), &item_index);
  G_MENU_MODEL_GET_CLASS (menu->model)->get_item_links (menu->model, item_index, links);
}

static GMenuLinkIter *
panel_joined_menu_iterate_item_links (GMenuModel *model,
                                      gint        item_index)
{
  const Menu *menu = panel_joined_menu_get_item (PANEL_JOINED_MENU (model), &item_index);
  return G_MENU_MODEL_GET_CLASS (menu->model)->iterate_item_links (menu->model, item_index);
}

static GMenuModel *
panel_joined_menu_get_item_link (GMenuModel  *model,
                                 gint         item_index,
                                 const gchar *link)
{
  const Menu *menu = panel_joined_menu_get_item (PANEL_JOINED_MENU (model), &item_index);
  return G_MENU_MODEL_GET_CLASS (menu->model)->get_item_link (menu->model, item_index, link);
}

static void
panel_joined_menu_finalize (GObject *object)
{
  PanelJoinedMenu *self = (PanelJoinedMenu *)object;

  g_clear_pointer (&self->menus, g_array_unref);

  G_OBJECT_CLASS (panel_joined_menu_parent_class)->finalize (object);
}

static void
panel_joined_menu_class_init (PanelJoinedMenuClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GMenuModelClass *menu_model_class = G_MENU_MODEL_CLASS (klass);

  object_class->finalize = panel_joined_menu_finalize;

  menu_model_class->is_mutable = panel_joined_menu_is_mutable;
  menu_model_class->get_n_items = panel_joined_menu_get_n_items;
  menu_model_class->get_item_attributes = panel_joined_menu_get_item_attributes;
  menu_model_class->iterate_item_attributes = panel_joined_menu_iterate_item_attributes;
  menu_model_class->get_item_attribute_value = panel_joined_menu_get_item_attribute_value;
  menu_model_class->get_item_links = panel_joined_menu_get_item_links;
  menu_model_class->iterate_item_links = panel_joined_menu_iterate_item_links;
  menu_model_class->get_item_link = panel_joined_menu_get_item_link;
}

static void
panel_joined_menu_init (PanelJoinedMenu *self)
{
  self->menus = g_array_new (FALSE, FALSE, sizeof (Menu));
  g_array_set_clear_func (self->menus, clear_menu);
}

static void
panel_joined_menu_on_items_changed (PanelJoinedMenu *self,
                                    guint            offset,
                                    guint            removed,
                                    guint            added,
                                    GMenuModel      *model)
{
  g_assert (PANEL_IS_JOINED_MENU (self));
  g_assert (G_IS_MENU_MODEL (model));

  offset += panel_joined_menu_get_offset_at_model (self, model);
  g_menu_model_items_changed (G_MENU_MODEL (self), offset, removed, added);
}

PanelJoinedMenu *
panel_joined_menu_new (void)
{
  return g_object_new (PANEL_TYPE_JOINED_MENU, NULL);
}

static void
panel_joined_menu_insert (PanelJoinedMenu *self,
                          GMenuModel      *model,
                          gint             index)
{
  Menu menu = { 0 };
  gint offset;
  gint n_items;

  g_assert (PANEL_IS_JOINED_MENU (self));
  g_assert (G_IS_MENU_MODEL (model));
  g_assert (index >= 0);
  g_assert (index <= self->menus->len);

  menu.model = g_object_ref (model);
  menu.items_changed_handler =
    g_signal_connect_swapped (menu.model,
                              "items-changed",
                              G_CALLBACK (panel_joined_menu_on_items_changed),
                              self);
  g_array_insert_val (self->menus, index, menu);

  n_items = g_menu_model_get_n_items (model);
  offset = panel_joined_menu_get_offset_at_index (self, index);
  g_menu_model_items_changed (G_MENU_MODEL (self), offset, 0, n_items);
}

void
panel_joined_menu_append_menu (PanelJoinedMenu *self,
                               GMenuModel      *model)
{

  g_return_if_fail (PANEL_IS_JOINED_MENU (self));
  g_return_if_fail (G_MENU_MODEL (model));

  panel_joined_menu_insert (self, model, self->menus->len);
}

void
panel_joined_menu_prepend_menu (PanelJoinedMenu *self,
                                GMenuModel      *model)
{
  g_return_if_fail (PANEL_IS_JOINED_MENU (self));
  g_return_if_fail (G_MENU_MODEL (model));

  panel_joined_menu_insert (self, model, 0);
}

void
panel_joined_menu_remove_index (PanelJoinedMenu *self,
                                guint            index)
{
  const Menu *menu;
  gint n_items;
  gint offset;

  g_return_if_fail (PANEL_IS_JOINED_MENU (self));
  g_return_if_fail (index < self->menus->len);

  menu = &g_array_index (self->menus, Menu, index);

  offset = panel_joined_menu_get_offset_at_index (self, index);
  n_items = g_menu_model_get_n_items (menu->model);

  g_array_remove_index (self->menus, index);

  g_menu_model_items_changed (G_MENU_MODEL (self), offset, n_items, 0);
}

void
panel_joined_menu_remove_menu (PanelJoinedMenu *self,
                               GMenuModel      *model)
{
  g_return_if_fail (PANEL_IS_JOINED_MENU (self));
  g_return_if_fail (G_IS_MENU_MODEL (model));

  for (guint i = 0; i < self->menus->len; i++)
    {
      if (g_array_index (self->menus, Menu, i).model == model)
        {
          panel_joined_menu_remove_index (self, i);
          break;
        }
    }
}

/**
 * panel_joined_menu_get_n_joined:
 * @self: a #PanelJoinedMenu
 *
 * Gets the number of joined menus.
 */
guint
panel_joined_menu_get_n_joined (PanelJoinedMenu *self)
{
  g_return_val_if_fail (PANEL_IS_JOINED_MENU (self), 0);

  return self->menus->len;
}
