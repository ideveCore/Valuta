/* panel-frame-tab-bar.h
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

#include <gtk/gtk.h>

#include "panel-types.h"

G_BEGIN_DECLS

#define PANEL_TYPE_FRAME_TAB_BAR (panel_frame_tab_bar_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_FINAL_TYPE (PanelFrameTabBar, panel_frame_tab_bar, PANEL, FRAME_TAB_BAR, GtkWidget)

PANEL_AVAILABLE_IN_ALL
GtkWidget *panel_frame_tab_bar_new             (void);
PANEL_AVAILABLE_IN_ALL
gboolean   panel_frame_tab_bar_get_autohide    (PanelFrameTabBar *self);
PANEL_AVAILABLE_IN_ALL
void       panel_frame_tab_bar_set_autohide    (PanelFrameTabBar *self,
                                                gboolean          autohide);
PANEL_AVAILABLE_IN_ALL
gboolean   panel_frame_tab_bar_get_inverted    (PanelFrameTabBar *self);
PANEL_AVAILABLE_IN_ALL
void       panel_frame_tab_bar_set_inverted    (PanelFrameTabBar *self,
                                                gboolean          inverted);
PANEL_AVAILABLE_IN_ALL
gboolean   panel_frame_tab_bar_get_expand_tabs (PanelFrameTabBar *self);
PANEL_AVAILABLE_IN_ALL
void       panel_frame_tab_bar_set_expand_tabs (PanelFrameTabBar *self,
                                                gboolean          expand_tabs);

G_END_DECLS
