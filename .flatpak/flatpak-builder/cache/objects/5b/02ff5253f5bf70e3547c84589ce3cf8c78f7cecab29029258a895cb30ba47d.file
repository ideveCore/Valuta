/* panel-settings.h
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

#define PANEL_TYPE_SETTINGS (panel_settings_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_FINAL_TYPE (PanelSettings, panel_settings, PANEL, SETTINGS, GObject)

PANEL_AVAILABLE_IN_1_4
char          *panel_settings_resolve_schema_path         (const char              *schema_id_prefix,
                                                           const char              *schema_id,
                                                           const char              *identifier,
                                                           const char              *path_prefix,
                                                           const char              *path_suffix);
PANEL_AVAILABLE_IN_1_4
PanelSettings *panel_settings_new                         (const char              *identifier,
                                                           const char              *schema_id);
PANEL_AVAILABLE_IN_1_4
PanelSettings *panel_settings_new_with_path               (const char              *identifier,
                                                           const char              *schema_id,
                                                           const char              *path);
PANEL_AVAILABLE_IN_1_4
PanelSettings *panel_settings_new_relocatable             (const char              *identifier,
                                                           const char              *schema_id,
                                                           const char              *schema_id_prefix,
                                                           const char              *path_prefix,
                                                           const char              *path_suffix);
PANEL_AVAILABLE_IN_1_4
const char    *panel_settings_get_schema_id               (PanelSettings           *self);
PANEL_AVAILABLE_IN_1_4
GVariant      *panel_settings_get_default_value           (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
GVariant      *panel_settings_get_user_value              (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
GVariant      *panel_settings_get_value                   (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_set_value                   (PanelSettings           *self,
                                                           const char              *key,
                                                           GVariant                *value);
PANEL_AVAILABLE_IN_1_4
gboolean       panel_settings_get_boolean                 (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
double         panel_settings_get_double                  (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
int            panel_settings_get_int                     (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
char          *panel_settings_get_string                  (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
guint          panel_settings_get_uint                    (PanelSettings           *self,
                                                           const char              *key);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_set_boolean                 (PanelSettings           *self,
                                                           const char              *key,
                                                           gboolean                 val);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_set_double                  (PanelSettings           *self,
                                                           const char              *key,
                                                           double                   val);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_set_int                     (PanelSettings           *self,
                                                           const char              *key,
                                                           int                      val);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_set_string                  (PanelSettings           *self,
                                                           const char              *key,
                                                           const char              *val);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_set_uint                    (PanelSettings           *self,
                                                           const char              *key,
                                                           guint                    val);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_bind                        (PanelSettings           *self,
                                                           const char              *key,
                                                           gpointer                 object,
                                                           const char              *property,
                                                           GSettingsBindFlags       flags);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_bind_with_mapping           (PanelSettings           *self,
                                                           const char              *key,
                                                           gpointer                 object,
                                                           const char              *property,
                                                           GSettingsBindFlags       flags,
                                                           GSettingsBindGetMapping  get_mapping,
                                                           GSettingsBindSetMapping  set_mapping,
                                                           gpointer                 user_data,
                                                           GDestroyNotify           destroy);
PANEL_AVAILABLE_IN_1_4
void           panel_settings_unbind                      (PanelSettings           *self,
                                                           const char              *property);

G_END_DECLS
