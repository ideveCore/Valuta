/* panel-grid-private.h
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

#include "panel-grid.h"

G_BEGIN_DECLS

PanelFrame *_panel_grid_create_frame     (PanelGrid          *self);
gboolean    _panel_grid_get_position     (PanelGrid          *self,
                                          GtkWidget          *widget,
                                          guint              *column,
                                          guint              *row);
void        _panel_grid_reposition       (PanelGrid          *self,
                                          GtkWidget          *widget,
                                          guint               column,
                                          guint               row,
                                          gboolean            force_row);
void        _panel_grid_prepend_column   (PanelGrid          *self);
void        _panel_grid_remove_column    (PanelGrid          *self,
                                          PanelGridColumn    *column);
void        _panel_grid_insert_column    (PanelGrid          *self,
                                          guint               position);
void        _panel_grid_foreach_frame    (PanelGrid          *self,
                                          PanelFrameCallback  callback,
                                          gpointer            user_data);
void        _panel_grid_collapse         (PanelGrid          *self,
                                          PanelGridColumn    *column);
void        _panel_grid_update_closeable (PanelGrid          *self);
void        _panel_grid_drop_frame_mru   (PanelGrid          *self,
                                          PanelFrame         *frame);
void        _panel_grid_update_focus     (PanelGrid          *self);

G_END_DECLS
