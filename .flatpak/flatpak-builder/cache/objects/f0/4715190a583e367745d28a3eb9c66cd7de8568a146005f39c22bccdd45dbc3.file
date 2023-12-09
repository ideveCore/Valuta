/* panel-drop-controls-private.h
 *
 * Copyright 2022 Christian Hergert <chergert@redhat.com>
 *
 * This file is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * This file is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include <gtk/gtk.h>

#include "panel-types.h"

G_BEGIN_DECLS

#define PANEL_TYPE_DROP_CONTROLS (panel_drop_controls_get_type())

G_DECLARE_FINAL_TYPE (PanelDropControls, panel_drop_controls, PANEL, DROP_CONTROLS, GtkWidget)

GtkWidget *panel_drop_controls_new      (void);
PanelArea  panel_drop_controls_get_area (PanelDropControls *self);
void       panel_drop_controls_set_area (PanelDropControls *self,
                                         PanelArea          area);
gboolean   panel_drop_controls_in_drop  (PanelDropControls *self);

G_END_DECLS
