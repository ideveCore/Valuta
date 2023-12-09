/* panel-theme-selector-private.h
 *
 * Copyright 2021-2022 Christian Hergert <chergert@redhat.com>
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

#include <gtk/gtk.h>

#include "panel-types.h"

G_BEGIN_DECLS

#define PANEL_TYPE_THEME_SELECTOR (panel_theme_selector_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_FINAL_TYPE (PanelThemeSelector, panel_theme_selector, PANEL, THEME_SELECTOR, GtkWidget)

PANEL_AVAILABLE_IN_ALL
GtkWidget  *panel_theme_selector_new             (void);
PANEL_AVAILABLE_IN_ALL
const char *panel_theme_selector_get_action_name (PanelThemeSelector *self);
PANEL_AVAILABLE_IN_ALL
void        panel_theme_selector_set_action_name (PanelThemeSelector *self,
                                                  const char         *action_name);

G_END_DECLS
