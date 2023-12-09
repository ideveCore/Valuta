/* panel-types.h
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

#include <glib-object.h>

#include "panel-version-macros.h"

G_BEGIN_DECLS

typedef struct _PanelDock           PanelDock;
typedef struct _PanelFrame          PanelFrame;
typedef struct _PanelFrameHeader    PanelFrameHeader;
typedef struct _PanelFrameHeaderBar PanelFrameHeaderBar;
typedef struct _PanelFrameSwitcher  PanelFrameSwitcher;
typedef struct _PanelFrameTabBar    PanelFrameTabBar;
typedef struct _PanelGrid           PanelGrid;
typedef struct _PanelGridColumn     PanelGridColumn;
typedef struct _PanelOmniBar        PanelOmniBar;
typedef struct _PanelPaned          PanelPaned;
typedef struct _PanelPosition       PanelPosition;
typedef struct _PanelSaveDelegate   PanelSaveDelegate;
typedef struct _PanelSaveDialog     PanelSaveDialog;
typedef struct _PanelStatusbar      PanelStatusbar;
typedef struct _PanelThemeSelector  PanelThemeSelector;
typedef struct _PanelToggleButton   PanelToggleButton;
typedef struct _PanelWidget         PanelWidget;

/**
 * PanelArea:
 * @PANEL_AREA_START: the area of the panel that is at the horizontal
 *    start. The side is defined by the direction of the user
 *    language. In English, it is the left side.
 * @PANEL_AREA_END: the area of the panel that is at the end.
 * @PANEL_AREA_TOP: the area at the top of the panel.
 * @PANEL_AREA_BOTTOM: the area at the bottom of the panel.
 * @PANEL_AREA_CENTER: the area that would be considered as the main area, always
 *    revealed.
 *
 * The area of the panel.
 */
typedef enum _PanelArea
{
  PANEL_AREA_START,
  PANEL_AREA_END,
  PANEL_AREA_TOP,
  PANEL_AREA_BOTTOM,
  PANEL_AREA_CENTER,
} PanelArea;

/**
 * PanelFrameCallback:
 * @frame: The #PanelFrame calling.
 * @user_data: the user data received by the callback.
 *
 * Callback passed to "foreach frame" functions.
 */
typedef void (*PanelFrameCallback) (PanelFrame *frame,
                                    gpointer    user_data);


G_END_DECLS
