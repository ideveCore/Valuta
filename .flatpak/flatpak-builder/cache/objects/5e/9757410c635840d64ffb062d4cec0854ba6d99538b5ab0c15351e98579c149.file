/* example-page.c
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

#ifdef HAVE_GTKSOURCEVIEW
# include <gtksourceview/gtksource.h>
#endif

#include "example-page.h"

struct _ExamplePage
{
  PanelWidget   parent_instance;

  GtkTextView  *text_view;
  GtkIMContext *im_context;
};

G_DEFINE_TYPE (ExamplePage, example_page, PANEL_TYPE_WIDGET)

enum {
  PROP_0,
  PROP_COMMAND_TEXT,
  PROP_COMMAND_BAR_TEXT,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

GtkWidget *
example_page_new (void)
{
  return g_object_new (EXAMPLE_TYPE_PAGE, NULL);
}

static gboolean
tick_cb (gpointer user_data)
{
  GTask *task = user_data;
  PanelSaveDelegate *delegate = g_task_get_source_object (task);
  double progress = panel_save_delegate_get_progress (delegate);

  if (g_task_had_error (task) ||
      g_task_return_error_if_cancelled (task))
    return G_SOURCE_REMOVE;

  progress = CLAMP (progress+.005, .0, 1.);
  panel_save_delegate_set_progress (delegate, progress);

  if (progress >= 1.)
    {
      g_task_return_boolean (task, TRUE);
      return G_SOURCE_REMOVE;
    }

  return G_SOURCE_CONTINUE;
}

static gboolean
example_page_save (ExamplePage       *self,
                   GTask             *task,
                   PanelSaveDelegate *delegate)
{
  g_assert (EXAMPLE_IS_PAGE (self));
  g_assert (G_IS_TASK (task));
  g_assert (PANEL_IS_SAVE_DELEGATE (delegate));

  g_timeout_add_full (G_PRIORITY_DEFAULT,
                      30,
                      tick_cb,
                      g_object_ref (task),
                      g_object_unref);

  return TRUE;
}

static void
on_vim_notify_cb (ExamplePage  *self,
                  GParamSpec   *pspec,
                  GtkIMContext *im_context)
{
  if (g_strcmp0 (pspec->name, "command-bar-text") == 0 ||
      g_strcmp0 (pspec->name, "command-text") == 0)
    g_object_notify (G_OBJECT (self), pspec->name);
}

static GtkWidget *
example_page_get_default_focus (PanelWidget *widget)
{
  return GTK_WIDGET (EXAMPLE_PAGE (widget)->text_view);
}

static void
example_page_dispose (GObject *object)
{
  ExamplePage *self = (ExamplePage *)object;

  g_clear_object (&self->im_context);

  G_OBJECT_CLASS (example_page_parent_class)->dispose (object);
}

static void
example_page_get_property (GObject    *object,
                           guint       prop_id,
                           GValue     *value,
                           GParamSpec *pspec)
{
  ExamplePage *self = EXAMPLE_PAGE (object);

  switch (prop_id)
    {
    #ifdef HAVE_GTKSOURCEVIEW
    case PROP_COMMAND_TEXT:
      if (self->im_context)
        g_value_set_string (value, gtk_source_vim_im_context_get_command_text (GTK_SOURCE_VIM_IM_CONTEXT (self->im_context)));
      break;

    case PROP_COMMAND_BAR_TEXT:
      if (self->im_context)
        g_value_set_string (value, gtk_source_vim_im_context_get_command_bar_text (GTK_SOURCE_VIM_IM_CONTEXT (self->im_context)));
      break;
    #endif

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
example_page_class_init (ExamplePageClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  PanelWidgetClass *p_widget_class = PANEL_WIDGET_CLASS (klass);

  p_widget_class->get_default_focus = example_page_get_default_focus;

  object_class->dispose = example_page_dispose;
  object_class->get_property = example_page_get_property;

  #ifdef HAVE_GTKSOURCEVIEW
  properties [PROP_COMMAND_TEXT] =
    g_param_spec_string ("command-text",
                         "Command Text",
                         "Command Text",
                         NULL,
                         (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));

  properties [PROP_COMMAND_BAR_TEXT] =
    g_param_spec_string ("command-bar-text",
                         "Command Bar Text",
                         "Command Bar Text",
                         NULL,
                         (G_PARAM_READABLE | G_PARAM_STATIC_STRINGS));
  #endif

  g_object_class_install_properties (object_class, N_PROPS, properties);
}

static void
example_page_init (ExamplePage *self)
{
  PanelSaveDelegate *delegate = NULL;
  GtkWidget *scroller;

  scroller = gtk_scrolled_window_new ();
  panel_widget_set_child (PANEL_WIDGET (self), scroller);

#ifdef HAVE_GTKSOURCEVIEW
  {
    GtkSourceLanguageManager *langs = gtk_source_language_manager_get_default ();
    GtkSourceLanguage *lang = gtk_source_language_manager_get_language (langs, "c");
    GtkSourceStyleSchemeManager *schemes = gtk_source_style_scheme_manager_get_default ();
    GtkSourceStyleScheme *scheme = gtk_source_style_scheme_manager_get_scheme (schemes, "Adwaita");
    GtkEventController *event_controller;
    GtkSourceBuffer *buffer;

    self->text_view = GTK_TEXT_VIEW (gtk_source_view_new ());
    buffer = GTK_SOURCE_BUFFER (gtk_text_view_get_buffer (self->text_view));

    gtk_source_view_set_show_line_numbers (GTK_SOURCE_VIEW (self->text_view), TRUE);

    gtk_source_buffer_set_language (buffer, lang);
    gtk_source_buffer_set_style_scheme (buffer, scheme);

    self->im_context = gtk_source_vim_im_context_new ();
    gtk_im_context_set_client_widget (self->im_context,
                                      GTK_WIDGET (self->text_view));
    g_signal_connect_object (self->im_context,
                             "notify",
                             G_CALLBACK (on_vim_notify_cb),
                             self,
                             G_CONNECT_SWAPPED);
    event_controller = gtk_event_controller_key_new ();
    gtk_event_controller_set_propagation_phase (event_controller, GTK_PHASE_CAPTURE);
    gtk_event_controller_key_set_im_context (GTK_EVENT_CONTROLLER_KEY (event_controller),
                                             self->im_context);
    gtk_widget_add_controller (GTK_WIDGET (self->text_view), event_controller);
  }
#else
  self->text_view = GTK_TEXT_VIEW (gtk_text_view_new ());
#endif

  g_object_set (self->text_view,
                "monospace", TRUE,
                "left-margin", 6,
                "top-margin", 6,
                NULL);

  gtk_scrolled_window_set_child (GTK_SCROLLED_WINDOW (scroller),
                                 GTK_WIDGET (self->text_view));

  delegate = panel_save_delegate_new ();
  g_signal_connect_object (delegate,
                           "save",
                           G_CALLBACK (example_page_save),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_swapped (delegate, "discard", G_CALLBACK (panel_widget_force_close), self);
  g_signal_connect_swapped (delegate, "close", G_CALLBACK (panel_widget_force_close), self);
  g_object_bind_property (self, "title", delegate, "title", G_BINDING_SYNC_CREATE);
  g_object_bind_property (self, "icon", delegate, "icon", G_BINDING_SYNC_CREATE);
  panel_save_delegate_set_subtitle (delegate, "~/Documents");
  panel_widget_set_save_delegate (PANEL_WIDGET (self), delegate);
  g_clear_object (&delegate);
}
