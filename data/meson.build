pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'ui/window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('currencyconverter',
  'currencyconverter.gresource.xml',
  dependencies: blueprints,
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

desktop_conf = configuration_data()
desktop_conf.set('ICON', application_id)
desktop_file = i18n.merge_file(
  input: configure_file(
    input: files('io.github.idevecore.CurrencyConverter.desktop.in.in'),
    output: 'io.github.idevecore.CurrencyConverter.desktop.in',
    configuration: desktop_conf
  ),
  output: '@0@.desktop'.format(application_id),
  po_dir: join_paths(meson.project_source_root(), 'po'),
  type: 'desktop',  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'io.github.idevecore.CurrencyConverter.appdata.xml.in',
       output: 'io.github.idevecore.CurrencyConverter.appdata.xml',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', appstream_file])
endif

install_data('io.github.idevecore.CurrencyConverter.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

subdir('icons')
