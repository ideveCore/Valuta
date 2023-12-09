/* panel-drop-controls.c
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

#include "panel-dock-private.h"
#include "panel-drop-controls-private.h"
#include "panel-enums.h"
#include "panel-frame-header.h"
#include "panel-frame-private.h"
#include "panel-frame-switcher-private.h"
#include "panel-grid-private.h"
#include "panel-grid-column-private.h"
#include "panel-paned.h"
#include "panel-resizer-private.h"
#include "panel-widget.h"

struct _PanelDropControls
{
  GtkWidget          parent_instance;

  GtkWidget         *child;

  GtkButton         *bottom;
  GtkButton         *center;
  GtkButton         *left;
  GtkButton         *right;
  GtkButton         *top;

  GtkDropTarget     *bottom_target;
  GtkDropTarget     *center_target;
  GtkDropTarget     *left_target;
  GtkDropTarget     *right_target;
  GtkDropTarget     *top_target;
  GtkDropTarget     *drop_target;

  PanelDock         *dock;
  AdwTabPage        *drop_before_page;

  PanelArea          area : 4;

  guint              in_drop : 1;
};

G_DEFINE_TYPE (PanelDropControls, panel_drop_controls, GTK_TYPE_WIDGET)

enum {
  PROP_0,
  PROP_AREA,
  N_PROPS
};

static GParamSpec *properties [N_PROPS];

GtkWidget *
panel_drop_controls_new (void)
{
  return g_object_new (PANEL_TYPE_DROP_CONTROLS, NULL);
}

static void
panel_drop_controls_drop_finished (PanelDropControls *self,
                                   gboolean           success)
{
  GtkWidget *frame;

  g_assert (PANEL_IS_DROP_CONTROLS (self));

  self->drop_before_page = NULL;
  self->in_drop = FALSE;

  if ((frame = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME)))
    _panel_frame_set_drop_before (PANEL_FRAME (frame), NULL);
}

void
panel_drop_controls_set_area (PanelDropControls *self,
                              PanelArea          area)
{
  g_return_if_fail (PANEL_IS_DROP_CONTROLS (self));
  g_return_if_fail (area <= PANEL_AREA_CENTER);

  self->area = area;

  switch (self->area)
    {
    case PANEL_AREA_START:
    case PANEL_AREA_END:
      gtk_widget_show (GTK_WIDGET (self->top));
      gtk_widget_show (GTK_WIDGET (self->bottom));
      gtk_widget_show (GTK_WIDGET (self->center));
      gtk_widget_hide (GTK_WIDGET (self->left));
      gtk_widget_hide (GTK_WIDGET (self->right));
      break;

    case PANEL_AREA_TOP:
    case PANEL_AREA_BOTTOM:
      gtk_widget_hide (GTK_WIDGET (self->top));
      gtk_widget_hide (GTK_WIDGET (self->bottom));
      gtk_widget_show (GTK_WIDGET (self->center));
      gtk_widget_show (GTK_WIDGET (self->left));
      gtk_widget_show (GTK_WIDGET (self->right));
      break;

    case PANEL_AREA_CENTER:
      gtk_widget_show (GTK_WIDGET (self->center));
      gtk_widget_show (GTK_WIDGET (self->top));
      gtk_widget_show (GTK_WIDGET (self->bottom));
      gtk_widget_show (GTK_WIDGET (self->left));
      gtk_widget_show (GTK_WIDGET (self->right));
      break;

    default:
      g_assert_not_reached ();
    }
}

PanelArea
panel_drop_controls_get_area (PanelDropControls *self)
{
  g_return_val_if_fail (PANEL_IS_DROP_CONTROLS (self), 0);

  return self->area;
}

static gboolean
drop_target_accept_cb (PanelDropControls *self,
                       GdkDrop           *drop,
                       GtkDropTarget     *drop_target)
{
  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GDK_IS_DROP (drop));
  g_assert (GTK_IS_DROP_TARGET (drop_target));

  return TRUE;
}

static void
on_drop_target_notify_value_cb (PanelDropControls *self,
                                GParamSpec        *pspec,
                                GtkDropTarget     *drop_target)
{
  PanelFrameHeader *header;
  const GValue *value;
  PanelWidget *panel;
  GtkWidget *frame;

  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GTK_IS_DROP_TARGET (drop_target));

  if (!(value = gtk_drop_target_get_value (drop_target)) ||
      !G_VALUE_HOLDS (value, PANEL_TYPE_WIDGET) ||
      !(panel = g_value_get_object (value)) ||
      !(frame = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME)) ||
      !(header = panel_frame_get_header (PANEL_FRAME (frame))))
    return;

  /* TODO: Actually handle this based on area */

  if (!panel_widget_get_reorderable (panel) ||
      (!panel_frame_header_can_drop (header, panel)))
    gtk_drop_target_reject (drop_target);
}

