python = import('python')

# ===== Generate Currency Convert bin ===== 
configure_file(
  input: 'currencyconverter.in',
  output: 'currencyconverter',
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
    'components/currency_selector_row/currency_selector_row.blp',
    'components/currency_selector/currency_selector.blp',
    # ==================================================
    # ====== This component temporarily is unused ======
    #'components/preferences/preferences.blp',
    # ==================================================
    'components/shortcuts/shortcuts.blp',
    'components/theme_switcher/theme_switcher.blp',
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

# ===== Compile Currence Converter gresource =====
gnome.compile_resources('currencyconverter',
  'currencyconverter.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# ===== Python sources =====
sources = [
  '__init__.py',
  './components/currency_selector/currency_selector.py',
  # ==================================================
  # ====== This component temporarily is unused ======
  # './components/preferences/preferences.py',
  # ==================================================
  'components/theme_switcher/theme_switcher.py',
  'utils.py',
  'main.py',
  'window.py',
]

# ===== Install python sources =====
install_data(sources, install_dir: moduledir)

# ===== Install components sources =====
install_subdir('components', install_dir: moduledir)

# ===== Install assets sources =====
install_subdir('assets', install_dir: moduledir)

# ===== Install provider =====
subdir('search_provider')
