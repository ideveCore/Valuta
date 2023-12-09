/* panel-position.c
 *
 * Copyright 2022 Christian Hergert <chergert@redhat.com>
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

#include "panel-dock.h"
#include "panel-enums.h"
#include "panel-position.h"

/**
 * PanelPosition:
 *
 * Specifies a position in the dock. You receive a #PanelPosition in the
 * handler to [signal@PanelDock::create-frame].
 */
struct _PanelPosition
{
  GObject parent_instance;

  guint column;
  guint depth;
  guint row;

  PanelArea area : 4;
  guint area_set : 1;
  guint column_set : 1;
  guint depth_set : 1;
  guint row_set : 1;
};

enum {
  PROP_0,
  PROP_AREA,
  PROP_AREA_SET,
  PROP_COLUMN,
  PROP_COLUMN_SET,
  PROP_DEPTH,
  PROP_DEPTH_SET,
  PROP_ROW,
  PROP_ROW_SET,
  N_PROPS
};

G_DEFINE_FINAL_TYPE (PanelPosition, panel_position, G_TYPE_OBJECT)

static GParamSpec *properties [N_PROPS];

static void
panel_position_get_property (GObject    *object,
                             guint       prop_id,
                             GValue     *value,
                             GParamSpec *pspec)
{
  PanelPosition *self = PANEL_POSITION (object);

  switch (prop_id)
    {
    case PROP_AREA:
      g_value_set_enum (value, panel_position_get_area (self));
      break;

    case PROP_AREA_SET:
      g_value_set_boolean (value, panel_position_get_area_set (self));
      break;

    case PROP_COLUMN:
      g_value_set_uint (value, panel_position_get_column (self));
      break;

    case PROP_COLUMN_SET:
      g_value_set_boolean (value, panel_position_get_column_set (self));
      break;

    case PROP_DEPTH:
      g_value_set_uint (value, panel_position_get_depth (self));
      break;

    case PROP_DEPTH_SET:
      g_value_set_boolean (value, panel_position_get_depth_set (self));
      break;

    case PROP_ROW:
      g_value_set_uint (value, panel_position_get_row (self));
      break;

    case PROP_ROW_SET:
      g_value_set_boolean (value, panel_position_get_row_set (self));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_position_set_property (GObject      *object,
                             guint         prop_id,
                             const GValue *value,
                             GParamSpec   *pspec)
{
  PanelPosition *self = PANEL_POSITION (object);

  switch (prop_id)
    {
    case PROP_AREA:
      panel_position_set_area (self, g_value_get_enum (value));
      break;

    case PROP_AREA_SET:
      panel_position_set_area_set (self, g_value_get_boolean (value));
      break;

    case PROP_COLUMN:
      panel_position_set_column (self, g_value_get_uint (value));
      break;

    case PROP_COLUMN_SET:
      panel_position_set_column_set (self, g_value_get_boolean (value));
      break;

    case PROP_DEPTH:
      panel_position_set_depth (self, g_value_get_uint (value));
      break;

    case PROP_DEPTH_SET:
      panel_position_set_depth_set (self, g_value_get_boolean (value));
      break;

    case PROP_ROW:
      panel_position_set_row (self, g_value_get_uint (value));
      break;

    case PROP_ROW_SET:
      panel_position_set_row_set (self, g_value_get_boolean (value));
      break;

    default:
      G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
    }
}

static void
panel_position_class_init (PanelPositionClass *klass)
{
  GObjectClass *object_class = G_OBJECT_CLASS (klass);

  object_class->get_property = panel_position_get_property;
  object_class->set_property = panel_position_set_property;

  /**
   * PanelPosition:area
   *
   * The area.
   */
  properties[PROP_AREA] =
    g_param_spec_enum ("area", NULL, NULL,
                       PANEL_TYPE_AREA,
                       PANEL_AREA_CENTER,
                       (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelPosition:area-set
   *
   * The area is set.
   */
  properties[PROP_AREA_SET] =
    g_param_spec_boolean ("area-set", NULL, NULL,
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelPosition:column
   *
   * The column in the position.
   */
  properties[PROP_COLUMN] =
    g_param_spec_uint ("column", NULL, NULL,
                       0, G_MAXUINT, 0,
                       (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  /**
   * PanelPosition:column-set
   *
   * The column is set.
   */
  properties[PROP_COLUMN_SET] =
    g_param_spec_boolean ("column-set", NULL, NULL,
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties[PROP_DEPTH] =
    g_param_spec_uint ("depth", NULL, NULL,
                       0, G_MAXUINT, 0,
                       (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties[PROP_DEPTH_SET] =
    g_param_spec_boolean ("depth-set", NULL, NULL,
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties[PROP_ROW] =
    g_param_spec_uint ("row", NULL, NULL,
                       0, G_MAXUINT, 0,
                       (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  properties[PROP_ROW_SET] =
    g_param_spec_boolean ("row-set", NULL, NULL,
                          FALSE,
                          (G_PARAM_READWRITE | G_PARAM_EXPLICIT_NOTIFY | G_PARAM_STATIC_STRINGS));

  g_object_class_install_properties (object_class, N_PROPS, properties);
}

static void
panel_position_init (PanelPosition *self)
{
  self->area = PANEL_AREA_CENTER;
}

/**
 * panel_position_new:
 *
 * Create a position.
 *
 * Returns: (transfer full): a newly created instance of #PanelPosition.
 */
PanelPosition *
panel_position_new (void)
{
  return g_object_new (PANEL_TYPE_POSITION, NULL);
}

#define SET_MEMBER(member, value, prop)                                    \
  G_STMT_START {                                                           \
    gboolean notify_set = self->member##_set == FALSE;                     \
    gboolean notify = self->member != value;                               \
    self->member = value;                                                  \
    self->member##_set = TRUE;                                             \
    if (notify)                                                            \
      g_object_notify_by_pspec (G_OBJECT (self), properties [prop]);       \
    if (notify_set)                                                        \
      g_object_notify_by_pspec (G_OBJECT (self), properties [prop##_SET]); \
  } G_STMT_END
#define SET_MEMBER_SET(member, value, prop)                                \
  G_STMT_START {                                                           \
    value = !!value;                                                       \
    if (value != self->member)                                             \
      {                                                                    \
        self->member = value;                                              \
        g_object_notify_by_pspec (G_OBJECT (self), properties [prop]);     \
      }                                                                    \
  } G_STMT_END

/**
 * panel_position_get_area:
 * @self: a #PanelPosition
 *
 * Gets the area.
 *
 * Returns: the area.
 */
PanelArea
panel_position_get_area (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), 0);

  return self->area;
}

/**
 * panel_position_set_area:
 * @self: a #PanelPosition
 * @area: the #PanelArea
 *
 * Sets the area.
 */
void
panel_position_set_area (PanelPosition *self,
                         PanelArea      area)
{
  g_return_if_fail (PANEL_IS_POSITION (self));
  g_return_if_fail (area <= PANEL_AREA_CENTER);

  SET_MEMBER (area, area, PROP_AREA);
}

/**
 * panel_position_get_area_set:
 * @self: a #PanelPosition
 *
 * Gets wether the area is set.
 *
 * Returns: the wether the area is set.
 */
gboolean
panel_position_get_area_set (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), FALSE);

  return self->area_set;
}

/**
 * panel_position_set_area_set:
 * @self: a #PanelPosition
 * @area_set: whether the area is set.
 *
 * Sets whether the area is set.
 */
void
panel_position_set_area_set (PanelPosition *self,
                             gboolean       area_set)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER_SET (area_set, area_set, PROP_AREA_SET);
}

guint
panel_position_get_column (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), 0);

  return self->column;
}

void
panel_position_set_column (PanelPosition *self,
                           guint          column)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER (column, column, PROP_COLUMN);
}

gboolean
panel_position_get_column_set (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), FALSE);

  return self->column_set;
}

void
panel_position_set_column_set (PanelPosition *self,
                               gboolean       column_set)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER_SET (column_set, column_set, PROP_COLUMN_SET);
}

guint
panel_position_get_depth (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), 0);

  return self->depth;
}

void
panel_position_set_depth (PanelPosition *self,
                          guint          depth)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER (depth, depth, PROP_DEPTH);
}

gboolean
panel_position_get_depth_set (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), FALSE);

  return self->depth_set;
}

