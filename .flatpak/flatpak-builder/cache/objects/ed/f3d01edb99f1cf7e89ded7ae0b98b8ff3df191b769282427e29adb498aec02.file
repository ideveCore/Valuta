/* panel-frame-header.c
 *
 * Copyright 2021 Christian Hergert <chergert@redhat.com>
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

#include "panel-frame.h"
#include "panel-frame-header.h"
#include "panel-widget.h"

/**
 * PanelFrameHeader:
 *
 * An interface implemented by the header of a #PanelFrame.
 */
G_DEFINE_INTERFACE (PanelFrameHeader, panel_frame_header, GTK_TYPE_WIDGET)

static void
panel_frame_header_default_init (PanelFrameHeaderInterface *iface)
{
  /**
   * PanelFrameHeader:frame:
   *
   * The frame the header is attached to, or %NULL.
   */
  g_object_interface_install_property (iface,
                                       g_param_spec_object ("frame",
                                                            "Frame",
                                                            "Frame",
                                                            PANEL_TYPE_FRAME,
                                                            (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS)));
}

/**
 * panel_frame_header_set_frame:
 * @self: a #PanelFrameHeader
 * @frame: (transfer none) (nullable): a #PanelFrame or %NULL
 *
 * Sets the frame the header is attached to.
 */
void
panel_frame_header_set_frame (PanelFrameHeader *self,
                              PanelFrame       *frame)
{
  g_return_if_fail (PANEL_IS_FRAME_HEADER (self));
  g_return_if_fail (!frame || PANEL_IS_FRAME (frame));

  gtk_widget_add_css_class (GTK_WIDGET (self), "frameheader");

  g_object_set (self, "frame", frame, NULL);
}

/**
 * panel_frame_header_get_frame:
 * @self: a #PanelFrameHeader
 *
 * Gets the frame the header is attached to.
 *
 * Returns: (transfer none) (nullable): a #PanelFrame or %NULL
 */
PanelFrame *
panel_frame_header_get_frame (PanelFrameHeader *self)
{
  PanelFrame *frame = NULL;

  g_return_val_if_fail (PANEL_IS_FRAME_HEADER (self), NULL);

  g_object_get (self, "frame", &frame, NULL);

  /* We return a borrowed reference */
  g_return_val_if_fail (!frame || PANEL_IS_FRAME (frame), NULL);
  g_return_val_if_fail (!frame || G_OBJECT (frame)->ref_count > 1, NULL);
  g_object_unref (frame);

  return frame;
}

/**
 * panel_frame_header_can_drop:
 * @self: a #PanelFrameHeader
 * @widget: (transfer none): a #PanelWidget
 *
 * Tells if the panel widget can be drop onto the panel frame.
 *
 * Returns: whether the widget can be dropped.
 */
gboolean
panel_frame_header_can_drop (PanelFrameHeader *self,
                             PanelWidget      *widget)
{
  g_return_val_if_fail (PANEL_IS_FRAME_HEADER (self), FALSE);
  g_return_val_if_fail (PANEL_IS_WIDGET (widget), FALSE);

  if (PANEL_FRAME_HEADER_GET_IFACE (self)->can_drop)
    return PANEL_FRAME_HEADER_GET_IFACE (self)->can_drop (self, widget);

  return FALSE;
}

/**
 * panel_frame_header_page_changed:
 * @self: a #PanelFrameHeader
 * @widget: (nullable): a #PanelWidget or %NULL if no page is visible
 *
 * Notifies the header that the visible page has changed.
 */
void
panel_frame_header_page_changed (PanelFrameHeader *self,
                                 PanelWidget      *widget)
{
  g_return_if_fail (PANEL_IS_FRAME_HEADER (self));
  g_return_if_fail (!widget || PANEL_IS_WIDGET (widget));

  if (PANEL_FRAME_HEADER_GET_IFACE (self)->page_changed)
    PANEL_FRAME_HEADER_GET_IFACE (self)->page_changed (self, widget);
}

/**
 * panel_frame_header_add_prefix:
 * @self: a #PanelFrameHeader
 * @priority: the priority
 * @child: a #GtkWidget
 *
 * Add a widget into a the prefix area with a priority. The highest
 * the priority the closest to the start.
 */
void
panel_frame_header_add_prefix (PanelFrameHeader *self,
                               int               priority,
                               GtkWidget        *child)
{
  g_return_if_fail (PANEL_IS_FRAME_HEADER (self));
  g_return_if_fail (GTK_IS_WIDGET (child));

  PANEL_FRAME_HEADER_GET_IFACE (self)->add_prefix (self, priority, child);
}

/**
 * panel_frame_header_add_suffix:
 * @self: a #PanelFrameHeader
 * @priority: the priority
 * @child: a #GtkWidget
 *
 * Add a widget into a the suffix area with a priority. The highest
 * the priority the closest to the start.
 */
void
panel_frame_header_add_suffix (PanelFrameHeader *self,
                               int               priority,
                               GtkWidget        *child)
{
  g_return_if_fail (PANEL_IS_FRAME_HEADER (self));
  g_return_if_fail (GTK_IS_WIDGET (child));

  PANEL_FRAME_HEADER_GET_IFACE (self)->add_suffix (self, priority, child);
}
