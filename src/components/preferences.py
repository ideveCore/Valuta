from gi.repository import Adw, Gtk, Gio
from currencyconverter.define import APP_ID

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/ui/components/preferences.ui')
class CurrencyConverterPreferences(Adw.PreferencesWindow):
    __gtype_name__ = 'CurrencyConverterPreferences'

    select_theme = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = Gtk.Application.get_default();
        self.settings = Gio.Settings.new(APP_ID);
        self.select_theme.connect('notify::selected-item', self._select_theme)
        self.load_theme_data();
        self.set_transient_for(self.app.props.active_window)

    def _select_theme(self, _sender, _e):
        self._change_theme(self.select_theme.get_selected())

    def _change_theme(self, _selected_item):
        if _selected_item == 0:
            self.settings.set_string('theme', 'light')
        elif _selected_item == 1:
            self.settings.set_string('theme', 'dark')
        else:
            self.settings.set_string('theme', 'default')
        self.app.load_theme()
        

    def load_theme_data(self):
        if self.settings.get_string('theme') == 'default':
            self.select_theme.set_selected(2)
        elif self.settings.get_string('theme') == 'dark':
            self.select_theme.set_selected(1)
        else:
            self.select_theme.set_selected(0)

