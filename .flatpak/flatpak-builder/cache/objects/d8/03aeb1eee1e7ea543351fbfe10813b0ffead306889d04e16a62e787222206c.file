/* panel-init.c
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

#include "config.h"

#include <glib/gi18n-lib.h>
#include <adwaita.h>

#include "panel-dock.h"
#include "panel-dock-child-private.h"
#include "panel-enums.h"
#include "panel-frame.h"
#include "panel-frame-header.h"
#include "panel-frame-switcher.h"
#include "panel-grid.h"
#include "panel-grid-column.h"
#include "panel-init.h"
#include "panel-omni-bar.h"
#include "panel-paned.h"
#include "panel-resources.h"
#include "panel-statusbar.h"
#include "panel-theme-selector.h"
#include "panel-toggle-button.h"
#include "panel-widget.h"

static GtkCssProvider *css_provider;

void
panel_init (void)
{
  if (css_provider)
    return;

  adw_init ();

  bind_textdomain_codeset (GETTEXT_PACKAGE, "UTF-8");
  bindtextdomain (GETTEXT_PACKAGE, LOCALEDIR);

  g_resources_register (panel_get_resource ());

  g_type_ensure (PANEL_TYPE_AREA);
  g_type_ensure (PANEL_TYPE_DOCK);
  g_type_ensure (PANEL_TYPE_DOCK_CHILD);
  g_type_ensure (PANEL_TYPE_FRAME);
  g_type_ensure (PANEL_TYPE_FRAME_HEADER);
  g_type_ensure (PANEL_TYPE_FRAME_SWITCHER);
  g_type_ensure (PANEL_TYPE_GRID);
  g_type_ensure (PANEL_TYPE_GRID_COLUMN);
  g_type_ensure (PANEL_TYPE_OMNI_BAR);
  g_type_ensure (PANEL_TYPE_PANED);
  g_type_ensure (PANEL_TYPE_STATUSBAR);
  g_type_ensure (PANEL_TYPE_THEME_SELECTOR);
  g_type_ensure (PANEL_TYPE_TOGGLE_BUTTON);
  g_type_ensure (PANEL_TYPE_WIDGET);

  css_provider = gtk_css_provider_new ();
  gtk_css_provider_load_from_resource (css_provider, "/org/gnome/libpanel/stylesheet.css");
  gtk_style_context_add_provider_for_display (gdk_display_get_default (),
                                              GTK_STYLE_PROVIDER (css_provider),
                                              GTK_STYLE_PROVIDER_PRIORITY_APPLICATION-2);
}

void
panel_finalize (void)
{
  if (!css_provider)
    return;

  gtk_style_context_remove_provider_for_display (gdk_display_get_default (),
                                                 GTK_STYLE_PROVIDER (css_provider));
  g_clear_object (&css_provider);

  g_resources_unregister (panel_get_resource ());
}

guint
panel_get_major_version (void)
{
  return PANEL_MAJOR_VERSION;
}

guint
panel_get_micro_version (void)
{
  return PANEL_MICRO_VERSION;
}

guint
panel_get_minor_version (void)
{
  return PANEL_MINOR_VERSION;
}

gboolean
panel_check_version (guint major,
                     guint minor,
                     guint micro)
{
  return PANEL_CHECK_VERSION (major, minor, micro);
}
