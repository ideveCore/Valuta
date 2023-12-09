/* panel-progress-icon-private.h
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

#include <gtk/gtk.h>

G_BEGIN_DECLS

#define PANEL_TYPE_PROGRESS_ICON (panel_progress_icon_get_type())

G_DECLARE_FINAL_TYPE (PanelProgressIcon, panel_progress_icon, PANEL, PROGRESS_ICON, GtkDrawingArea)

GtkWidget *panel_progress_icon_new          (void);
gdouble    panel_progress_icon_get_progress (PanelProgressIcon *self);
void       panel_progress_icon_set_progress (PanelProgressIcon *self,
                                             double             progress);

G_END_DECLS
