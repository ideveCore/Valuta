/* panel-save-dialog.c
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

#include <glib/gi18n.h>

#include <adwaita.h>

#include "panel-save-delegate.h"
#include "panel-save-dialog.h"
#include "panel-save-dialog-row-private.h"

struct _PanelSaveDialog
{
  AdwMessageDialog     parent_instance;

  GPtrArray           *rows;
  GCancellable        *cancellable;
  GTask               *task;

  AdwPreferencesPage  *page;
  AdwPreferencesGroup *group;

  guint                close_after_save : 1;
  guint                discarding : 1;
  guint                saving : 1;
  guint                suppress_close : 1;
};

typedef struct
{
  GPtrArray *delegates;
  guint close_after_save : 1;
} Save;

G_DEFINE_FINAL_TYPE (PanelSaveDialog, panel_save_dialog, ADW_TYPE_MESSAGE_DIALOG)

enum {
  PROP_0,
  PROP_CLOSE_AFTER_SAVE,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

static void
save_free (gpointer data)
{
  Save *save = data;

  g_clear_pointer (&save->delegates, g_ptr_array_unref);
  g_slice_free (Save, save);
}

/**
 * panel_save_dialog_new:
 *
 * Create a new #PanelSaveDialog.
 *
 * Returns: a newly created #PanelSaveDialog
 */
GtkWidget *
panel_save_dialog_new (void)
{
  return g_object_new (PANEL_TYPE_SAVE_DIALOG, NULL);
}

static void
panel_save_dialog_response_cancel_cb (PanelSaveDialog *self,
                                      const char      *response)
{
  GTask *task;

  g_assert (PANEL_IS_SAVE_DIALOG (self));

  if ((task = g_steal_pointer (&self->task)))
    {
      g_cancellable_cancel (self->cancellable);
      if (!g_task_get_completed (task))
        g_task_return_error_if_cancelled (task);
      g_clear_object (&task);
    }
}

static void
panel_save_dialog_response_discard_cb (PanelSaveDialog *self,
                                       const char      *response)
{
  GTask *task;

  g_assert (PANEL_IS_SAVE_DIALOG (self));

  self->discarding = TRUE;

  task = g_steal_pointer (&self->task);

  for (guint i = 0; i < self->rows->len; i++)
    {
      PanelSaveDialogRow *row = g_ptr_array_index (self->rows, i);
      PanelSaveDelegate *delegate = panel_save_dialog_row_get_delegate (row);

      panel_save_delegate_discard (delegate);
    }

  if (!g_task_get_completed (task))
    g_task_return_boolean (task, TRUE);

  g_clear_object (&task);
}

static void
panel_save_dialog_save_cb (GObject      *object,
                           GAsyncResult *result,
                           gpointer      user_data)
{
  PanelSaveDelegate *delegate = (PanelSaveDelegate *)object;
  GTask *task = user_data;
  GError *error = NULL;
  Save *save;

  g_assert (PANEL_IS_SAVE_DELEGATE (delegate));
  g_assert (G_IS_ASYNC_RESULT (result));
  g_assert (G_IS_TASK (task));

  save = g_task_get_task_data (task);

  if (!panel_save_delegate_save_finish (delegate, result, &error))
    {
      if (!g_task_had_error (task))
        g_task_return_error (task, g_steal_pointer (&error));
    }
  else if (save->close_after_save)
    {
      if (!g_task_had_error (task))
        panel_save_delegate_close (delegate);
    }

  g_ptr_array_remove (save->delegates, delegate);

  if (save->delegates->len == 0)
    {
      if (!g_task_had_error (task))
        g_task_return_boolean (task, TRUE);
    }

  g_clear_object (&task);
  g_clear_error (&error);
}

static void
panel_save_dialog_response_save_cb (PanelSaveDialog *self,
                                    const char      *response)
{
  Save *save;

  g_assert (PANEL_IS_SAVE_DIALOG (self));
  g_assert (self->task != NULL);

  adw_message_dialog_set_response_enabled (ADW_MESSAGE_DIALOG (self), "save", FALSE);
  adw_message_dialog_set_response_enabled (ADW_MESSAGE_DIALOG (self), "discard", FALSE);

  self->saving = TRUE;

  save = g_slice_new0 (Save);
  save->close_after_save = self->close_after_save;
  save->delegates = g_ptr_array_new_with_free_func (g_object_unref);
  g_task_set_task_data (self->task, save, save_free);

  for (guint i = 0; i < self->rows->len; i++)
    {
      PanelSaveDialogRow *row = g_ptr_array_index (self->rows, i);
      PanelSaveDelegate *delegate = panel_save_dialog_row_get_delegate (row);

      if (!panel_save_dialog_row_get_selected (row))
        {
          panel_save_delegate_discard (delegate);
          continue;
        }

      g_ptr_array_add (save->delegates, g_object_ref (delegate));

      panel_save_delegate_save_async (delegate,
                                      g_task_get_cancellable (self->task),
                                      panel_save_dialog_save_cb,
                                      g_object_ref (self->task));
    }

  if (save->delegates->len == 0)
    g_task_return_boolean (self->task, TRUE);
}

