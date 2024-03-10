# ===== Install application icon ===== 
scalable_dir = join_paths('hicolor', 'scalable', 'apps')
install_data(
  join_paths(scalable_dir, ('@0@.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
)

# ===== Install application symbolic icon ===== 
symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, 'io.github.idevecore.Valuta-symbolic.svg'),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
)
