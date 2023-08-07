python = import('python')

configure_file(
  input: 'currencyconverter.in',
  output: 'currencyconverter',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

configure_file(
  input: 'define.in',
  output: 'define.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

launcher = join_paths(meson.project_build_root(), 'src', meson.project_name())
run_target('run',
  command: [launcher]
)

subdir('search_provider')

currencyconverter_sources = [
  '__init__.py',
  'api.py',
  'main.py',
  'window.py',
  'components/currency_selector.py',
  'components/preferences.py',
]

install_data(currencyconverter_sources, install_dir: moduledir)
install_subdir('components', install_dir: moduledir)
