pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'currencyconverter')
gnome = import('gnome')

define = configuration_data()

define.set('APPID', application_id)
define.set('PROFILE', profile)
define.set('PYTHON', python.find_installation('python3').full_path())

configure_file(
  input: 'define.in',
  output: 'define.py',
  configuration: define,
  install: true,
  install_dir: moduledir
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'currencyconverter.in',
  output: 'currencyconverter',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

currencyconverter_sources = [
  '__init__.py',
  'api.py',
  'main.py',
  'window.py',
]

install_data(currencyconverter_sources, install_dir: moduledir)
