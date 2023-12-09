/* panel-application.c
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

#include "panel-application.h"
#include "panel-init.h"

G_DEFINE_TYPE (PanelApplication, panel_application, ADW_TYPE_APPLICATION)

static void
panel_application_startup (GApplication *app)
{
  G_APPLICATION_CLASS (panel_application_parent_class)->startup (app);

  panel_init ();
}

static void
panel_application_class_init (PanelApplicationClass *klass)
{
  GApplicationClass *app_class = G_APPLICATION_CLASS (klass);

  app_class->startup = panel_application_startup;
}

static void
panel_application_init (PanelApplication *self)
{
}

PanelApplication *
panel_application_new (const char        *application_id,
                       GApplicationFlags  flags)
{
  return g_object_new (PANEL_TYPE_APPLICATION,
                       "application-id", application_id,
                       "flags", flags,
                       NULL);
}
