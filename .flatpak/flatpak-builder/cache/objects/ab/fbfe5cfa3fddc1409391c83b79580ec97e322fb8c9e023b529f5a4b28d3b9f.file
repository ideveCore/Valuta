/* panel-action-muxer-private.h
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

#include "panel-action-muxer.h"

G_BEGIN_DECLS

struct _PanelAction
{
  const struct _PanelAction *next;
  const char                *name;
  GType                      owner;
  const GVariantType        *parameter_type;
  const GVariantType        *state_type;
  GParamSpec                *pspec;
  PanelActionActivateFunc    activate;
  guint                      position;
};

void panel_action_muxer_set_enabled     (PanelActionMuxer  *self,
                                         const PanelAction *action,
                                         gboolean           enabled);
void panel_action_muxer_connect_actions (PanelActionMuxer  *self,
                                         gpointer           instance,
                                         const PanelAction *actions);

G_END_DECLS
