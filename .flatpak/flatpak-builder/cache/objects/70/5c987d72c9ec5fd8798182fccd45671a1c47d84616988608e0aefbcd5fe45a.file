/* example-window.c
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

#include <libpanel.h>

#include "example-page.h"
#include "example-window.h"

struct _ExampleWindow
{
  GtkApplicationWindow parent_instance;
  PanelDock *dock;
  PanelGrid *grid;
  GMenuModel *page_menu;
  GtkDropDown *language;
  GtkToggleButton *frame_header_bar;
  GtkMenuButton *primary_button;
  AdwSplitButton *run_button;
  PanelThemeSelector *theme_selector;
  GtkLabel *command;
  GtkLabel *command_bar;
};

G_DEFINE_TYPE (ExampleWindow, example_window, ADW_TYPE_APPLICATION_WINDOW)

static GdkRGBA white;
static GdkRGBA grey;
static GdkRGBA black;

GtkWidget *
example_window_new (GtkApplication *application)
{
  return g_object_new (EXAMPLE_TYPE_WINDOW,
                       "application", application,
                       NULL);
}

static gboolean
text_to_visible (GBinding     *binding,
                 const GValue *from_value,
                 GValue       *to_value,
                 gpointer      user_data)
{
  const char *str = g_value_get_string (from_value);
  g_value_set_boolean (to_value, str && *str);
  return TRUE;
}

static void
example_window_add_document (ExampleWindow *self)
{
  static guint count;
  PanelWidget *widget;
  char *title;
  char *tooltip;

  g_return_if_fail (EXAMPLE_IS_WINDOW (self));

  title = g_strdup_printf ("Untitled Document %u", ++count);
  tooltip = g_strdup_printf ("Draft: %s", title);
  widget = g_object_new (EXAMPLE_TYPE_PAGE,
                         "title", title,
                         "tooltip", tooltip,
                         "kind", PANEL_WIDGET_KIND_DOCUMENT,
                         "icon-name", "text-x-generic-symbolic",
                         "menu-model", self->page_menu,
                         "can-maximize", TRUE,
                         "modified", TRUE,
                         NULL);

  panel_grid_add (self->grid, widget);
  panel_widget_raise (widget);
  panel_widget_focus_default (widget);

  /* You really want to use a BindingGroup or something for this
   * to only connect to the active page.
   */
  g_object_bind_property (widget, "command-bar-text", self->command_bar, "label", 0);
  g_object_bind_property_full (widget, "command-text", self->command, "visible", 0, text_to_visible, NULL, NULL, NULL);
  g_object_bind_property (widget, "command-text", self->command, "label", 0);

  g_free (title);
  g_free (tooltip);
}

static void
add_document_action (GtkWidget  *widget,
                     const char *action_name,
                     GVariant   *param)
{
  example_window_add_document (EXAMPLE_WINDOW (widget));
}

static void
project_build_action (GtkWidget  *widget,
                      const char *action_name,
                      GVariant   *param)
{
}

static void
set_theme_action (GSimpleAction *action,
                  GVariant      *param,
                  gpointer       user_data)
{
  const char *str = g_variant_get_string (param, NULL);
  AdwStyleManager *manager = adw_style_manager_get_default ();

  if (g_strcmp0 (str, "default") == 0)
    adw_style_manager_set_color_scheme (manager, ADW_COLOR_SCHEME_DEFAULT);
  else if (g_strcmp0 (str, "light") == 0)
    adw_style_manager_set_color_scheme (manager, ADW_COLOR_SCHEME_FORCE_LIGHT);
  else if (g_strcmp0 (str, "dark") == 0)
    adw_style_manager_set_color_scheme (manager, ADW_COLOR_SCHEME_FORCE_DARK);
}

static void
set_runner_action (GSimpleAction *action,
                   GVariant      *param,
                   gpointer       user_data)
{
  g_simple_action_set_state (action, param);
}

static void
set_high_contrast_action (GSimpleAction *action,
                          GVariant      *param,
                          gpointer       user_data)
{
  GVariant *v = g_action_get_state (G_ACTION (action));

  if (!v ||
      !g_variant_is_of_type (v, G_VARIANT_TYPE_BOOLEAN) ||
      g_variant_get_boolean (v) == FALSE)
    g_simple_action_set_state (action, g_variant_new_boolean (TRUE));
  else
    g_simple_action_set_state (action, g_variant_new_boolean (FALSE));

  g_clear_pointer (&v, g_variant_unref);
}