static GdkDragAction
on_drop_target_motion_cb (PanelDropControls *self,
                          double             x,
                          double             y,
                          GtkDropTarget     *drop_target)
{
  PanelFrameHeader *header;
  GtkOrientation orientation;
  AdwTabPage *drop_before = NULL;
  GtkWidget *pick;
  GtkWidget *frame;
  double header_x, header_y;

  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GTK_IS_DROP_TARGET (drop_target));

  frame = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME);
  header = panel_frame_get_header (PANEL_FRAME (frame));

  if (PANEL_IS_FRAME_SWITCHER (header))
    {
      orientation = gtk_orientable_get_orientation (GTK_ORIENTABLE (header));

      gtk_widget_translate_coordinates (GTK_WIDGET (self),
                                        GTK_WIDGET (header),
                                        x, y, &header_x, &header_y);
      if (gtk_widget_contains (GTK_WIDGET (header), header_x, header_y))
        {
          for (pick = gtk_widget_pick (GTK_WIDGET (header), header_x, header_y, GTK_PICK_DEFAULT);
               pick != NULL && pick != GTK_WIDGET (header);
               pick = gtk_widget_get_parent (pick))
            {
              if (GTK_IS_TOGGLE_BUTTON (pick))
                {
                  GtkAllocation alloc;
                  double pick_x, pick_y;

                  /* If the drop spot is >= ⅔ through the widget, assume they want it after this widget */
                  gtk_widget_translate_coordinates (GTK_WIDGET (self), pick, x, y, &pick_x, &pick_y);
                  gtk_widget_get_allocation (pick, &alloc);
                  if ((orientation == GTK_ORIENTATION_HORIZONTAL && pick_x > (alloc.width * 2 / 3)) ||
                      (orientation == GTK_ORIENTATION_VERTICAL && pick_y > (alloc.height * 2 / 3)))
                    pick = gtk_widget_get_next_sibling (pick);

                  if (pick != NULL)
                    drop_before = _panel_frame_switcher_get_page (PANEL_FRAME_SWITCHER (header), pick);

                  break;
                }
            }
        }
    }

  self->drop_before_page = drop_before;
  _panel_frame_set_drop_before (PANEL_FRAME (frame),
                                drop_before ? PANEL_WIDGET (adw_tab_page_get_child (drop_before))
                                            : NULL);

  return GDK_ACTION_MOVE;
}

static void
on_drop_target_leave_cb (PanelDropControls *self,
                         GtkDropTarget     *drop_target)
{
  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GTK_IS_DROP_TARGET (drop_target));

  panel_drop_controls_drop_finished (self, FALSE);
}

static GdkDragAction
on_drop_target_enter_cb (PanelDropControls *self,
                         double             x,
                         double             y,
                         GtkDropTarget     *drop_target)
{
  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GTK_IS_DROP_TARGET (drop_target));

  self->in_drop = TRUE;
  self->drop_before_page= NULL;

  gtk_widget_queue_allocate (GTK_WIDGET (self));

  return GDK_ACTION_MOVE;
}

static GtkWidget *
get_prev_frame (PanelFrame *frame)
{
  GtkWidget *resizer;

  g_assert (PANEL_IS_FRAME (frame));

  resizer = gtk_widget_get_ancestor (GTK_WIDGET (frame), PANEL_TYPE_RESIZER);
  resizer = gtk_widget_get_prev_sibling (resizer);

  if (resizer != NULL)
    return panel_resizer_get_child (PANEL_RESIZER (resizer));

  return NULL;
}

