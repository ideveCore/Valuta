/* panel-inhibitor.c
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

#include "config.h"

#include "panel-inhibitor-private.h"

struct _PanelInhibitor
{
  GObject         parent_instance;
  GtkApplication *application;
  guint           cookie;
};

G_DEFINE_FINAL_TYPE (PanelInhibitor, panel_inhibitor, G_TYPE_OBJECT)

static void
panel_inhibitor_dispose (GObject *object)
{
  PanelInhibitor *self = (PanelInhibitor *)object;

  panel_inhibitor_uninhibit (self);

  G_OBJECT_CLASS (panel_inhibitor_parent_class)->dispose (object);
}

static void
panel_inhibitor_class_init (PanelInhibitorClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->dispose = panel_inhibitor_dispose;
}

static void
panel_inhibitor_init (PanelInhibitor *self)
{
}

PanelInhibitor *
_panel_inhibitor_new (GtkApplication *application,
                      guint           cookie)
{
  PanelInhibitor *self;

  g_return_val_if_fail (GTK_IS_APPLICATION (application), NULL);

  self = g_object_new (PANEL_TYPE_INHIBITOR, NULL);
  g_set_object (&self->application, application);
  self->cookie = cookie;

  return self;
}

void
panel_inhibitor_uninhibit (PanelInhibitor *self)
{
  g_return_if_fail (PANEL_IS_INHIBITOR (self));

  if (self->application != NULL && self->cookie != 0)
    {
      gtk_application_uninhibit (self->application, self->cookie);

      g_clear_object (&self->application);
      self->cookie = 0;
    }
}
