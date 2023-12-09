/* panel-theme-selector.c
 *
 * Copyright 2021-2022 Christian Hergert <chergert@redhat.com>
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

#include <adwaita.h>

#include "panel-theme-selector.h"

/**
 * PanelThemeSelector:
 *
 * A widget that allow selecting theme preference between "dark",
 * "light" and "follow" the system preference.
 *
 * <picture>
 *   <source srcset="theme-selector-dark.png" media="(prefers-color-scheme: dark)">
 *   <img src="theme-selector.png" alt="theme-selector">
 * </picture>
 *
 * Upon activation it will activate the named action in
 * #PanelThemeSelector:action-name.
 */
struct _PanelThemeSelector
{
  GtkWidget        parent_instance;

  /* Template widgets */
  GtkWidget       *box;
  GtkToggleButton *dark;
  GtkToggleButton *light;
  GtkToggleButton *follow;

  char            *action_name;
};

G_DEFINE_TYPE (PanelThemeSelector, panel_theme_selector, GTK_TYPE_WIDGET)

enum {
  PROP_0,
  PROP_ACTION_NAME,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

/**
 * panel_theme_selector_new:
 *
 * Create a new #ThemeSelector.
 *
 * Returns: a newly created #PanelThemeSelector.
 */
GtkWidget *
panel_theme_selector_new (void)
{
  return g_object_new (PANEL_TYPE_THEME_SELECTOR, NULL);
}

static void
on_notify_system_supports_color_schemes_cb (PanelThemeSelector *self,
                                            GParamSpec          *pspec,
                                            AdwStyleManager     *style_manager)
{
  gboolean visible;

  g_assert (PANEL_IS_THEME_SELECTOR (self));
  g_assert (ADW_IS_STYLE_MANAGER (style_manager));

  visible = adw_style_manager_get_system_supports_color_schemes (style_manager);
  gtk_widget_set_visible (GTK_WIDGET (self->follow), visible);
}

static void
on_notify_dark_cb (PanelThemeSelector *self,
                   GParamSpec          *pspec,
                   AdwStyleManager     *style_manager)
{
  g_assert (PANEL_IS_THEME_SELECTOR (self));
  g_assert (ADW_IS_STYLE_MANAGER (style_manager));

  style_manager = adw_style_manager_get_default ();

  if (adw_style_manager_get_dark (style_manager))
    gtk_widget_add_css_class (GTK_WIDGET (self), "dark");
  else
    gtk_widget_remove_css_class (GTK_WIDGET (self), "dark");
}

static void
panel_theme_selector_dispose (GObject *object)
{
  PanelThemeSelector *self = (PanelThemeSelector *)object;

  g_clear_pointer (&self->box, gtk_widget_unparent);
  g_clear_pointer (&self->action_name, g_free);

  G_OBJECT_CLASS (panel_theme_selector_parent_class)->dispose (object);
}

static void
panel_theme_selector_get_property (GObject    *object,
                                   guint       prop_id,
                                   GValue     *value,
                                   GParamSpec *pspec)
{
  PanelThemeSelector *self = PANEL_THEME_SELECTOR (object);

  switch (prop_id)
    {
    case PROP_ACTION_NAME:
      g_value_set_string (value, panel_theme_selector_get_action_name (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_theme_selector_set_property (GObject      *object,
                                   guint         prop_id,
                                   const GValue *value,
                                   GParamSpec   *pspec)
{
  PanelThemeSelector *self = PANEL_THEME_SELECTOR (object);

  switch (prop_id)
    {
    case PROP_ACTION_NAME:
      panel_theme_selector_set_action_name (self, g_value_get_string (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_theme_selector_class_init (PanelThemeSelectorClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_theme_selector_dispose;
  object_class->get_property = panel_theme_selector_get_property;
  object_class->set_property = panel_theme_selector_set_property;

  /**
   * PanelThemeSelector:action-name
   *
   * The name of the action activated on activation.
   */
  properties [PROP_ACTION_NAME] =
    g_param_spec_string ("action-name",
                         "Action Name",
                         "The action to bind choices to",
                         NULL,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_css_name (widget_class, "panelthemeselector");
  gtk_widget_class_set_template_from_resource (widget_class, "/org/gnome/libpanel/panel-theme-selector.ui");
  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
  gtk_widget_class_bind_template_child (widget_class, PanelThemeSelector, box);
  gtk_widget_class_bind_template_child (widget_class, PanelThemeSelector, dark);
  gtk_widget_class_bind_template_child (widget_class, PanelThemeSelector, light);
  gtk_widget_class_bind_template_child (widget_class, PanelThemeSelector, follow);
}

static void
panel_theme_selector_init (PanelThemeSelector *self)
{
  AdwStyleManager *style_manager = adw_style_manager_get_default ();
  gboolean dark;

  gtk_widget_init_template (GTK_WIDGET (self));

  g_signal_connect_object (style_manager,
                           "notify::system-supports-color-schemes",
                           G_CALLBACK (on_notify_system_supports_color_schemes_cb),
                           self,
                           G_CONNECT_SWAPPED);

  g_signal_connect_object (style_manager,
                           "notify::dark",
                           G_CALLBACK (on_notify_dark_cb),
                           self,
                           G_CONNECT_SWAPPED);

  dark = adw_style_manager_get_dark (style_manager);
  self->action_name = g_strdup (dark ? "dark" : "light");

  on_notify_system_supports_color_schemes_cb (self, NULL, style_manager);
  on_notify_dark_cb (self, NULL, style_manager);
}

/**
 * panel_theme_selector_get_action_name:
 * @self: a #PanelThemeSelector
 *
 * Gets the name of the action that will be activated.
 *
 * Returns: (transfer none): the name of the action.
 */
const char *
panel_theme_selector_get_action_name (PanelThemeSelector *self)
{
  g_return_val_if_fail (PANEL_IS_THEME_SELECTOR (self), NULL);

  return self->action_name;
}

/**
 * panel_theme_selector_set_action_name:
 * @self: a #PanelThemeSelector
 * @action_name: (transfer none): the action name.
 *
 * Sets the name of the action that will be activated.
 */
void
panel_theme_selector_set_action_name (PanelThemeSelector *self,
                                      const char         *action_name)
{
  g_return_if_fail (PANEL_IS_THEME_SELECTOR (self));

  if (g_strcmp0 (action_name, self->action_name) != 0)
    {
      g_free (self->action_name);
      self->action_name = g_strdup (action_name);
      gtk_actionable_set_action_name (GTK_ACTIONABLE (self->dark), action_name);
      gtk_actionable_set_action_name (GTK_ACTIONABLE (self->light), action_name);
      gtk_actionable_set_action_name (GTK_ACTIONABLE (self->follow), action_name);
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_ACTION_NAME]);
    }
}
