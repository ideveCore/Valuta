/* panel-workbench.h
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

#if !defined (LIBPANEL_INSIDE) && !defined (LIBPANEL_COMPILATION)
# error "Only <libpanel.h> can be included directly."
#endif

#include <adwaita.h>

#include "panel-action-muxer.h"
#include "panel-inhibitor.h"
#include "panel-version-macros.h"

G_BEGIN_DECLS

#define PANEL_TYPE_WORKBENCH (panel_workbench_get_type())
#define PANEL_TYPE_WORKSPACE (panel_workspace_get_type())

PANEL_AVAILABLE_IN_1_4
G_DECLARE_DERIVABLE_TYPE (PanelWorkbench, panel_workbench, PANEL, WORKBENCH, GtkWindowGroup)

PANEL_AVAILABLE_IN_1_4
G_DECLARE_DERIVABLE_TYPE (PanelWorkspace, panel_workspace, PANEL, WORKSPACE, AdwApplicationWindow)

/**
 * PanelWorkspaceForeach:
 * @workspace: a #PanelWorkspace
 * @user_data: closure data provided with foreach func
 *
 * This function is called for each workspace window within a #PanelWorkbench
 * when using panel_workbench_foreach_workspace().
 *
 * Since: 1.4
 */
typedef void (*PanelWorkspaceForeach) (PanelWorkspace *workspace,
                                       gpointer        user_data);

struct _PanelWorkbenchClass
{
  GtkWindowGroupClass parent_class;

  void     (*activate)      (PanelWorkbench       *self);
  void     (*unload_async)  (PanelWorkbench       *self,
                             GCancellable         *cancellable,
                             GAsyncReadyCallback   callback,
                             gpointer              user_data);
  gboolean (*unload_finish) (PanelWorkbench       *self,
                             GAsyncResult         *result,
                             GError              **error);

  /*< private >*/
  gpointer _reserved[8];
};

PANEL_AVAILABLE_IN_1_4
PanelWorkbench *panel_workbench_new                           (void);
PANEL_AVAILABLE_IN_1_4
PanelWorkbench *panel_workbench_find_from_widget              (GtkWidget                  *widget);
PANEL_AVAILABLE_IN_1_4
const char     *panel_workbench_get_id                        (PanelWorkbench             *self);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_set_id                        (PanelWorkbench             *self,
                                                               const char                 *id);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_activate                      (PanelWorkbench             *self);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_add_workspace                 (PanelWorkbench             *self,
                                                               PanelWorkspace             *workspace);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_remove_workspace              (PanelWorkbench             *self,
                                                               PanelWorkspace             *workspace);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_focus_workspace               (PanelWorkbench             *self,
                                                               PanelWorkspace             *workspace);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_foreach_workspace             (PanelWorkbench             *self,
                                                               PanelWorkspaceForeach       foreach_func,
                                                               gpointer                    foreach_func_data);
PANEL_AVAILABLE_IN_1_4
PanelWorkspace *panel_workbench_find_workspace_typed          (PanelWorkbench             *self,
                                                               GType                       workspace_type);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_action_set_enabled            (PanelWorkbench             *self,
                                                               const char                 *action_name,
                                                               gboolean                    enabled);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_class_install_action          (PanelWorkbenchClass        *workbench_class,
                                                               const char                 *action_name,
                                                               const char                 *parameter_type,
                                                               PanelActionActivateFunc     activate);
PANEL_AVAILABLE_IN_1_4
void            panel_workbench_class_install_property_action (PanelWorkbenchClass        *workbench_class,
                                                               const char                 *action_name,
                                                               const char                 *property_name);

struct _PanelWorkspaceClass
{
  AdwApplicationWindowClass parent_class;

  /*< private >*/
  gpointer _reserved[8];
};

PANEL_AVAILABLE_IN_1_4
PanelWorkspace *panel_workspace_find_from_widget              (GtkWidget                  *widget);
PANEL_AVAILABLE_IN_1_4
PanelWorkbench *panel_workspace_get_workbench                 (PanelWorkspace             *self);
PANEL_AVAILABLE_IN_1_4
const char     *panel_workspace_get_id                        (PanelWorkspace             *self);
PANEL_AVAILABLE_IN_1_4
void            panel_workspace_set_id                        (PanelWorkspace             *self,
                                                               const char                 *id);
PANEL_AVAILABLE_IN_1_4
PanelInhibitor *panel_workspace_inhibit                       (PanelWorkspace             *self,
                                                               GtkApplicationInhibitFlags  flags,
                                                               const char                 *reason);
PANEL_AVAILABLE_IN_1_4
void            panel_workspace_action_set_enabled            (PanelWorkspace             *self,
                                                               const char                 *action_name,
                                                               gboolean                    enabled);
PANEL_AVAILABLE_IN_1_4
void            panel_workspace_class_install_action          (PanelWorkspaceClass        *workspace_class,
                                                               const char                 *action_name,
                                                               const char                 *parameter_type,
                                                               PanelActionActivateFunc     activate);
PANEL_AVAILABLE_IN_1_4
void            panel_workspace_class_install_property_action (PanelWorkspaceClass        *workspace_class,
                                                               const char                 *action_name,
                                                               const char                 *property_name);

G_END_DECLS
