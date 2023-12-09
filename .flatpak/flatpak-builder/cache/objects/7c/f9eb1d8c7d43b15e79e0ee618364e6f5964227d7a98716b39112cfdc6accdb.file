/* panel-frame-private.h
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

#include <adwaita.h>

#include "panel-frame.h"

G_BEGIN_DECLS

void        _panel_frame_set_closeable   (PanelFrame  *self,
                                          gboolean     closeable);
GMenuModel *_panel_frame_get_tab_menu    (PanelFrame  *self);
AdwTabView *_panel_frame_get_tab_view    (PanelFrame  *self);
void        _panel_frame_transfer        (PanelFrame  *self,
                                          PanelWidget *widget,
                                          PanelFrame  *new_frame,
                                          int          position);
gboolean    _panel_frame_in_drop         (PanelFrame  *self);
void        _panel_frame_set_drop_before (PanelFrame  *self,
                                          PanelWidget *widget);
void        _panel_frame_request_close   (PanelFrame  *self,
                                          PanelWidget *widget);

G_END_DECLS
