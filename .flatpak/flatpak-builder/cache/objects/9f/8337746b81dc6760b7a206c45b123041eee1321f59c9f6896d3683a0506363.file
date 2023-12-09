/* panel-session.h
 *
 * Copyright 2022-2023 Christian Hergert <chergert@redhat.com>
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

#if !defined (LIBPANEL_INSIDE) && !defined (LIBPANEL_COMPILATION)
# error "Only <libpanel.h> can be included directly."
#endif

#include "panel-session-item.h"
#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_SESSION (panel_session_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_FINAL_TYPE (PanelSession, panel_session, PANEL, SESSION, GObject)

PANEL_AVAILABLE_IN_1_4
PanelSession     *panel_session_new              (void);
PANEL_AVAILABLE_IN_1_4
void              panel_session_append           (PanelSession      *self,
                                                  PanelSessionItem  *item);
PANEL_AVAILABLE_IN_1_4
void              panel_session_prepend          (PanelSession      *self,
                                                  PanelSessionItem  *item);
PANEL_AVAILABLE_IN_1_4
void              panel_session_insert           (PanelSession      *self,
                                                  guint              position,
                                                  PanelSessionItem  *item);
PANEL_AVAILABLE_IN_1_4
void              panel_session_remove           (PanelSession      *self,
                                                  PanelSessionItem  *item);
PANEL_AVAILABLE_IN_1_4
void              panel_session_remove_at        (PanelSession      *self,
                                                  guint              position);
PANEL_AVAILABLE_IN_1_4
guint             panel_session_get_n_items      (PanelSession      *self);
PANEL_AVAILABLE_IN_1_4
PanelSessionItem *panel_session_get_item         (PanelSession      *self,
                                                  guint              position);
PANEL_AVAILABLE_IN_1_4
PanelSession     *panel_session_new_from_variant (GVariant          *variant,
                                                  GError           **error);
PANEL_AVAILABLE_IN_1_4
GVariant         *panel_session_to_variant       (PanelSession      *self);
PANEL_AVAILABLE_IN_1_4
PanelSessionItem *panel_session_lookup_by_id     (PanelSession      *self,
                                                  const char        *id);

G_END_DECLS

