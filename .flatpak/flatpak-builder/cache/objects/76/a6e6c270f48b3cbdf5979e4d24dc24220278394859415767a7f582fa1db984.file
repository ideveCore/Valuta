/* panel-version-macros.h
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

#pragma once

#include <glib.h>

#include "panel-version.h"

#ifndef _PANEL_EXTERN
# define _PANEL_EXTERN extern
#endif

#ifdef PANEL_DISABLE_DEPRECATION_WARNINGS
# define PANEL_DEPRECATED _PANEL_EXTERN
# define PANEL_DEPRECATED_FOR(f) _PANEL_EXTERN
# define PANEL_UNAVAILABLE(maj,min) _PANEL_EXTERN
#else
# define PANEL_DEPRECATED G_DEPRECATED _PANEL_EXTERN
# define PANEL_DEPRECATED_FOR(f) G_DEPRECATED_FOR(f) _PANEL_EXTERN
# define PANEL_UNAVAILABLE(maj,min) G_UNAVAILABLE(maj,min) _PANEL_EXTERN
#endif

#define PANEL_VERSION_1_0 (G_ENCODE_VERSION (1, 0))
#define PANEL_VERSION_1_2 (G_ENCODE_VERSION (1, 2))
#define PANEL_VERSION_1_4 (G_ENCODE_VERSION (1, 4))

#if (PANEL_MINOR_VERSION == 99)
# define PANEL_VERSION_CUR_STABLE (G_ENCODE_VERSION (PANEL_MAJOR_VERSION + 1, 0))
#elif (PANEL_MINOR_VERSION % 2)
# define PANEL_VERSION_CUR_STABLE (G_ENCODE_VERSION (PANEL_MAJOR_VERSION, PANEL_MINOR_VERSION + 1))
#else
# define PANEL_VERSION_CUR_STABLE (G_ENCODE_VERSION (PANEL_MAJOR_VERSION, PANEL_MINOR_VERSION))
#endif

#if (PANEL_MINOR_VERSION == 99)
# define PANEL_VERSION_PREV_STABLE (G_ENCODE_VERSION (PANEL_MAJOR_VERSION + 1, 0))
#elif (PANEL_MINOR_VERSION % 2)
# define PANEL_VERSION_PREV_STABLE (G_ENCODE_VERSION (PANEL_MAJOR_VERSION, PANEL_MINOR_VERSION - 1))
#else
# define PANEL_VERSION_PREV_STABLE (G_ENCODE_VERSION (PANEL_MAJOR_VERSION, PANEL_MINOR_VERSION - 2))
#endif

/**
 * PANEL_VERSION_MIN_REQUIRED:
 *
 * A macro that should be defined by the user prior to including
 * the libpanel.h header.
 *
 * The definition should be one of the predefined Drafting version
 * macros: %PANEL_VERSION_1_0, ...
 *
 * This macro defines the lower bound for the Drafting API to use.
 *
 * If a function has been deprecated in a newer version of Drafting,
 * it is possible to use this symbol to avoid the compiler warnings
 * without disabling warning for every deprecated function.
 */
#ifndef PANEL_VERSION_MIN_REQUIRED
# define PANEL_VERSION_MIN_REQUIRED (PANEL_VERSION_CUR_STABLE)
#endif

/**
 * PANEL_VERSION_MAX_ALLOWED:
 *
 * A macro that should be defined by the user prior to including
 * the libpanel.h header.

 * The definition should be one of the predefined Drafting version
 * macros: %PANEL_VERSION_1_0, %PANEL_VERSION_1_2,...
 *
 * This macro defines the upper bound for the Drafting API to use.
 *
 * If a function has been introduced in a newer version of Drafting,
 * it is possible to use this symbol to get compiler warnings when
 * trying to use that function.
 */
#ifndef PANEL_VERSION_MAX_ALLOWED
# if PANEL_VERSION_MIN_REQUIRED > PANEL_VERSION_PREV_STABLE
#  define PANEL_VERSION_MAX_ALLOWED (PANEL_VERSION_MIN_REQUIRED)
# else
#  define PANEL_VERSION_MAX_ALLOWED (PANEL_VERSION_CUR_STABLE)
# endif
#endif

#if PANEL_VERSION_MAX_ALLOWED < PANEL_VERSION_MIN_REQUIRED
#error "PANEL_VERSION_MAX_ALLOWED must be >= PANEL_VERSION_MIN_REQUIRED"
#endif
#if PANEL_VERSION_MIN_REQUIRED < PANEL_VERSION_1_0
#error "PANEL_VERSION_MIN_REQUIRED must be >= PANEL_VERSION_1_0"
#endif

#define PANEL_AVAILABLE_IN_ALL                  _PANEL_EXTERN

#if PANEL_VERSION_MIN_REQUIRED >= PANEL_VERSION_1_0
# define PANEL_DEPRECATED_IN_1_0                PANEL_DEPRECATED
# define PANEL_DEPRECATED_IN_1_0_FOR(f)         PANEL_DEPRECATED_FOR(f)
#else
# define PANEL_DEPRECATED_IN_1_0                _PANEL_EXTERN
# define PANEL_DEPRECATED_IN_1_0_FOR(f)         _PANEL_EXTERN
#endif
#if PANEL_VERSION_MAX_ALLOWED < PANEL_VERSION_1_0
# define PANEL_AVAILABLE_IN_1_0                 PANEL_UNAVAILABLE(1, 0)
#else
# define PANEL_AVAILABLE_IN_1_0                 _PANEL_EXTERN
#endif

#if PANEL_VERSION_MIN_REQUIRED >= PANEL_VERSION_1_2
# define PANEL_DEPRECATED_IN_1_2                PANEL_DEPRECATED
# define PANEL_DEPRECATED_IN_1_2_FOR(f)         PANEL_DEPRECATED_FOR(f)
#else
# define PANEL_DEPRECATED_IN_1_2                _PANEL_EXTERN
# define PANEL_DEPRECATED_IN_1_2_FOR(f)         _PANEL_EXTERN
#endif
#if PANEL_VERSION_MAX_ALLOWED < PANEL_VERSION_1_2
# define PANEL_AVAILABLE_IN_1_2                 PANEL_UNAVAILABLE(1, 2)
#else
# define PANEL_AVAILABLE_IN_1_2                 _PANEL_EXTERN
#endif

#if PANEL_VERSION_MIN_REQUIRED >= PANEL_VERSION_1_4
# define PANEL_DEPRECATED_IN_1_4                PANEL_DEPRECATED
# define PANEL_DEPRECATED_IN_1_4_FOR(f)         PANEL_DEPRECATED_FOR(f)
#else
# define PANEL_DEPRECATED_IN_1_4                _PANEL_EXTERN
# define PANEL_DEPRECATED_IN_1_4_FOR(f)         _PANEL_EXTERN
#endif
#if PANEL_VERSION_MAX_ALLOWED < PANEL_VERSION_1_4
# define PANEL_AVAILABLE_IN_1_4                 PANEL_UNAVAILABLE(1, 4)
#else
# define PANEL_AVAILABLE_IN_1_4                 _PANEL_EXTERN
#endif

PANEL_AVAILABLE_IN_1_2
guint    panel_get_major_version (void);
PANEL_AVAILABLE_IN_1_2
guint    panel_get_minor_version (void);
PANEL_AVAILABLE_IN_1_2
guint    panel_get_micro_version (void);
PANEL_AVAILABLE_IN_1_2
gboolean panel_check_version     (guint major,
                                  guint minor,
                                  guint micro);
