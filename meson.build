project('currencyconverter',
          version: '0.1.0',
    meson_version: '>= 0.62.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
python = import('python')
gnome = import('gnome')

base_id = 'io.github.idevecore.CurrencyConverter'
package_url = 'https://github.com/fkinoshita/Telegraph'

# Profiles
if get_option('profile') == 'development'
    profile = 'Devel'
    application_id = '@0@.@1@'.format(base_id, profile)

    find_program('git')
    rev_txt = run_command('git', 'rev-parse', '--short', 'HEAD').stdout().strip()
    version = meson.project_version() + '-' + rev_txt
else
    application_id = base_id
    profile = 'Default'
    version = meson.project_version()
endif

subdir('data')
subdir('src')
subdir('po')

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