void
panel_position_set_depth_set (PanelPosition *self,
                              gboolean       depth_set)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER_SET (depth_set, depth_set, PROP_DEPTH_SET);
}

guint
panel_position_get_row (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), 0);

  return self->row;
}

void
panel_position_set_row (PanelPosition *self,
                        guint          row)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER (row, row, PROP_ROW);
}

gboolean
panel_position_get_row_set (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), FALSE);

  return self->row_set;
}

void
panel_position_set_row_set (PanelPosition *self,
                            gboolean       row_set)
{
  g_return_if_fail (PANEL_IS_POSITION (self));

  SET_MEMBER_SET (row_set, row_set, PROP_ROW_SET);
}

/**
 * panel_position_is_indeterminate:
 * @self: a #PanelPosition
 *
 * Tells is the position is indeterminate.
 *
 * Returns: whether the position is indeterminate.
 */
gboolean
panel_position_is_indeterminate (PanelPosition *self)
{
  g_return_val_if_fail (PANEL_IS_POSITION (self), FALSE);

  return !self->area_set || !self->column_set || !self->row_set;
}

/**
 * panel_position_to_variant:
 * @self: a #PanelPosition
 *
 * Convert a #PanelPosition to a #GVariant.
 *
 * Returns: (transfer full) (nullable): the new #GVariant containing
 * the positon values
 */
