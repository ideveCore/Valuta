/* panel-dock-child.h
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

#define PANEL_TYPE_DOCK_CHILD (panel_dock_child_get_type())

G_DECLARE_FINAL_TYPE (PanelDockChild, panel_dock_child, PANEL, DOCK_CHILD, GtkWidget)

GtkWidget *panel_dock_child_new               (PanelArea   area);
PanelArea  panel_dock_child_get_area          (PanelDockChild     *self);
GtkWidget *panel_dock_child_get_child         (PanelDockChild     *self);
void       panel_dock_child_set_child         (PanelDockChild     *self,
                                               GtkWidget          *child);
gboolean   panel_dock_child_get_reveal_child  (PanelDockChild     *self);
void       panel_dock_child_set_reveal_child  (PanelDockChild     *self,
                                               gboolean            reveal_child);
gboolean   panel_dock_child_get_empty         (PanelDockChild     *self);
gboolean   panel_dock_child_get_dragging      (PanelDockChild     *self);
void       panel_dock_child_set_dragging      (PanelDockChild     *self,
                                               gboolean            dragging);
void       panel_dock_child_foreach_frame     (PanelDockChild     *self,
                                               PanelFrameCallback  callback,
                                               gpointer            user_data);
int        panel_dock_child_get_drag_position (PanelDockChild     *self);
void       panel_dock_child_set_drag_position (PanelDockChild     *self,
                                               int                 drag_position);

G_END_DECLS
