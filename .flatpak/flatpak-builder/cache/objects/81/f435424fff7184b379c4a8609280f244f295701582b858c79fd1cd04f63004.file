/* panel-widget.h
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

#define PANEL_TYPE_WIDGET (panel_widget_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_DERIVABLE_TYPE (PanelWidget, panel_widget, PANEL, WIDGET, GtkWidget)

struct _PanelWidgetClass
{
  GtkWidgetClass  parent_instance;

  GtkWidget      *(*get_default_focus) (PanelWidget *self);
  void            (*presented)         (PanelWidget *self);

  /*< private >*/
  gpointer _reserved[8];
};

#define PANEL_WIDGET_KIND_ANY      "*"
#define PANEL_WIDGET_KIND_UNKNOWN  "unknown"
#define PANEL_WIDGET_KIND_DOCUMENT "document"
#define PANEL_WIDGET_KIND_UTILITY  "utility"

PANEL_AVAILABLE_IN_ALL
GtkWidget         *panel_widget_new                           (void);
PANEL_AVAILABLE_IN_ALL
const char        *panel_widget_get_id                        (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_id                        (PanelWidget                 *self,
                                                               const char                  *id);
PANEL_AVAILABLE_IN_ALL
GtkWidget         *panel_widget_get_child                     (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_child                     (PanelWidget                 *self,
                                                               GtkWidget                   *child);
PANEL_AVAILABLE_IN_ALL
const char        *panel_widget_get_title                     (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_title                     (PanelWidget                 *self,
                                                               const char                  *title);
PANEL_AVAILABLE_IN_ALL
GIcon             *panel_widget_get_icon                      (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_icon                      (PanelWidget                 *self,
                                                               GIcon                       *icon);
PANEL_AVAILABLE_IN_ALL
const char        *panel_widget_get_icon_name                 (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_icon_name                 (PanelWidget                 *self,
                                                               const char                  *icon_name);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_widget_get_reorderable               (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_reorderable               (PanelWidget                 *self,
                                                               gboolean                     reorderable);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_widget_get_can_maximize              (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_can_maximize              (PanelWidget                 *self,
                                                               gboolean                     can_maximize);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_widget_get_modified                  (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_modified                  (PanelWidget                 *self,
                                                               gboolean                     modified);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_widget_get_needs_attention           (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_needs_attention           (PanelWidget                 *self,
                                                               gboolean                     needs_attention);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_maximize                      (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_unmaximize                    (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
const char        *panel_widget_get_kind                      (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_kind                      (PanelWidget                 *self,
                                                               const char                  *kind);
PANEL_AVAILABLE_IN_1_2
const char        *panel_widget_get_tooltip                   (PanelWidget                 *self);
PANEL_AVAILABLE_IN_1_2
void               panel_widget_set_tooltip                   (PanelWidget                 *self,
                                                               const char                  *tooltip);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_widget_get_busy                      (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_mark_busy                     (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_unmark_busy                   (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
GMenuModel        *panel_widget_get_menu_model                (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_menu_model                (PanelWidget                 *self,
                                                               GMenuModel                  *menu_model);
PANEL_AVAILABLE_IN_ALL
PanelPosition     *panel_widget_get_position                  (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_raise                         (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
GtkWidget         *panel_widget_get_default_focus             (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_widget_focus_default                 (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
PanelSaveDelegate *panel_widget_get_save_delegate             (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_set_save_delegate             (PanelWidget                 *self,
                                                               PanelSaveDelegate           *save_delegate);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_close                         (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_force_close                   (PanelWidget                 *self);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_insert_action_group           (PanelWidget                 *self,
                                                               const char                  *prefix,
                                                               GActionGroup                *group);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_class_install_action          (PanelWidgetClass            *widget_class,
                                                               const char                  *action_name,
                                                               const char                  *parameter_type,
                                                               GtkWidgetActionActivateFunc  activate);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_action_set_enabled            (PanelWidget                 *widget,
                                                               const char                  *action_name,
                                                               gboolean                     enabled);
PANEL_AVAILABLE_IN_ALL
void               panel_widget_class_install_property_action (PanelWidgetClass            *widget_class,
                                                               const char                  *action_name,
                                                               const char                  *property_name);

G_END_DECLS
