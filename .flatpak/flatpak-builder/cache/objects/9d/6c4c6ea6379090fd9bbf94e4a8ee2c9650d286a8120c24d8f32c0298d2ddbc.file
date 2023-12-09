/* panel-frame-header-bar-row-private.h
 *
 * Copyright 2021 Christian Hergert <chergert@redhat.com>
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

#include <adwaita.h>

G_BEGIN_DECLS

#define PANEL_TYPE_FRAME_HEADER_BAR_ROW (panel_frame_header_bar_row_get_type())

G_DECLARE_FINAL_TYPE (PanelFrameHeaderBarRow, panel_frame_header_bar_row, PANEL, FRAME_HEADER_BAR_ROW, GtkWidget)

GtkWidget  *panel_frame_header_bar_row_new      (void);
AdwTabPage *panel_frame_header_bar_row_get_page (PanelFrameHeaderBarRow *self);
void        panel_frame_header_bar_row_set_page (PanelFrameHeaderBarRow *self,
                                                 AdwTabPage             *page);

G_END_DECLS
