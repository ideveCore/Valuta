/* panel-resizer.h
 *
 * Copyright 2021 Christian Hergert <chergert@redhat.com>
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

#define PANEL_TYPE_RESIZER (panel_resizer_get_type())

G_DECLARE_FINAL_TYPE (PanelResizer, panel_resizer, PANEL, RESIZER, GtkWidget)

GtkWidget *panel_resizer_new               (PanelArea     area);
PanelArea  panel_resizer_get_area          (PanelResizer *self);
void       panel_resizer_set_area          (PanelResizer *self,
                                            PanelArea     area);
GtkWidget *panel_resizer_get_child         (PanelResizer *self);
void       panel_resizer_set_child         (PanelResizer *self,
                                            GtkWidget    *child);
GtkWidget *panel_resizer_get_handle        (PanelResizer *self);
int        panel_resizer_get_drag_position (PanelResizer *self);
void       panel_resizer_set_drag_position (PanelResizer *self,
                                            int           drag_position);

G_END_DECLS
