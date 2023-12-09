/* panel-util-private.h
 *
 * Copyright 2023 Christian Hergert <chergert@redhat.com>
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

#pragma once

#include <glib.h>

G_BEGIN_DECLS

#define panel_str_empty0(str)       (!(str) || !*(str))
#define panel_str_equal(str1,str2)  (strcmp((char*)str1,(char*)str2)==0)
#define panel_str_equal0(str1,str2) (g_strcmp0((char*)str1,(char*)str2)==0)
#define panel_strv_empty0(strv)     (((strv) == NULL) || ((strv)[0] == NULL))

static inline gboolean
panel_set_strv (char               ***dest,
                const char * const   *src)
{
  if ((const char * const *)*dest == src)
    return FALSE;

  if (*dest == NULL ||
      src == NULL ||
      !g_strv_equal ((const char * const *)*dest, src))
    {
      char **copy = g_strdupv ((char **)src);
      g_strfreev (*dest);
      *dest = copy;
      return TRUE;
    }

  return FALSE;
}

static inline gboolean
panel_set_str (char       **str_pointer,
               const char  *new_str)
{
#if GLIB_CHECK_VERSION(2, 75, 0) && !defined(GLIB_VERSION_MAX_ALLOWED)
  return g_set_str (str_pointer, new_str);
#else
  char *copy;

  if (*str_pointer == new_str ||
      (*str_pointer && new_str && strcmp (*str_pointer, new_str) == 0))
    return FALSE;

  copy = g_strdup (new_str);
  g_free (*str_pointer);
  *str_pointer = copy;

  return TRUE;
#endif
}

G_END_DECLS
