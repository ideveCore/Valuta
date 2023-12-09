/*
 * Copyright © 2018 Benjamin Otte
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library. If not, see <http://www.gnu.org/licenses/>.
 *
 * Authors: Benjamin Otte <otte@gnome.org>
 */

#include "config.h"

#include <gtk/gtk.h>

#include "panel-scaler-private.h"

struct _PanelScaler
{
  GObject parent_instance;

  GdkPaintable *paintable;
  double scale_factor;
};

struct _PanelScalerClass
{
  GObjectClass parent_class;
};

static void
panel_scaler_paintable_snapshot (GdkPaintable *paintable,
                                 GdkSnapshot  *snapshot,
                                 double        width,
                                 double        height)
{
  PanelScaler *self = PANEL_SCALER (paintable);

  gtk_snapshot_save (snapshot);
  gtk_snapshot_scale (snapshot, 1.0 / self->scale_factor, 1.0 / self->scale_factor);
  gdk_paintable_snapshot (self->paintable,
                          snapshot,
                          width * self->scale_factor,
                          height * self->scale_factor);

  gtk_snapshot_restore (snapshot);
}

static GdkPaintable *
panel_scaler_paintable_get_current_image (GdkPaintable *paintable)
{
  PanelScaler *self = PANEL_SCALER (paintable);
  GdkPaintable *current_paintable, *current_self;

  current_paintable = gdk_paintable_get_current_image (self->paintable);
  current_self = panel_scaler_new (current_paintable, self->scale_factor);
  g_object_unref (current_paintable);

  return current_self;
}

static GdkPaintableFlags
panel_scaler_paintable_get_flags (GdkPaintable *paintable)
{
  PanelScaler *self = PANEL_SCALER (paintable);

  return gdk_paintable_get_flags (self->paintable);
}

static int
panel_scaler_paintable_get_intrinsic_width (GdkPaintable *paintable)
{
  PanelScaler *self = PANEL_SCALER (paintable);

  return gdk_paintable_get_intrinsic_width (self->paintable) / self->scale_factor;
}

static int
panel_scaler_paintable_get_intrinsic_height (GdkPaintable *paintable)
{
  PanelScaler *self = PANEL_SCALER (paintable);

  return gdk_paintable_get_intrinsic_height (self->paintable) / self->scale_factor;
}

static double panel_scaler_paintable_get_intrinsic_aspect_ratio (GdkPaintable *paintable)
{
  PanelScaler *self = PANEL_SCALER (paintable);

  return gdk_paintable_get_intrinsic_aspect_ratio (self->paintable);
};

static void
panel_scaler_paintable_init (GdkPaintableInterface *iface)
{
  iface->snapshot = panel_scaler_paintable_snapshot;
  iface->get_current_image = panel_scaler_paintable_get_current_image;
  iface->get_flags = panel_scaler_paintable_get_flags;
  iface->get_intrinsic_width = panel_scaler_paintable_get_intrinsic_width;
  iface->get_intrinsic_height = panel_scaler_paintable_get_intrinsic_height;
  iface->get_intrinsic_aspect_ratio = panel_scaler_paintable_get_intrinsic_aspect_ratio;
}

G_DEFINE_TYPE_EXTENDED (PanelScaler, panel_scaler, G_TYPE_OBJECT, 0,
                        G_IMPLEMENT_INTERFACE (GDK_TYPE_PAINTABLE,
                                               panel_scaler_paintable_init))

static void
panel_scaler_dispose (GObject *object)
{
  PanelScaler *self = PANEL_SCALER (object);

  if (self->paintable)
    {
      const guint flags = gdk_paintable_get_flags (self->paintable);

      if ((flags & GDK_PAINTABLE_STATIC_CONTENTS) == 0)
        g_signal_handlers_disconnect_by_func (self->paintable, gdk_paintable_invalidate_contents, self);

      if ((flags & GDK_PAINTABLE_STATIC_SIZE) == 0)
        g_signal_handlers_disconnect_by_func (self->paintable, gdk_paintable_invalidate_size, self);

      g_clear_object (&self->paintable);
    }

  G_OBJECT_CLASS (panel_scaler_parent_class)->dispose (object);
}

static void
panel_scaler_class_init (PanelScalerClass *klass)
{
  GObjectClass *gobject_class = G_OBJECT_CLASS (klass);

  gobject_class->dispose = panel_scaler_dispose;
}

static void
panel_scaler_init (PanelScaler *self)
{
  self->scale_factor = 1.0;
}

GdkPaintable *
panel_scaler_new (GdkPaintable *paintable,
                  double        scale_factor)
{
  PanelScaler *self;
  guint flags;

  g_return_val_if_fail (GDK_IS_PAINTABLE (paintable), NULL);
  g_return_val_if_fail (scale_factor > 0.0, NULL);

  self = g_object_new (PANEL_TYPE_SCALER, NULL);

  self->paintable = g_object_ref (paintable);
  flags = gdk_paintable_get_flags (paintable);

  if ((flags & GDK_PAINTABLE_STATIC_CONTENTS) == 0)
    g_signal_connect_swapped (paintable, "invalidate-contents", G_CALLBACK (gdk_paintable_invalidate_contents), self);

  if ((flags & GDK_PAINTABLE_STATIC_SIZE) == 0)
    g_signal_connect_swapped (paintable, "invalidate-size", G_CALLBACK (gdk_paintable_invalidate_size), self);

  self->scale_factor = scale_factor;

  return GDK_PAINTABLE (self);
}
