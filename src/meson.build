python = import('python')

# ===== Generate Currency Convert bin ===== 
configure_file(
  input: 'valuta.in',
  output: 'valuta',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

# ===== Generate define module
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

# ===== Blueprint compiler =====
blueprints = custom_target('blueprints',
  input: files(
    'components/currency_selector/index.blp',
    'components/currency_selector_row/index.blp',
    'components/shortcuts/shortcuts.blp',
    'pages/convertion/index.blp',
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

# ===== Compile Currence Converter gresource =====
gnome.compile_resources('valuta',
  'valuta.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# ===== Python sources =====
sources = [
  '__init__.py',
  'about.py',
  'actions.py',
  'requests.py',
  'utils.py',
  'main.py',
  'application.py',
  'window.py',
]

# ===== Install python sources =====
install_data(sources, install_dir: moduledir)

# ===== Install components sources =====
install_subdir('components', install_dir: moduledir)

# ===== Install page sources =====
install_subdir('pages', install_dir: moduledir)

# ===== Install assets sources =====
install_subdir('assets', install_dir: moduledir)

# ===== Install provider =====
subdir('search_provider')

# ===== Install icons =====
subdir('assets/icons')
