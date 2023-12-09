/* panel-progress-icon.c
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

#include "config.h"

#include "panel-progress-icon-private.h"

struct _PanelProgressIcon
{
  GtkDrawingArea parent_instance;
  double         progress;
};

G_DEFINE_FINAL_TYPE (PanelProgressIcon, panel_progress_icon, GTK_TYPE_DRAWING_AREA)

enum {
  PROP_0,
  PROP_PROGRESS,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

static void
panel_progress_icon_draw (GtkDrawingArea *area,
                          cairo_t        *cr,
                          int             width,
                          int             height,
                          gpointer        user_data)
{
  PanelProgressIcon *self = (PanelProgressIcon *)area;
  GtkStyleContext *style_context;
  GdkRGBA rgba;
  double alpha;

  g_assert (PANEL_IS_PROGRESS_ICON (self));
  g_assert (cr != NULL);

  style_context = gtk_widget_get_style_context (GTK_WIDGET (area));
  gtk_style_context_get_color (style_context, &rgba);

  alpha = rgba.alpha;
  rgba.alpha = 0.15;
  gdk_cairo_set_source_rgba (cr, &rgba);

  cairo_arc (cr, width/2, height/2, width/2, .0, 2*G_PI);
  cairo_fill (cr);

  if (self->progress > .0)
    {
      rgba.alpha = alpha;
      gdk_cairo_set_source_rgba (cr, &rgba);

      cairo_arc (cr, width/2, height/2, width/2, (-.5*G_PI), (self->progress*2*G_PI) - (.5*G_PI));

      if (self->progress != 1.0)
        {
          cairo_line_to (cr, width/2, height/2);
          cairo_line_to (cr, width/2, 0);
        }

      cairo_fill (cr);
    }
}

static void
panel_progress_icon_get_property (GObject    *object,
                                  guint       prop_id,
                                  GValue     *value,
                                  GParamSpec *pspec)
{
  PanelProgressIcon *self = PANEL_PROGRESS_ICON (object);

  switch (prop_id)
    {
    case PROP_PROGRESS:
      g_value_set_double (value, panel_progress_icon_get_progress (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_progress_icon_set_property (GObject      *object,
                                  guint         prop_id,
                                  const GValue *value,
                                  GParamSpec   *pspec)
{
  PanelProgressIcon *self = PANEL_PROGRESS_ICON (object);

  switch (prop_id)
    {
    case PROP_PROGRESS:
      panel_progress_icon_set_progress (self, g_value_get_double (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_progress_icon_class_init (PanelProgressIconClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->get_property = panel_progress_icon_get_property;
  object_class->set_property = panel_progress_icon_set_property;

  properties [PROP_PROGRESS] =
    g_param_spec_double ("progress", NULL, NULL,
                         0.0, 1.0, 0.0,
                         (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_css_name (widget_class, "panelprogressicon");
}

static void
panel_progress_icon_init (PanelProgressIcon *icon)
{
  gtk_widget_set_size_request (GTK_WIDGET (icon), 16, 16);
  gtk_widget_set_valign (GTK_WIDGET (icon), GTK_ALIGN_CENTER);
  gtk_widget_set_halign (GTK_WIDGET (icon), GTK_ALIGN_CENTER);

  gtk_drawing_area_set_draw_func (GTK_DRAWING_AREA (icon),
                                  panel_progress_icon_draw,
                                  NULL, NULL);
}

GtkWidget *
panel_progress_icon_new (void)
{
  return g_object_new (PANEL_TYPE_PROGRESS_ICON, NULL);
}

double
panel_progress_icon_get_progress (PanelProgressIcon *self)
{
  g_return_val_if_fail (PANEL_IS_PROGRESS_ICON (self), 0.0);

  return self->progress;
}

void
panel_progress_icon_set_progress (PanelProgressIcon *self,
                                  double          progress)
{
  g_return_if_fail (PANEL_IS_PROGRESS_ICON (self));

  progress = CLAMP (progress, 0.0, 1.0);

  if (self->progress != progress)
    {
      self->progress = progress;
      g_object_notify_by_pspec (G_OBJECT (self), properties [PROP_PROGRESS]);
      gtk_widget_queue_draw (GTK_WIDGET (self));
    }
}
