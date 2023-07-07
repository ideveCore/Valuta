from gi.repository import Gio, GObject
from currencyconverter.define import APP_ID

class Settings(Gio.Settings):
    __gsignals__ = {
        'provider-changed': (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, (str, str))
    }

    instance = None

    def __init__(self, *args):
        super().__init__(*args)

    @staticmethod
    def new():
        """Create a new instance of Settings."""
        g_settings = Settings(APP_ID)
        return g_settings

    @staticmethod
    def get():
        if Settings.instance is None:
            Settings.instance = Settings.new()
            print(Settings.instance.get_strv('src-currencies'))
        return Settings.instance

    @property
    def src_currencies(self):
        return Settings.instance.get_strv('src-currencies')

    @src_currencies.setter
    def src_currencies(self, src_currencies):
        print(src_currencies)
        # self.get_converter_settings().set_strv('src-currencies', src_currencies)

    def get_converter_settings(self, converter=None):
        print(converter)
