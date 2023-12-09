/* panel-omni-bar.h
 *
 * Copyright 2022 Christian Hergert <chergert@redhat.com>
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

#define PANEL_TYPE_OMNI_BAR (panel_omni_bar_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_DERIVABLE_TYPE (PanelOmniBar, panel_omni_bar, PANEL, OMNI_BAR, GtkWidget)

struct _PanelOmniBarClass
{
  GtkWidgetClass parent_class;

  /*< private >*/
  gpointer _reserved[8];
};

PANEL_AVAILABLE_IN_ALL
GtkWidget  *panel_omni_bar_new           (void);
PANEL_AVAILABLE_IN_ALL
GtkPopover *panel_omni_bar_get_popover   (PanelOmniBar *self);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_set_popover   (PanelOmniBar *self,
                                          GtkPopover   *popover);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_add_prefix    (PanelOmniBar *self,
                                          int           priority,
                                          GtkWidget    *widget);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_add_suffix    (PanelOmniBar *self,
                                          int           priority,
                                          GtkWidget    *widget);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_remove        (PanelOmniBar *self,
                                          GtkWidget    *widget);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_start_pulsing (PanelOmniBar *self);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_stop_pulsing  (PanelOmniBar *self);
PANEL_AVAILABLE_IN_ALL
double      panel_omni_bar_get_progress  (PanelOmniBar *self);
PANEL_AVAILABLE_IN_ALL
void        panel_omni_bar_set_progress  (PanelOmniBar *self,
                                          double        progress);

G_END_DECLS
