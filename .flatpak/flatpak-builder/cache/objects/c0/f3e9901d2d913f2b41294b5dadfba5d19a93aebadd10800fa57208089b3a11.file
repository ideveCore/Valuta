/* panel-save-dialog-row-private.h
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

#include <adwaita.h>

#include "panel-types.h"

G_BEGIN_DECLS

#define PANEL_TYPE_SAVE_DIALOG_ROW (panel_save_dialog_row_get_type())

G_DECLARE_FINAL_TYPE (PanelSaveDialogRow, panel_save_dialog_row, PANEL, SAVE_DIALOG_ROW, AdwActionRow)

GtkWidget         *panel_save_dialog_row_new                (PanelSaveDelegate  *delegate);
PanelSaveDelegate *panel_save_dialog_row_get_delegate       (PanelSaveDialogRow *self);
gboolean           panel_save_dialog_row_get_selected       (PanelSaveDialogRow *self);
void               panel_save_dialog_row_set_selected       (PanelSaveDialogRow *self,
                                                             gboolean            selected);
void               panel_save_dialog_row_set_selection_mode (PanelSaveDialogRow *self,
                                                             gboolean            selection_mode);

G_END_DECLS
