Summary:	A C++ BitTorrent library
Summary(pl.UTF-8):	Biblioteka BitTorrenta napisana w C++
Name:		rb_libtorrent
Version:	0.13
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libtorrent/libtorrent-%{version}.tar.gz
# Source0-md5:	571a91a98c7426321681dd9f767a87de
URL:		http://www.rasterbar.com/products/libtorrent/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	libstdc++-devel
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
rb_libtorrent is a C++ library that aims to be a good alternative to
all the other BitTorrent implementations around. It is a library and
not a full featured client, although it comes with a working example
client.

Its main goals are to be very efficient (in terms of CPU and memory
usage) as well as being very easy to use both as a user and developer.

%description -l pl.UTF-8
rb_libtorrent jest biblioteką napisaną w C++ która aspiruje do bycia
dobrą alternatywą dla wszystkich innych implementacji BitTorrenta.
Jest to biblioteka a nie pełnoprawny klient, jakkolwiek pakiet
zawiera działającego przykładowego klienta.

Główne cele biblioteki to bycie bardzo efektywną (w rozumieniu
wykorzystania procesora i pamięci) jak również łatwą w użyciu
zarówno dla użytkownika, jak i programisty.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
License:	BSD, zlib/libpng License, Boost Software License
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	boost-devel
Requires:	openssl-devel
## Same pkgconfig file, and unsuffixed shared library symlink.:(
Conflicts:	libtorrent-devel

%description    devel
The rb_libtorrent-devel package contains libraries and header files
for developing applications that use rb_libtorrent.

The various source and header files included in this package are
licensed under the revised BSD, zlib/libpng, and Boost Public
licenses.

%description devel -l pl.UTF-8
Pakiet rb_libtorrent-devel zawiera biblioteki i nagłówki do rozwijania
aplikacji używających rb_libtorrent.

Różne pliki źródłowe i nagłówki dostarcozne z tym pakietem są
licencjonowane pod zmienioną licencją BSD, zlib/libpng i Boost
Public.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static rb_libtorrent library.

%description static -l pl.UTF-8
Statyczna biblioteka rb_libtorrent.

%prep
%setup -q -n "libtorrent-%{version}"
## Some of the sources and docs are executable, which makes rpmlint against
## the resulting -debuginfo and -devel packages, respectively, quite angry. :]
find src docs -type f | xargs chmod a-x
find -type f -regex '.*\.[hc]pp' | xargs chmod a-x
## The RST files are the sources used to create the final HTML files; and are
## not needed.
rm -f docs/*.rst
## Fix the installed pkgconfig file: we don't need linkage that the
## libtorrent DSO already takes care of.
%{__sed} -i -e 's/^Libs:.*$/Libs: -L${libdir} -ltorrent/' libtorrent.pc.in

%build
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--enable-examples \
	--with-zlib=system

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
## Ensure that we preserve our timestamps properly.
#export CPPROG="%{__cp} -p"
#make install DESTDIR=$RPM_BUILD_ROOT INSTALL="%{__install} -c -p"
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

## Do the renaming due to the somewhat limited %{_bindir} namespace.
rename client torrent_client $RPM_BUILD_ROOT%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README
%attr(755,root,root) %{_bindir}/*torrent*
#%%attr(755,root,root) %{_libdir}/libtorrent.so.*.*.*
%attr(755,root,root) %{_libdir}/libtorrent-0.13.so

%files devel
%defattr(644,root,root,755)
%doc docs/
%attr(755,root,root) %{_libdir}/libtorrent.so
%{_libdir}/libtorrent.la
%{_pkgconfigdir}/libtorrent.pc
%{_includedir}/libtorrent

%files static
%defattr(644,root,root,755)
%{_libdir}/libtorrent.a