static void
set_rtl_action (GSimpleAction *action,
                GVariant      *param,
                gpointer       user_data)
{
  GVariant *v = g_action_get_state (G_ACTION (action));

  if (!v ||
      !g_variant_is_of_type (v, G_VARIANT_TYPE_BOOLEAN) ||
      g_variant_get_boolean (v) == FALSE)
    g_simple_action_set_state (action, g_variant_new_boolean (TRUE));
  else
    g_simple_action_set_state (action, g_variant_new_boolean (FALSE));

  g_clear_pointer (&v, g_variant_unref);
}

static void
notify_theme_cb (ExampleWindow   *self,
                 GParamSpec      *pspec,
                 AdwStyleManager *style_manager)
{
  const char *name;
  GAction *action;

  g_assert (EXAMPLE_IS_WINDOW (self));
  g_assert (ADW_IS_STYLE_MANAGER (style_manager));

  switch (adw_style_manager_get_color_scheme (style_manager))
    {
    case ADW_COLOR_SCHEME_PREFER_DARK:
    case ADW_COLOR_SCHEME_FORCE_DARK:
      name = "dark";
      break;

    case ADW_COLOR_SCHEME_FORCE_LIGHT:
    case ADW_COLOR_SCHEME_PREFER_LIGHT:
      name = "light";
      break;

    case ADW_COLOR_SCHEME_DEFAULT:
    default:
      if (!adw_style_manager_get_system_supports_color_schemes (style_manager))
        name = "light";
      else
        name = "default";
      break;
    }


  action = g_action_map_lookup_action (G_ACTION_MAP (self), "theme");
  g_simple_action_set_state (G_SIMPLE_ACTION (action),
                             g_variant_new_string (name));
}

static PanelFrame *
create_frame_cb (PanelGrid     *grid,
                 ExampleWindow *self)
{
  PanelFrame *frame;
  PanelFrameHeader *header;
  AdwStatusPage *status;
  GtkGrid *shortcuts;
  GtkWidget *child;

  g_assert (EXAMPLE_IS_WINDOW (self));

  frame = PANEL_FRAME (panel_frame_new ());

  status = ADW_STATUS_PAGE (adw_status_page_new ());
  adw_status_page_set_title (status, "Open a File or Terminal");
  adw_status_page_set_icon_name (status, "document-new-symbolic");
  adw_status_page_set_description (status, "Use the page switcher above or use one of the following:");
  shortcuts = GTK_GRID (gtk_grid_new ());
  gtk_grid_set_row_spacing (shortcuts, 6);
  gtk_grid_set_column_spacing (shortcuts, 32);
  gtk_widget_set_halign (GTK_WIDGET (shortcuts), GTK_ALIGN_CENTER);
  gtk_grid_attach (shortcuts, gtk_label_new ("New Document"), 0, 0, 1, 1);
  gtk_grid_attach (shortcuts, gtk_label_new ("Ctrl+N"), 1, 0, 1, 1);
  gtk_grid_attach (shortcuts, gtk_label_new ("Close Document"), 0, 1, 1, 1);
  gtk_grid_attach (shortcuts, gtk_label_new ("Ctrl+W"), 1, 1, 1, 1);
  for (child = gtk_widget_get_first_child (GTK_WIDGET (shortcuts));
       child;
       child = gtk_widget_get_next_sibling (child))
    gtk_widget_set_halign (child, GTK_ALIGN_START);
  adw_status_page_set_child (status, GTK_WIDGET (shortcuts));
  panel_frame_set_placeholder (frame, GTK_WIDGET (status));

  if (gtk_toggle_button_get_active (self->frame_header_bar))
    header = PANEL_FRAME_HEADER (panel_frame_header_bar_new ());
  else
    header = PANEL_FRAME_HEADER (panel_frame_tab_bar_new ());

  if (PANEL_IS_FRAME_HEADER_BAR (header))
    panel_frame_header_bar_set_show_icon (PANEL_FRAME_HEADER_BAR (header), TRUE);

  panel_frame_set_header (frame, header);
  panel_frame_header_add_prefix (header,
                                 -100,
                                 (child = g_object_new (GTK_TYPE_BUTTON,
                                                        "width-request", 40,
                                                        "focus-on-click", FALSE,
                                                        "icon-name", "go-previous-symbolic",
                                                        NULL)));
  gtk_widget_add_css_class (child, "flat");

  panel_frame_header_add_prefix (header,
                                 -50,
                                 (child = g_object_new (GTK_TYPE_BUTTON,
                                                        "width-request", 40,
                                                        "focus-on-click", FALSE,
                                                        "icon-name", "go-next-symbolic",
                                                        NULL)));
  gtk_widget_add_css_class (child, "flat");

  return frame;
}