static void
find_button_and_set_visible (GtkWidget  *parent,
                             const char *label,
                             gboolean    visible)
{
  g_assert (!parent || GTK_IS_WIDGET (parent));

  for (GtkWidget *child = gtk_widget_get_first_child (parent);
       child != NULL;
       child = gtk_widget_get_next_sibling (child))
    {
      if (GTK_IS_BUTTON (child) &&
          g_strcmp0 (label, gtk_button_get_label (GTK_BUTTON (child))) == 0)
        {
          gtk_widget_set_visible (child, visible);
          break;
        }
    }
}

static void
set_response_visible (AdwMessageDialog *dialog,
                      const char       *response,
                      gboolean          visible)
{
  const char *label;
  GObject *wide;
  GObject *narrow;

  g_assert (ADW_IS_MESSAGE_DIALOG (dialog));
  g_assert (response != NULL);
  g_assert (adw_message_dialog_has_response (dialog, response));

  adw_message_dialog_set_response_enabled (dialog, response, visible);

  if (!(label = adw_message_dialog_get_response_label (dialog, response)))
    return;

  if ((wide = gtk_widget_get_template_child (GTK_WIDGET (dialog), ADW_TYPE_MESSAGE_DIALOG, "wide_response_box")))
    find_button_and_set_visible (GTK_WIDGET (wide), label, visible);

  if ((narrow = gtk_widget_get_template_child (GTK_WIDGET (dialog), ADW_TYPE_MESSAGE_DIALOG, "narrow_response_box")))
    find_button_and_set_visible (GTK_WIDGET (narrow), label, visible);
}

static gboolean
panel_save_dialog_close_request_idle_cb (gpointer user_data)
{
  PanelSaveDialog *self = user_data;

  g_assert (PANEL_IS_SAVE_DIALOG (self));

  if (self->saving || self->discarding)
    return G_SOURCE_REMOVE;

  if (!GTK_WINDOW_CLASS (panel_save_dialog_parent_class)->close_request (GTK_WINDOW (self)))
    gtk_window_destroy (GTK_WINDOW (self));

  return G_SOURCE_REMOVE;
}

static gboolean
panel_save_dialog_close_request (GtkWindow *window)
{
  PanelSaveDialog *self = (PanelSaveDialog *)window;

  g_assert (PANEL_IS_SAVE_DIALOG (self));

  /* Defer to idle so that we can check if we are actively saving. */
  if (self->suppress_close)
    g_idle_add_full (G_PRIORITY_HIGH,
                     panel_save_dialog_close_request_idle_cb,
                     g_object_ref (self),
                     g_object_unref);

  return TRUE;
}

static void
panel_save_dialog_dispose (GObject *object)
{
  PanelSaveDialog *self = (PanelSaveDialog *)object;

  g_clear_pointer (&self->rows, g_ptr_array_unref);
  g_clear_object (&self->cancellable);
  g_clear_object (&self->task);

  G_OBJECT_CLASS (panel_save_dialog_parent_class)->dispose (object);
}

