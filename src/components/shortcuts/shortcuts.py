
from gi.repository import Gtk

@Gtk.Template(resource_path='/io/github/idevecore/CurrencyConverter/components/shortcuts/shortcuts.ui')
class CurrencyConverterShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'CurrencyConverterShortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