GVariant *
panel_position_to_variant (PanelPosition *self)
{
  GVariantDict dict;

  g_return_val_if_fail (PANEL_IS_POSITION (self), NULL);

  g_variant_dict_init (&dict, NULL);

  if (self->area_set)
    {
      const char *area;

      switch (self->area)
        {
        case PANEL_AREA_START:
          area = "start";
          break;

        case PANEL_AREA_END:
          area = "end";
          break;

        case PANEL_AREA_TOP:
          area = "top";
          break;

        case PANEL_AREA_BOTTOM:
          area = "bottom";
          break;

        case PANEL_AREA_CENTER:
          area = "center";
          break;

        default:
          g_assert_not_reached ();
        }

      g_variant_dict_insert (&dict, "area", "s", area);
    }

  if (self->column_set)
    g_variant_dict_insert (&dict, "column", "u", self->column);

  if (self->depth_set)
    g_variant_dict_insert (&dict, "depth", "u", self->depth);

  if (self->row_set)
    g_variant_dict_insert (&dict, "row", "u", self->row);

  return g_variant_dict_end (&dict);
}

/**
 * panel_position_new_from_variant:
 * @variant: a #GVariant
 *
 * Create a #PanelPosition from a #GVariant.
 *
 * Returns: (transfer full) (nullable): A newly created #PanelPosition
 *   from the #GVariant.
 */
PanelPosition *
panel_position_new_from_variant (GVariant *variant)
{

  PanelPosition *self;
  const char *area;

  g_return_val_if_fail (variant, NULL);

  self = g_object_new (PANEL_TYPE_POSITION, NULL);

  if (g_variant_lookup (variant, "area", "&s", &area))
    {
      if (area[0] == 't')
        self->area = PANEL_AREA_TOP;
      else if (area[0] == 'e')
        self->area = PANEL_AREA_END;
      else if (area[0] == 'b')
        self->area = PANEL_AREA_BOTTOM;
      else if (area[0] == 's')
        self->area = PANEL_AREA_START;
      else if (area[0] == 'c')
        self->area = PANEL_AREA_CENTER;

      self->area_set = TRUE;
    }

  self->column_set = g_variant_lookup (variant, "column", "u", &self->column);
  self->depth_set = g_variant_lookup (variant, "depth", "u", &self->depth);
  self->row_set = g_variant_lookup (variant, "row", "u", &self->row);

  return self;
}

/**
 * panel_position_equal:
 * @a: a #PanelPosition
 * @b: another #PanelPosition
 *
 * Compares two #PanelPosition.
 *
 * Returns: whether the two pane positions are equal.
 */
gboolean
panel_position_equal (PanelPosition *a,
                      PanelPosition *b)
{
  return a->area_set == b->area_set &&
         a->column_set == b->column_set &&
         a->row_set == b->row_set &&
         a->depth_set == b->depth_set &&
         (!a->area_set || a->area == b->area) &&
         (!a->column_set || a->column == b->column) &&
         (!a->row_set || a->row == b->row) &&
         (!a->depth_set || a->depth == b->depth);
}
