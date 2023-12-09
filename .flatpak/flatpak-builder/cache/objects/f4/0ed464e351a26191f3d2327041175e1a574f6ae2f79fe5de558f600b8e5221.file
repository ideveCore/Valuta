/* panel-save-delegate.h
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

#define PANEL_TYPE_SAVE_DELEGATE (panel_save_delegate_get_type())

PANEL_AVAILABLE_IN_ALL
G_DECLARE_DERIVABLE_TYPE (PanelSaveDelegate, panel_save_delegate, PANEL, SAVE_DELEGATE, GObject)

struct _PanelSaveDelegateClass
{
  GObjectClass parent_class;

  void     (*save_async)  (PanelSaveDelegate   *self,
                           GCancellable        *cancellable,
                           GAsyncReadyCallback  callback,
                           gpointer             user_data);
  gboolean (*save_finish) (PanelSaveDelegate  *self,
                           GAsyncResult       *result,
                           GError            **error);
  gboolean (*save)        (PanelSaveDelegate  *self,
                           GTask              *task);
  void     (*discard)     (PanelSaveDelegate  *self);
  void     (*close)       (PanelSaveDelegate  *self);

  /*< private >*/
  gpointer _reserved[8];
};

PANEL_AVAILABLE_IN_ALL
PanelSaveDelegate *panel_save_delegate_new           (void);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_save_delegate_get_is_draft  (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_set_is_draft  (PanelSaveDelegate    *self,
                                                      gboolean              is_draft);
PANEL_AVAILABLE_IN_ALL
const char        *panel_save_delegate_get_icon_name (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_set_icon_name (PanelSaveDelegate    *self,
                                                      const char           *icon);
PANEL_AVAILABLE_IN_ALL
GIcon             *panel_save_delegate_get_icon      (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_set_icon      (PanelSaveDelegate    *self,
                                                      GIcon                *icon);
PANEL_AVAILABLE_IN_ALL
const char        *panel_save_delegate_get_subtitle  (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_set_subtitle  (PanelSaveDelegate    *self,
                                                      const char           *subtitle);
PANEL_AVAILABLE_IN_ALL
const char        *panel_save_delegate_get_title     (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_set_title     (PanelSaveDelegate    *self,
                                                      const char           *title);
PANEL_AVAILABLE_IN_ALL
double             panel_save_delegate_get_progress  (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_set_progress  (PanelSaveDelegate    *self,
                                                      double                progress);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_save_async    (PanelSaveDelegate    *self,
                                                      GCancellable         *cancellable,
                                                      GAsyncReadyCallback   callback,
                                                      gpointer              user_data);
PANEL_AVAILABLE_IN_ALL
gboolean           panel_save_delegate_save_finish   (PanelSaveDelegate    *self,
                                                      GAsyncResult         *result,
                                                      GError              **error);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_close         (PanelSaveDelegate    *self);
PANEL_AVAILABLE_IN_ALL
void               panel_save_delegate_discard       (PanelSaveDelegate    *self);

G_END_DECLS
