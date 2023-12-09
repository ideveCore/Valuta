/* panel-dock-private.h
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

#include "panel-dock.h"

G_BEGIN_DECLS

typedef struct _PanelDockChild PanelDockChild;
typedef struct _PanelFrame     PanelFrame;

GtkWidget *_panel_dock_get_top_child      (PanelDock      *self);
GtkWidget *_panel_dock_get_bottom_child   (PanelDock      *self);
GtkWidget *_panel_dock_get_start_child    (PanelDock      *self);
GtkWidget *_panel_dock_get_end_child      (PanelDock      *self);
void       _panel_dock_begin_drag         (PanelDock      *self,
                                           PanelWidget    *widget);
void       _panel_dock_end_drag           (PanelDock      *self,
                                           PanelWidget    *widget);
void       _panel_dock_set_maximized      (PanelDock      *self,
                                           PanelWidget    *widget);
void       _panel_dock_add_widget         (PanelDock      *self,
                                           PanelDockChild *dock_child,
                                           PanelFrame     *frame,
                                           PanelWidget    *widget);
void       _panel_dock_remove_frame       (PanelDock      *self,
                                           PanelFrame     *frame);
void       _panel_dock_update_orientation (GtkWidget      *widget,
                                           GtkOrientation  orientation);
PanelFrame *
           _panel_dock_create_frame       (PanelDock      *self,
                                           PanelPosition  *position);
gboolean   _panel_dock_can_adopt          (PanelDock      *self,
                                           PanelWidget    *widget);

G_END_DECLS
