/* main.c
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

#include <adwaita.h>
#include <libpanel.h>

#include "example-window.h"

static void
on_activate_cb (GtkApplication *app)
{
  GtkWidget *window = example_window_new (app);
  gtk_window_present (GTK_WINDOW (window));
}

static void
on_startup_cb (GtkApplication *app)
{
  panel_init ();
  gtk_icon_theme_add_resource_path (gtk_icon_theme_get_for_display (gdk_display_get_default ()), "/icons");
}

int
main (int argc,
      char *argv[])
{
  GApplication *app;
  int ret;

  app = g_object_new (ADW_TYPE_APPLICATION,
                      "application-id", "org.gnome.libpanel.demo",
                      NULL);
  g_signal_connect (app,
                    "startup",
                    G_CALLBACK (on_startup_cb),
                    NULL);
  g_signal_connect (app,
                    "activate",
                    G_CALLBACK (on_activate_cb),
                    NULL);

  ret = g_application_run (app, argc, argv);

  g_object_unref (app);

  return ret;
}
