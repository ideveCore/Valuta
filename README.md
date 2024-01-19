<img heigth="128" src="data/icons/hicolor/scalable/apps/io.github.idevecore.CurrencyConverter.svg" align="left" />

# Currency Converter

A simple currency converter using Google-based data

![CurrencyConverter](data/screenshots/01.png)

## Features
- Google finance conversion provider
- European Central Bank conversion provider through the API (Frankfurter)

## Flathub
<a href='https://flathub.org/apps/io.github.idevecore.CurrencyConverter'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>

## Building

###  Requirements
- Python 3 `python` 
- PyGObject `python-gobject` 
- GTK4 `gtk4` 
- libadwaita (>= 1.2.0) `libadwaita`
- Meson `meson` 
- Ninja `ninja` 
- D-Bus `python-dbus`

### Building from Git
```bash 
 git clone --recurse-submodules https://github.com/idevecore/currency-converter.git
 cd currency-converter
 meson builddir --prefix=/usr/local 
 sudo ninja -C builddir install 
 ```

## Translations

[![Translation status](https://hosted.weblate.org/widget/currency-converter/svg-badge.svg)](https://hosted.weblate.org/engage/currency-converter/) ✨Powered by [Weblate](https://weblate.org/en/)✨

Currency Converter has been translated into the following languages:

<a href="https://hosted.weblate.org/engage/currency-converter/">
<img src="https://hosted.weblate.org/widget/currency-converter/multi-auto.svg" alt="Translation status" />
</a>

Please help translate Currency Converter into more languages through [Weblate](https://hosted.weblate.org/engage/currency-converter/).


## Donate
If you like this project and have some spare money left, consider donating:

### Ko-fi and Github Sponsors
<a href='https://ko-fi.com/idevecore'><img width='86' alt='Download on Flathub' src='https://storage.ko-fi.com/cdn/nav-logo-stroke.png'/></a>
<a href='https://github.com/sponsors/ideveCore'><img width='60' alt='Download on Flathub' src='https://github.githubassets.com/images/email/sponsors/mona.png'/></a>

## License 
 [GNU General Public License 3 or later](https://www.gnu.org/licenses/gpl-3.0.en.html)
