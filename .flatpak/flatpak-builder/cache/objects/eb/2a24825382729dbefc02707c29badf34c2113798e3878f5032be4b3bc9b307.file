/* panel-frame.h
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

#define PANEL_TYPE_FRAME (panel_frame_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_DERIVABLE_TYPE (PanelFrame, panel_frame, PANEL, FRAME, GtkWidget)

struct _PanelFrameClass
{
  GtkWidgetClass parent_class;

  void     (*page_closed)    (PanelFrame   *self,
                              PanelWidget  *widget);
  gboolean (*adopt_widget)   (PanelFrame   *self,
                              PanelWidget  *widget);

  /*< private >*/
  gpointer _reserved[6];
};

PANEL_AVAILABLE_IN_ALL
GtkWidget         *panel_frame_new                (void);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_frame_get_closeable      (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
PanelFrameHeader  *panel_frame_get_header         (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_set_header         (PanelFrame       *self,
                                                   PanelFrameHeader *header);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_frame_get_empty          (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_add                (PanelFrame       *self,
                                                   PanelWidget      *panel);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_add_before         (PanelFrame       *self,
                                                   PanelWidget      *panel,
                                                   PanelWidget      *sibling);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_remove             (PanelFrame       *self,
                                                   PanelWidget      *panel);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_set_visible_child  (PanelFrame       *self,
                                                   PanelWidget      *widget);
PANEL_AVAILABLE_IN_ALL
PanelWidget       *panel_frame_get_visible_child  (PanelFrame       *self);
PANEL_AVAILABLE_IN_1_2
void               panel_frame_set_child_pinned   (PanelFrame       *self,
                                                   PanelWidget      *child,
                                                   gboolean          pinned);
PANEL_AVAILABLE_IN_ALL
PanelWidget       *panel_frame_get_page           (PanelFrame       *self,
                                                   guint             n);
PANEL_AVAILABLE_IN_ALL
GtkSelectionModel *panel_frame_get_pages          (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
guint              panel_frame_get_n_pages        (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
GtkWidget         *panel_frame_get_placeholder    (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_set_placeholder    (PanelFrame       *self,
                                                   GtkWidget        *placeholder);
PANEL_AVAILABLE_IN_ALL
PanelPosition     *panel_frame_get_position       (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
int                panel_frame_get_requested_size (PanelFrame       *self);
PANEL_AVAILABLE_IN_ALL
void               panel_frame_set_requested_size (PanelFrame       *self,
                                                   int               requested_size);

G_END_DECLS