static GtkWidget *
create_frame (PanelDropControls *self,
              PanelFrame        *target)
{
  PanelPosition *position = panel_frame_get_position (target);
  PanelDock *dock = PANEL_DOCK (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_DOCK));
  GtkWidget *frame;

  if (dock != NULL)
    frame = GTK_WIDGET (_panel_dock_create_frame (dock, position));
  else
    frame = panel_frame_new ();

  g_clear_object (&position);

  return frame;
}

static gboolean
on_drop_target_drop_cb (PanelDropControls *self,
                        const GValue      *value,
                        double             x,
                        double             y,
                        GtkDropTarget     *drop_target)
{
  PanelArea area;
  GtkOrientation orientation;
  PanelFrameHeader *header;
  PanelWidget *before_panel = NULL;
  PanelFrame *target;
  PanelGrid *grid;
  GtkWidget *paned;
  GtkWidget *src_paned;
  PanelWidget *panel;
  GtkWidget *frame;
  GtkWidget *button;
  gboolean success = FALSE;
  guint column;
  guint row;

  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GTK_IS_DROP_TARGET (drop_target));

  if (self->drop_before_page != NULL)
    before_panel = PANEL_WIDGET (adw_tab_page_get_child (self->drop_before_page));

  target = PANEL_FRAME (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_FRAME));

  if (!G_VALUE_HOLDS (value, PANEL_TYPE_WIDGET) ||
      !(panel = g_value_get_object (value)) ||
      !(frame = gtk_widget_get_ancestor (GTK_WIDGET (panel), PANEL_TYPE_FRAME)) ||
      !panel_widget_get_reorderable (panel) ||
      !(header = panel_frame_get_header (PANEL_FRAME (target))) ||
      !panel_frame_header_can_drop (header, panel) ||
      !(src_paned = gtk_widget_get_ancestor (GTK_WIDGET (panel), PANEL_TYPE_PANED)) ||
      !(paned = gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_PANED)))
    goto cleanup;

  g_assert (PANEL_IS_WIDGET (panel));
  g_assert (PANEL_IS_FRAME_HEADER (header));
  g_assert (PANEL_IS_PANED (src_paned));
  g_assert (PANEL_IS_PANED (paned));
  g_assert (panel_frame_header_can_drop (header, panel));

  button = gtk_event_controller_get_widget (GTK_EVENT_CONTROLLER (drop_target));
  area = GPOINTER_TO_INT (g_object_get_data (G_OBJECT (button), "AREA"));
  grid = PANEL_GRID (gtk_widget_get_ancestor (GTK_WIDGET (self), PANEL_TYPE_GRID));
  orientation = gtk_orientable_get_orientation (GTK_ORIENTABLE (target));

  switch (area)
    {
    case PANEL_AREA_CENTER:
      /* Do Nothing */
      break;

    case PANEL_AREA_START:
      if (grid != NULL)
        {
          PanelGridColumn *grid_column;

          _panel_grid_get_position (grid, GTK_WIDGET (target), &column, &row);
          _panel_grid_insert_column (grid, column);

          grid_column = panel_grid_get_column (grid, column);
          target = panel_grid_column_get_most_recent_frame (grid_column);
        }
      else
        {
          GtkWidget *new_frame;

          new_frame = create_frame (self, target);
          gtk_orientable_set_orientation (GTK_ORIENTABLE (new_frame), orientation);
          panel_paned_insert_after (PANEL_PANED (paned),
                                    new_frame,
                                    get_prev_frame (target));
          target = PANEL_FRAME (new_frame);
        }
      break;

    case PANEL_AREA_END:
      if (grid != NULL)
        {
          PanelGridColumn *grid_column;

          _panel_grid_get_position (grid, GTK_WIDGET (target), &column, &row);
          _panel_grid_insert_column (grid, ++column);

          grid_column = panel_grid_get_column (grid, column);
          target = panel_grid_column_get_most_recent_frame (grid_column);
        }
      else
        {
          GtkWidget *new_frame;

          new_frame = create_frame (self, target);
          gtk_orientable_set_orientation (GTK_ORIENTABLE (new_frame), orientation);
          panel_paned_insert_after (PANEL_PANED (paned), new_frame, GTK_WIDGET (target));
          target = PANEL_FRAME (new_frame);
        }
      break;

    case PANEL_AREA_TOP:
      if (grid != NULL)
        {
          PanelGridColumn *grid_column;

          _panel_grid_get_position (grid, GTK_WIDGET (target), &column, &row);
          grid_column = panel_grid_get_column (grid, column);

          if (row == 0)
            {
              _panel_grid_column_prepend_frame (PANEL_GRID_COLUMN (grid_column));
              row++;
            }

          target = panel_grid_column_get_row (grid_column, row - 1);
        }
      else
        {
          GtkWidget *new_frame;

          new_frame = create_frame (self, target);
          gtk_orientable_set_orientation (GTK_ORIENTABLE (new_frame), orientation);
          panel_paned_insert_after (PANEL_PANED (paned),
                                    new_frame,
                                    get_prev_frame (target));
          target = PANEL_FRAME (new_frame);
        }
      break;

    case PANEL_AREA_BOTTOM:
      if (grid != NULL)
        {
          PanelGridColumn *grid_column;

          _panel_grid_get_position (grid, GTK_WIDGET (target), &column, &row);
          grid_column = panel_grid_get_column (grid, column);
          target = panel_grid_column_get_row (grid_column, row + 1);
        }
      else
        {
          GtkWidget *new_frame;

          new_frame = create_frame (self, target);
          gtk_orientable_set_orientation (GTK_ORIENTABLE (new_frame), orientation);
          panel_paned_insert_after (PANEL_PANED (paned), new_frame, GTK_WIDGET (target));
          target = PANEL_FRAME (new_frame);
        }
      break;

    default:
      g_assert_not_reached ();
    }

  /* Ignore the No-Op case */
  if (frame == GTK_WIDGET (target) && before_panel == panel)
    goto cleanup;

  g_object_ref (panel);

  panel_frame_remove (PANEL_FRAME (frame), panel);
  panel_frame_add_before (target, panel, before_panel);
  panel_frame_set_visible_child (target, panel);

  /* If we failed to locate a grid, we need to cleanup and remove any
   * empty frame we left behind as we're in an edge panel.
   */
  if (grid == NULL &&
      panel_frame_get_empty (PANEL_FRAME (frame)) &&
      panel_paned_get_n_children (PANEL_PANED (src_paned)) > 1)
    panel_paned_remove (PANEL_PANED (src_paned), frame);

  g_object_unref (panel);

  success = TRUE;

