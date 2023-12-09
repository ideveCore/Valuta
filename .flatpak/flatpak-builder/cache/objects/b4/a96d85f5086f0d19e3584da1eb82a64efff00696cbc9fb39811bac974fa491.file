/* panel-layered-settings.h
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

#include <gio/gio.h>

#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_LAYERED_SETTINGS (panel_layered_settings_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_FINAL_TYPE (PanelLayeredSettings, panel_layered_settings, PANEL, LAYERED_SETTINGS, GObject)

PANEL_AVAILABLE_IN_1_4
PanelLayeredSettings  *panel_layered_settings_new               (const char              *schema_id,
                                                                 const char              *path);
PANEL_AVAILABLE_IN_1_4
GSettingsSchemaKey    *panel_layered_settings_get_key           (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
char                 **panel_layered_settings_list_keys         (PanelLayeredSettings    *self);
PANEL_AVAILABLE_IN_1_4
GVariant              *panel_layered_settings_get_default_value (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
GVariant              *panel_layered_settings_get_user_value    (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
GVariant              *panel_layered_settings_get_value         (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_set_value         (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 GVariant                *value);
PANEL_AVAILABLE_IN_1_4
gboolean               panel_layered_settings_get_boolean       (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
double                 panel_layered_settings_get_double        (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
int                    panel_layered_settings_get_int           (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
char                  *panel_layered_settings_get_string        (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
guint                  panel_layered_settings_get_uint          (PanelLayeredSettings    *self,
                                                                 const char              *key);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_set_boolean       (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 gboolean                 val);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_set_double        (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 double                   val);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_set_int           (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 int                      val);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_set_string        (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 const char              *val);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_set_uint          (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 guint                    val);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_append            (PanelLayeredSettings    *self,
                                                                 GSettings               *settings);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_bind              (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 gpointer                 object,
                                                                 const char              *property,
                                                                 GSettingsBindFlags       flags);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_bind_with_mapping (PanelLayeredSettings    *self,
                                                                 const char              *key,
                                                                 gpointer                 object,
                                                                 const char              *property,
                                                                 GSettingsBindFlags       flags,
                                                                 GSettingsBindGetMapping  get_mapping,
                                                                 GSettingsBindSetMapping  set_mapping,
                                                                 gpointer                 user_data,
                                                                 GDestroyNotify           destroy);
PANEL_AVAILABLE_IN_1_4
void                   panel_layered_settings_unbind            (PanelLayeredSettings    *self,
                                                                 const char              *property);

G_END_DECLS
