<img heigth="128" src="data/icons/hicolor/scalable/apps/io.github.idevecore.Valuta.svg" align="left" />

# Valuta

Convert currencies with ease. Valuta provides an intuitive and fast experience for your conversion needs.

![Valuta](data/screenshots/01.png)

## Providers
- [European Central Bank conversion provider through the API (Frankfurter).](https://www.frankfurter.app/)
- [Google finance conversion provider.](https://google.com)
- [Moeda.info conversion provider.](https://moeda.info/)

## Features
- Gnome search provider integration: example "10" or "10 USD to EUR".

## Flathub
<a href='https://flathub.org/apps/io.github.idevecore.Valuta'><img width='240' alt='Download on Flathub' src='https://flathub.org/assets/badges/flathub-badge-en.png'/></a>

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
 git clone --recurse-submodules https://github.com/idevecore/valuta.git
 cd valuta
 meson builddir --prefix=/usr/local 
 sudo ninja -C builddir install
 ```

## Translations

[![Status da tradução](https://hosted.weblate.org/widget/currency-converter/svg-badge.svg)](https://hosted.weblate.org/engage/currency-converter/)

Valuta has been translated into the following languages:

<a href="https://hosted.weblate.org/engage/currency-converter/">
<img src="https://hosted.weblate.org/widget/currency-converter/multi-auto.svg" alt="Translation status" />
</a>

Please help translate Valuta into more languages through [Weblate](https://hosted.weblate.org/engage/currency-converter/).


## Donate
If you like this project and have some spare money left, consider donating:

### Github Sponsors
<a href='https://github.com/sponsors/ideveCore'><img width='60' alt='Download on Flathub' src='https://github.githubassets.com/images/email/sponsors/mona.png'/></a>

## Code of Conduct
The project follows the [GNOME Code of Conduct](https://conduct.gnome.org/).

## License 
 [GNU General Public License 3 or later](https://www.gnu.org/licenses/gpl-3.0.en.html)