cleanup:
  panel_drop_controls_drop_finished (self, success);

  return success;
}

static void
setup_drop_target (PanelDropControls  *self,
                   GtkWidget          *widget,
                   GtkDropTarget     **targetptr,
                   PanelArea           area)
{
  GType types[] = { PANEL_TYPE_WIDGET };

  g_assert (PANEL_IS_DROP_CONTROLS (self));
  g_assert (GTK_IS_WIDGET (widget));

  g_object_set_data (G_OBJECT (widget),
                     "AREA",
                     GINT_TO_POINTER (area));

  *targetptr = gtk_drop_target_new (G_TYPE_INVALID, GDK_ACTION_COPY | GDK_ACTION_MOVE);
  gtk_drop_target_set_gtypes (*targetptr, types, G_N_ELEMENTS (types));
  gtk_drop_target_set_preload (*targetptr, TRUE);
  g_signal_connect_object (*targetptr,
                           "accept",
                           G_CALLBACK (drop_target_accept_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (*targetptr,
                           "notify::value",
                           G_CALLBACK (on_drop_target_notify_value_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (*targetptr,
                           "motion",
                           G_CALLBACK (on_drop_target_motion_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (*targetptr,
                           "drop",
                           G_CALLBACK (on_drop_target_drop_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (*targetptr,
                           "leave",
                           G_CALLBACK (on_drop_target_leave_cb),
                           self,
                           G_CONNECT_SWAPPED);
  g_signal_connect_object (*targetptr,
                           "enter",
                           G_CALLBACK (on_drop_target_enter_cb),
                           self,
                           G_CONNECT_SWAPPED);
  gtk_widget_add_controller (GTK_WIDGET (widget),
                             GTK_EVENT_CONTROLLER (*targetptr));
}

static void
panel_drop_controls_root (GtkWidget *widget)
{
  PanelDropControls *self = (PanelDropControls *)widget;
  GtkWidget *dock;

  g_assert (PANEL_IS_DROP_CONTROLS (self));

  if (!(dock = gtk_widget_get_ancestor (widget, PANEL_TYPE_DOCK)))
    {
      g_warning ("%s added without a dock, this cannot work.",
                 G_OBJECT_TYPE_NAME (self));
      return;
    }

  self->dock = PANEL_DOCK (dock);
}

static void
panel_drop_controls_unroot (GtkWidget *widget)
{
  PanelDropControls *self = (PanelDropControls *)widget;

  g_assert (PANEL_IS_DROP_CONTROLS (self));

  self->dock = NULL;
}

static void
panel_drop_controls_dispose (GObject *object)
{
  PanelDropControls *self = (PanelDropControls *)object;

  g_clear_pointer (&self->child, gtk_widget_unparent);

  G_OBJECT_CLASS (panel_drop_controls_parent_class)->dispose (object);
}

static void
panel_drop_controls_get_property (GObject    *object,
                                  guint       prop_id,
                                  GValue     *value,
                                  GParamSpec *pspec)
{
  PanelDropControls *self = PANEL_DROP_CONTROLS (object);

  switch (prop_id)
    {
    case PROP_AREA:
      g_value_set_enum (value, panel_drop_controls_get_area (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_drop_controls_set_property (GObject      *object,
                                  guint         prop_id,
                                  const GValue *value,
                                  GParamSpec   *pspec)
{
  PanelDropControls *self = PANEL_DROP_CONTROLS (object);

  switch (prop_id)
    {
    case PROP_AREA:
      panel_drop_controls_set_area (self, g_value_get_enum (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_drop_controls_class_init (PanelDropControlsClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);
  GtkWidgetClass *widget_class = GTK_WIDGET_CLASS (klass);

  object_class->dispose = panel_drop_controls_dispose;
  object_class->get_property = panel_drop_controls_get_property;
  object_class->set_property = panel_drop_controls_set_property;

  widget_class->root = panel_drop_controls_root;
  widget_class->unroot = panel_drop_controls_unroot;

  properties [PROP_AREA] =
    g_param_spec_enum ("area", NULL, NULL,
                       PANEL_TYPE_AREA,
                       PANEL_AREA_CENTER,
                       (G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);

  gtk_widget_class_set_layout_manager_type (widget_class, GTK_TYPE_BIN_LAYOUT);
  gtk_widget_class_set_template_from_resource (widget_class, "/org/gnome/libpanel/panel-drop-controls.ui");
  gtk_widget_class_set_css_name (widget_class, "paneldropcontrols");

  gtk_widget_class_bind_template_child (widget_class, PanelDropControls, child);
  gtk_widget_class_bind_template_child (widget_class, PanelDropControls, left);
  gtk_widget_class_bind_template_child (widget_class, PanelDropControls, right);
  gtk_widget_class_bind_template_child (widget_class, PanelDropControls, top);
  gtk_widget_class_bind_template_child (widget_class, PanelDropControls, bottom);
  gtk_widget_class_bind_template_child (widget_class, PanelDropControls, center);
}

static void
panel_drop_controls_init (PanelDropControls *self)
{
  gtk_widget_init_template (GTK_WIDGET (self));

  setup_drop_target (self, GTK_WIDGET (self->bottom), &self->bottom_target, PANEL_AREA_BOTTOM);
  setup_drop_target (self, GTK_WIDGET (self->center), &self->center_target, PANEL_AREA_CENTER);
  setup_drop_target (self, GTK_WIDGET (self->left), &self->left_target, PANEL_AREA_START);
  setup_drop_target (self, GTK_WIDGET (self->right), &self->right_target, PANEL_AREA_END);
  setup_drop_target (self, GTK_WIDGET (self->top), &self->top_target, PANEL_AREA_TOP);
  setup_drop_target (self, GTK_WIDGET (self), &self->drop_target, PANEL_AREA_CENTER);
}

gboolean
panel_drop_controls_in_drop (PanelDropControls *self)
{
  g_return_val_if_fail (PANEL_IS_DROP_CONTROLS (self), FALSE);

  return self->in_drop;
}
