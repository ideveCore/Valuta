/* panel-document-workspace.h
 *
 * Copyright 2023 Christian Hergert <chergert@redhat.com>
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
#include "panel-frame.h"
#include "panel-grid.h"
#include "panel-position.h"
#include "panel-statusbar.h"
#include "panel-workbench.h"
#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_DOCUMENT_WORKSPACE (panel_document_workspace_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_DERIVABLE_TYPE (PanelDocumentWorkspace, panel_document_workspace, PANEL, DOCUMENT_WORKSPACE, PanelWorkspace)

struct _PanelDocumentWorkspaceClass
{
  PanelWorkspaceClass parent_class;

  PanelFrame *(*create_frame) (PanelDocumentWorkspace *self,
                               PanelPosition          *position);
  gboolean    (*add_widget)   (PanelDocumentWorkspace *self,
                               PanelWidget            *widget,
                               PanelPosition          *position);

  /*< private >*/
  gpointer _reserved[16];
};

PANEL_AVAILABLE_IN_1_4
GtkWidget      *panel_document_workspace_new           (void);
PANEL_AVAILABLE_IN_1_4
PanelDock      *panel_document_workspace_get_dock      (PanelDocumentWorkspace *self);
PANEL_AVAILABLE_IN_1_4
PanelGrid      *panel_document_workspace_get_grid      (PanelDocumentWorkspace *self);
PANEL_AVAILABLE_IN_1_4
PanelStatusbar *panel_document_workspace_get_statusbar (PanelDocumentWorkspace *self);
PANEL_AVAILABLE_IN_1_4
GtkWidget      *panel_document_workspace_get_titlebar  (PanelDocumentWorkspace *self);
PANEL_AVAILABLE_IN_1_4
void            panel_document_workspace_set_titlebar  (PanelDocumentWorkspace *self,
                                                        GtkWidget              *titlebar);
PANEL_AVAILABLE_IN_1_4
gboolean        panel_document_workspace_add_widget    (PanelDocumentWorkspace *self,
                                                        PanelWidget            *widget,
                                                        PanelPosition          *position);

G_END_DECLS