static void
panel_save_dialog_get_property (GObject    *object,
                                guint       prop_id,
                                GValue     *value,
                                GParamSpec *pspec)
{
  PanelSaveDialog *self = PANEL_SAVE_DIALOG (object);

  switch (prop_id)
    {
    case PROP_CLOSE_AFTER_SAVE:
      g_value_set_boolean (value, panel_save_dialog_get_close_after_save (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_save_dialog_set_property (GObject      *object,
                                guint         prop_id,
                                const GValue *value,
                                GParamSpec   *pspec)
{
  PanelSaveDialog *self = PANEL_SAVE_DIALOG (object);

  switch (prop_id)
    {
    case PROP_CLOSE_AFTER_SAVE:
      panel_save_dialog_set_close_after_save (self, g_value_get_boolean (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_save_dialog_class_init (PanelSaveDialogClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);
  GtkWindowClass *window_class = GTK_WINDOW_CLASS (klass);

  object_class->dispose = panel_save_dialog_dispose;
  object_class->get_property = panel_save_dialog_get_property;
  object_class->set_property = panel_save_dialog_set_property;

  window_class->close_request = panel_save_dialog_close_request;

  /**
   * PanelSaveDialog:close-after-save:
   *
   * This property requests that the widget close after saving.
   */
  properties [PROP_CLOSE_AFTER_SAVE] =
    g_param_spec_boolean ("close-after-save", NULL, NULL,
                          FALSE,
                          (G_PARAM_READWRITE |
                           G_PARAM_EXPLICIT_NOTIFY |
                           G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_template_from_resource (widget_class, "/org/gnome/libpanel/panel-save-dialog.ui");

  gtk_widget_class_bind_template_child (widget_class, PanelSaveDialog, group);
  gtk_widget_class_bind_template_child (widget_class, PanelSaveDialog, page);

  gtk_widget_class_bind_template_callback (widget_class, panel_save_dialog_response_cancel_cb);
  gtk_widget_class_bind_template_callback (widget_class, panel_save_dialog_response_discard_cb);
  gtk_widget_class_bind_template_callback (widget_class, panel_save_dialog_response_save_cb);
}

static void
panel_save_dialog_init (PanelSaveDialog *self)
{
  self->rows = g_ptr_array_new ();
  self->suppress_close = TRUE;

  gtk_widget_init_template (GTK_WIDGET (self));
}

static void
panel_save_dialog_update (PanelSaveDialog *self)
{
  g_assert (PANEL_IS_SAVE_DIALOG (self));

  if (self->rows->len == 1)
    {
      PanelSaveDialogRow *row = g_ptr_array_index (self->rows, 0);
      PanelSaveDelegate *delegate = panel_save_dialog_row_get_delegate (row);

      panel_save_dialog_row_set_selection_mode (row, FALSE);

      if (panel_save_delegate_get_is_draft (delegate))
        {
          const char *title = panel_save_delegate_get_title (delegate);
          char *body;

          /* translators: %s is replaced with the document title */
          body = g_strdup_printf (_("The draft “%s” has not been saved. It can be saved or discarded."), title);

          adw_message_dialog_set_heading (ADW_MESSAGE_DIALOG (self),
                                          _("Save or Discard Draft?"));
          adw_message_dialog_set_body (ADW_MESSAGE_DIALOG (self), body);

          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "discard", ADW_RESPONSE_DESTRUCTIVE);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "discard", _("_Discard"));
          set_response_visible (ADW_MESSAGE_DIALOG (self), "discard", TRUE);

          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "save", ADW_RESPONSE_SUGGESTED);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "save", _("_Save As…"));
          set_response_visible (ADW_MESSAGE_DIALOG (self), "save", TRUE);

          g_free (body);
        }
      else
        {
          const char *title = panel_save_delegate_get_title (delegate);
          char *body;

          /* translators: %s is replaced with the document title */
          body = g_strdup_printf (_("“%s” contains unsaved changes. Changes can be saved or discarded."), title);

          adw_message_dialog_set_heading (ADW_MESSAGE_DIALOG (self),
                                          _("Save or Discard Changes?"));
          adw_message_dialog_set_body (ADW_MESSAGE_DIALOG (self), body);

          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "discard", ADW_RESPONSE_DESTRUCTIVE);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "discard", _("_Discard"));
          set_response_visible (ADW_MESSAGE_DIALOG (self), "discard", TRUE);

          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "save", ADW_RESPONSE_SUGGESTED);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "save", _("_Save"));
          set_response_visible (ADW_MESSAGE_DIALOG (self), "save", TRUE);

          g_free (body);
        }

      gtk_widget_hide (GTK_WIDGET (self->page));
    }
  else
    {
      gboolean has_selected = FALSE;
      gboolean has_unselected = FALSE;

      for (guint i = 0; i < self->rows->len; i++)
        {
          PanelSaveDialogRow *row = g_ptr_array_index (self->rows, i);
          gboolean selected = panel_save_dialog_row_get_selected (row);

          has_selected |= selected;
          has_unselected |= !selected;

          panel_save_dialog_row_set_selection_mode (row, TRUE);
        }

      adw_message_dialog_set_heading (ADW_MESSAGE_DIALOG (self),
                                      _("Save or Discard Changes?"));
      adw_message_dialog_set_body (ADW_MESSAGE_DIALOG (self),
                                   _("Open documents contain unsaved changes. Changes can be saved or discarded."));

      if (has_selected && has_unselected)
        {
          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "save", ADW_RESPONSE_DESTRUCTIVE);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "save", _("Only _Save Selected"));
          set_response_visible (ADW_MESSAGE_DIALOG (self), "save", TRUE);

          set_response_visible (ADW_MESSAGE_DIALOG (self), "discard", FALSE);
        }
      else if (has_selected)
        {
          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "save", ADW_RESPONSE_SUGGESTED);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "save", _("Save All"));

          set_response_visible (ADW_MESSAGE_DIALOG (self), "discard", FALSE);
        }
      else
        {
          set_response_visible (ADW_MESSAGE_DIALOG (self), "save", FALSE);

          adw_message_dialog_set_response_appearance (ADW_MESSAGE_DIALOG (self), "discard", ADW_RESPONSE_DESTRUCTIVE);
          adw_message_dialog_set_response_label (ADW_MESSAGE_DIALOG (self), "discard", _("Discard All"));
          set_response_visible (ADW_MESSAGE_DIALOG (self), "discard", TRUE);
        }

      gtk_widget_show (GTK_WIDGET (self->page));
    }
}

