/* panel-position.h
 *
 * Copyright 2022 Christian Hergert <chergert@redhat.com>
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

#include "panel-dock.h"
#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_POSITION (panel_position_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_FINAL_TYPE (PanelPosition, panel_position, PANEL, POSITION, GObject)

PANEL_AVAILABLE_IN_ALL
PanelPosition *panel_position_new              (void);
PANEL_AVAILABLE_IN_ALL
PanelPosition *panel_position_new_from_variant (GVariant      *variant);
PANEL_AVAILABLE_IN_ALL
GVariant      *panel_position_to_variant       (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
PanelArea      panel_position_get_area         (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
gboolean       panel_position_get_area_set     (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
guint          panel_position_get_column       (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
gboolean       panel_position_get_column_set   (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
guint          panel_position_get_depth        (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
gboolean       panel_position_get_depth_set    (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
guint          panel_position_get_row          (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
gboolean       panel_position_get_row_set      (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
gboolean       panel_position_is_indeterminate (PanelPosition *self);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_area         (PanelPosition *self,
                                                PanelArea      area);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_area_set     (PanelPosition *self,
                                                gboolean       area_set);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_column       (PanelPosition *self,
                                                guint          column);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_column_set   (PanelPosition *self,
                                                gboolean       column_set);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_depth        (PanelPosition *self,
                                                guint          depth);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_depth_set    (PanelPosition *self,
                                                gboolean       depth_set);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_row          (PanelPosition *self,
                                                guint          row);
PANEL_AVAILABLE_IN_ALL
void           panel_position_set_row_set      (PanelPosition *self,
                                                gboolean       row_set);
PANEL_AVAILABLE_IN_ALL
gboolean       panel_position_equal            (PanelPosition *a,
                                                PanelPosition *b);

G_END_DECLS
