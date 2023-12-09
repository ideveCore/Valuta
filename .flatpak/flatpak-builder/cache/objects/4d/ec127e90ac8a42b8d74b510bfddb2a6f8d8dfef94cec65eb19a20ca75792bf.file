/* panel-menu-manager.h
 *
 * Copyright 2015-2023 Christian Hergert <chergert@redhat.com>
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

#pragma once

#if !defined (LIBPANEL_INSIDE) && !defined (LIBPANEL_COMPILATION)
# error "Only <libpanel.h> can be included directly."
#endif

#include <gio/gio.h>

#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_MENU_MANAGER (panel_menu_manager_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_FINAL_TYPE (PanelMenuManager, panel_menu_manager, PANEL, MENU_MANAGER, GObject)

PANEL_AVAILABLE_IN_1_4
PanelMenuManager     *panel_menu_manager_new                  (void);
PANEL_AVAILABLE_IN_1_4
guint                 panel_menu_manager_add_filename         (PanelMenuManager  *self,
                                                               const char        *filename,
                                                               GError           **error);
PANEL_AVAILABLE_IN_1_4
guint                 panel_menu_manager_add_resource         (PanelMenuManager  *self,
                                                               const char        *resource,
                                                               GError           **error);
PANEL_AVAILABLE_IN_1_4
guint                 panel_menu_manager_merge                (PanelMenuManager  *self,
                                                               const char        *menu_id,
                                                               GMenuModel        *menu_model);
PANEL_AVAILABLE_IN_1_4
void                  panel_menu_manager_remove               (PanelMenuManager  *self,
                                                               guint              merge_id);
PANEL_AVAILABLE_IN_1_4
GMenu                *panel_menu_manager_get_menu_by_id       (PanelMenuManager  *self,
                                                               const char        *menu_id);
PANEL_AVAILABLE_IN_1_4
const char * const   *panel_menu_manager_get_menu_ids         (PanelMenuManager  *self);
PANEL_AVAILABLE_IN_1_4
void                  panel_menu_manager_set_attribute_string (PanelMenuManager  *self,
                                                               GMenu             *menu,
                                                               guint              position,
                                                               const char        *attribute,
                                                               const char        *value);
PANEL_AVAILABLE_IN_1_4
GMenu                *panel_menu_manager_find_item_by_id      (PanelMenuManager  *self,
                                                               const char        *id,
                                                               guint             *position);

G_END_DECLS
