<img heigth="128" src="data/icons/hicolor/scalable/apps/io.github.idevecore.Valuta.svg" align="left" />

# Valuta

Convert currencies with ease. Valuta provides an intuitive and fast experience for your conversion needs.

![Valuta](data/screenshots/01.png)

## Features
- European Central Bank conversion provider through the API (Frankfurter)
- Google finance conversion provider

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

[![Translation status](https://hosted.weblate.org/widget/valuta/svg-badge.svg)](https://hosted.weblate.org/engage/valuta/) ✨Powered by [Weblate](https://weblate.org/en/)✨

Valuta has been translated into the following languages:

<a href="https://hosted.weblate.org/engage/valuta/">
<img src="https://hosted.weblate.org/widget/valuta/multi-auto.svg" alt="Translation status" />
</a>

Please help translate Valuta into more languages through [Weblate](https://hosted.weblate.org/engage/valuta/).


## Donate
If you like this project and have some spare money left, consider donating:

### Ko-fi and Github Sponsors
<a href='https://ko-fi.com/idevecore'><img width='86' alt='Download on Flathub' src='https://storage.ko-fi.com/cdn/nav-logo-stroke.png'/></a>
<a href='https://github.com/sponsors/ideveCore'><img width='60' alt='Download on Flathub' src='https://github.githubassets.com/images/email/sponsors/mona.png'/></a>

## License 
 [GNU General Public License 3 or later](https://www.gnu.org/licenses/gpl-3.0.en.html)
