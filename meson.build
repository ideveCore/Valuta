project('valuta',
          version: '1.3.2',
    meson_version: '>= 0.64.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

python = import('python')
i18n = import('i18n')

prefix = get_option('prefix')
base_id = 'io.github.idevecore.Valuta'
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'valuta')
datadir = prefix / get_option('datadir')

if get_option('profile') == 'development'
  profile = 'Devel'
  vcs_tag = run_command('git', 'rev-parse', '--short', 'HEAD').stdout().strip()
  if vcs_tag == ''
    version_suffix = '-devel'
  else
    version_suffix = '-@0@'.format(vcs_tag)
  endif
  application_id = '@0@.@1@'.format(base_id, profile)
  object_path = '/io/github/idevecore/Valuta/Devel/SearchProvider'
else
  profile = ''
  version_suffix = ''
  application_id = base_id
  object_path = '/io/github/idevecore/Valuta/SearchProvider'
endif

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('PROFILE', profile)
conf.set('VERSION', meson.project_version() + version_suffix)
conf.set('APP_ID', application_id)
conf.set('BIN', join_paths(get_option('prefix'), get_option('bindir'), meson.project_name()))
conf.set('object_path', object_path)
conf.set('pkgdatadir', pkgdatadir)
conf.set('datadir', get_option('datadir'))
conf.set('prefix', get_option('prefix'))
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))

message('Looking for dependencies')
py_installation = python.find_installation('python3')
if not py_installation.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif

dependency('glib-2.0')
dependency('gobject-introspection-1.0', version: '>= 1.35.0')
dependency('gstreamer-1.0', version: '>= 1.18')
dependency('gtk4', version: '>= 4.6')
dependency('libadwaita-1', version: '>= 1.0')
dependency('libsoup-3.0')
dependency('pygobject-3.0', version: '>= 3.40')

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
  gtk_update_icon_cache: true,
  glib_compile_schemas: true,
  update_desktop_database: true,
)
