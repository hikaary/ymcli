# Maintainer: hikaary <hikary.local@gmail.com>
pkgname=ymcli-git
_pkgname=ymcli
pkgver=0.0.1
pkgrel=1
provides=("$_pkgname")
conflicts=("$_pkgname")
pkgdesc="CLI player for yandex music"
url="https://github.com/hikaary/ymcli"
arch=("any")
license=("MIT")
depends=("python" "vlc")
source=("git+https://github.com/hikaary/$_pkgname.git")
md5sums=("SKIP")

pkgver()
{
  cd "$_pkgname"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

package()
{
  cd "$_pkgname"
  python setup.py install --root="$pkgdir"
}