static void
panel_save_dialog_notify_selected_cb (PanelSaveDialog    *self,
                                      GParamSpec         *pspec,
                                      PanelSaveDialogRow *row)
{
  g_assert (PANEL_IS_SAVE_DIALOG (self));
  g_assert (PANEL_IS_SAVE_DIALOG_ROW (row));

  panel_save_dialog_update (self);
}

void
panel_save_dialog_add_delegate (PanelSaveDialog   *self,
                                PanelSaveDelegate *delegate)
{
  GtkWidget *row;

  g_return_if_fail (PANEL_IS_SAVE_DIALOG (self));
  g_return_if_fail (PANEL_IS_SAVE_DELEGATE (delegate));

  panel_save_delegate_set_progress (delegate, 0);

  row = panel_save_dialog_row_new (delegate);
  g_signal_connect_object (row,
                           "notify::selected",
                           G_CALLBACK (panel_save_dialog_notify_selected_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_ptr_array_add (self->rows, row);
  adw_preferences_group_add (self->group, row);

  panel_save_dialog_update (self);
}

static void
task_completed_cb (PanelSaveDialog *self,
                   GParamSpec      *pspec,
                   GTask           *task)
{
  g_assert (PANEL_IS_SAVE_DIALOG (self));
  g_assert (G_IS_TASK (task));

  self->saving = FALSE;
  self->discarding = FALSE;

  if (self->task == task)
    g_clear_object (&self->task);

  gtk_window_destroy (GTK_WINDOW (self));
}

void
panel_save_dialog_run_async (PanelSaveDialog     *self,
                             GCancellable        *cancellable,
                             GAsyncReadyCallback  callback,
                             gpointer             user_data)
{
  GTask *task = NULL;

  g_return_if_fail (PANEL_IS_SAVE_DIALOG (self));
  g_return_if_fail (!cancellable || G_IS_CANCELLABLE (cancellable));

  g_object_ref_sink (self);

  if (cancellable == NULL)
    self->cancellable = g_cancellable_new ();
  else
    self->cancellable = g_object_ref (cancellable);

  task = g_task_new (self, self->cancellable, callback, user_data);
  g_task_set_source_tag (task, panel_save_dialog_run_async);

  g_signal_connect_object (task,
                           "notify::completed",
                           G_CALLBACK (task_completed_cb),
                           self,
                           G_CONNECT_SWAPPED);

  if (self->rows->len == 0)
    {
      g_task_return_boolean (task, TRUE);
      g_clear_object (&task);
      return;
    }

  if (self->task)
    {
      g_task_return_new_error (task,
                               G_IO_ERROR,
                               G_IO_ERROR_INVAL,
                               "Run has already been called");
      g_clear_object (&task);
      return;
    }

  g_clear_object (&self->task);
  self->task = g_steal_pointer (&task);

  gtk_window_present (GTK_WINDOW (self));
}

gboolean
panel_save_dialog_run_finish (PanelSaveDialog  *self,
                              GAsyncResult     *result,
                              GError          **error)
{
  g_return_val_if_fail (PANEL_IS_SAVE_DIALOG (self), FALSE);
  g_return_val_if_fail (G_IS_TASK (result), FALSE);

  return g_task_propagate_boolean (G_TASK (result), error);
}

gboolean
panel_save_dialog_get_close_after_save (PanelSaveDialog *self)
{
  g_return_val_if_fail (PANEL_IS_SAVE_DIALOG (self), FALSE);

  return self->close_after_save;
}

void
panel_save_dialog_set_close_after_save (PanelSaveDialog *self,
                                        gboolean         close_after_save)
{
  g_return_if_fail (PANEL_IS_SAVE_DIALOG (self));

  close_after_save = !!close_after_save;

  if (close_after_save != self->close_after_save)
    {
      self->close_after_save = close_after_save;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_CLOSE_AFTER_SAVE]);
    }
}
