/* panel-session-item.h
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

#pragma once

#if !defined (LIBPANEL_INSIDE) && !defined (LIBPANEL_COMPILATION)
# error "Only <libpanel.h> can be included directly."
#endif

#include <glib-object.h>

#include "panel-position.h"
#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_SESSION_ITEM (panel_session_item_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_FINAL_TYPE (PanelSessionItem, panel_session_item, PANEL, SESSION_ITEM, GObject)

PANEL_AVAILABLE_IN_1_4
PanelSessionItem *panel_session_item_new                    (void);
PANEL_AVAILABLE_IN_1_4
PanelPosition    *panel_session_item_get_position           (PanelSessionItem    *self);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_position           (PanelSessionItem    *self,
                                                             PanelPosition       *position);
PANEL_AVAILABLE_IN_1_4
const char       *panel_session_item_get_id                 (PanelSessionItem    *self);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_id                 (PanelSessionItem    *self,
                                                             const char          *id);
PANEL_AVAILABLE_IN_1_4
const char       *panel_session_item_get_workspace          (PanelSessionItem    *self);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_workspace          (PanelSessionItem    *self,
                                                             const char          *workspace);
PANEL_AVAILABLE_IN_1_4
const char       *panel_session_item_get_module_name        (PanelSessionItem    *self);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_module_name        (PanelSessionItem    *self,
                                                             const char          *module_name);
PANEL_AVAILABLE_IN_1_4
const char       *panel_session_item_get_type_hint          (PanelSessionItem    *self);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_type_hint          (PanelSessionItem    *self,
                                                             const char          *type_hint);
PANEL_AVAILABLE_IN_1_4
gboolean          panel_session_item_has_metadata           (PanelSessionItem    *self,
                                                             const char          *key,
                                                             const GVariantType **value_type);
PANEL_AVAILABLE_IN_1_4
gboolean          panel_session_item_has_metadata_with_type (PanelSessionItem    *self,
                                                             const char          *key,
                                                             const GVariantType  *expected_type);
PANEL_AVAILABLE_IN_1_4
gboolean          panel_session_item_get_metadata           (PanelSessionItem    *self,
                                                             const char          *key,
                                                             const char          *format,
                                                             ...);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_metadata           (PanelSessionItem    *self,
                                                             const char          *key,
                                                             const char          *format,
                                                             ...);
PANEL_AVAILABLE_IN_1_4
GVariant         *panel_session_item_get_metadata_value     (PanelSessionItem    *self,
                                                             const char          *key,
                                                             const GVariantType  *expected_type);
PANEL_AVAILABLE_IN_1_4
void              panel_session_item_set_metadata_value     (PanelSessionItem    *self,
                                                             const char          *key,
                                                             GVariant            *value);

G_END_DECLS
