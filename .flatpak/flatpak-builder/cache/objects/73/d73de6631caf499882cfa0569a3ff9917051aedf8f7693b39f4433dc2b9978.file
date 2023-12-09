/* panel-widget-private.h
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

#include "panel-action-muxer-private.h"
#include "panel-widget.h"

G_BEGIN_DECLS

gboolean          _panel_widget_can_discard      (PanelWidget *self);
gboolean          _panel_widget_can_save         (PanelWidget *self);
void              _panel_widget_emit_presented   (PanelWidget *self);
PanelActionMuxer *_panel_widget_get_action_muxer (PanelWidget *self);

G_END_DECLS