static void
example_window_constructed (GObject *object)
{
  ExampleWindow *self = (ExampleWindow *)object;

  G_OBJECT_CLASS (example_window_parent_class)->constructed (object);

  /* Create 0,0 frame */
  (void)panel_grid_column_get_row (panel_grid_get_column (self->grid, 0), 0);
}

static void
example_window_class_init (ExampleWindowClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->constructed = example_window_constructed;

  gtk_widget_class_set_template_from_resource (widget_class, "/example-window.ui");
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, dock);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, grid);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, page_menu);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, frame_header_bar);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, language);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, command);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, command_bar);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, primary_button);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, run_button);
  gtk_widget_class_bind_template_child (widget_class, ExampleWindow, theme_selector);
  gtk_widget_class_bind_template_callback (widget_class, create_frame_cb);

  gtk_widget_class_install_action (widget_class, "document.new", NULL, add_document_action);
  gtk_widget_class_install_action (widget_class, "project.build", NULL, project_build_action);

  gtk_widget_class_add_binding_action (widget_class, GDK_KEY_n, GDK_CONTROL_MASK, "document.new", NULL);
  gtk_widget_class_add_binding_action (widget_class, GDK_KEY_F9, 0, "win.reveal-start", NULL);
  gtk_widget_class_add_binding_action (widget_class, GDK_KEY_F9, GDK_CONTROL_MASK, "win.reveal-bottom", NULL);
  gtk_widget_class_add_binding_action (widget_class, GDK_KEY_F9, GDK_SHIFT_MASK, "win.reveal-end", NULL);

  gdk_rgba_parse (&white, "#fff");
  gdk_rgba_parse (&grey, "#1e1e1e");
  gdk_rgba_parse (&black, "#000");
}

static void
example_window_init (ExampleWindow *self)
{
  static const GActionEntry entries[] = {
    { "theme", NULL, "s", "'default'", set_theme_action },
    { "runner", NULL, "s", "''", set_runner_action },
    { "high-contrast", set_high_contrast_action, NULL, "false" },
    { "right-to-left", set_rtl_action, NULL, "false" },
  };
  GPropertyAction *reveal_start = NULL;
  GPropertyAction *reveal_end = NULL;
  GPropertyAction *reveal_bottom = NULL;
  AdwStyleManager *style_manager = adw_style_manager_get_default ();
  GtkPopover *popover;

  gtk_widget_init_template (GTK_WIDGET (self));

  g_action_map_add_action_entries (G_ACTION_MAP (self), entries, G_N_ELEMENTS (entries), self);
  g_signal_connect_object (style_manager,
                           "notify",
                           G_CALLBACK (notify_theme_cb),
                           self,
                           G_CONNECT_SWAPPED);
  notify_theme_cb (self, NULL, style_manager);

  reveal_start = g_property_action_new ("reveal-start", self->dock, "reveal-start");
  reveal_bottom = g_property_action_new ("reveal-bottom", self->dock, "reveal-bottom");
  reveal_end = g_property_action_new ("reveal-end", self->dock, "reveal-end");

  g_action_map_add_action (G_ACTION_MAP (self), G_ACTION (reveal_start));
  g_action_map_add_action (G_ACTION_MAP (self), G_ACTION (reveal_end));
  g_action_map_add_action (G_ACTION_MAP (self), G_ACTION (reveal_bottom));

  for (GtkWidget *child = gtk_widget_get_first_child (GTK_WIDGET (self->language));
       child;
       child = gtk_widget_get_next_sibling (child))
    {
      /* Override to force upwards */
      if (GTK_IS_POPOVER (child))
        gtk_popover_set_position (GTK_POPOVER (child), GTK_POS_TOP);
    }

  popover = gtk_menu_button_get_popover (self->primary_button);
  gtk_popover_menu_add_child (GTK_POPOVER_MENU (popover),
                              GTK_WIDGET (self->theme_selector),
                              "theme");

  g_clear_object (&reveal_start);
  g_clear_object (&reveal_end);
  g_clear_object (&reveal_bottom);
}
