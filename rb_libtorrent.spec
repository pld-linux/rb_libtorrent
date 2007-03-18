Summary:	A C++ BitTorrent library
Summary(pl.UTF-8):	Biblioteka BitTorrenata napisana w C++
Name:		rb_libtorrent
Version:	0.11
Release:	0.1
License:	BSD
Group:		Libraries
Source0:	http://dl.sourceforge.net/libtorrent/libtorrent-%{version}.tar.gz
# Source0-md5:	56e9071b95a6e3f9377121f2fead3499
URL:		http://www.rasterbar.com/products/libtorrent/
BuildRequires:	boost-array-devel
BuildRequires:	boost-bind-devel
BuildRequires:	boost-call_traits-devel
BuildRequires:	boost-date_time-devel
BuildRequires:	boost-devel >= 0.33.1
BuildRequires:	boost-filesystem-devel
BuildRequires:	boost-thread-devel
BuildRequires:	libstdc++-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{name} is a C++ library that aims to be a good alternative to all the
other BitTorrent implementations around. It is a library and not a
full featured client, although it comes with a working example client.

Its main goals are to be very efficient (in terms of CPU and memory
usage) as well as being very easy to use both as a user and developer.

%description -l pl.UTF-8
%{name} jest biblioteką napisaną w C++ która aspiruje do bycia
dobrą alternatywą dla wszystkich innych implementacji BitTorrenta.
Jest to biblioteka a nie pełnoprawny klient, jakkolwiek paczka
zawiera działającego przykładowego klienta.

Głównymi celami biblioteki jest być bardzo efektywną (w rozumieniu
efektywnośći CPU i wykorzystania pamięci) jak również bycie
łatwą w użyciu zarówno dla użytkownika, jak i programisty.

%package        devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
License:	BSD, zlib/libpng License, Boost Software License
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
## Same pkgconfig file, and unsuffixed shared library symlink.:(
Conflicts:	libtorrent-devel
## Needed for various headers retrieved via #include directives...
Requires:	boost-devel
Requires:	openssl-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

The various source and header files included in this package are
licensed under the revised BSD, zlib/libpng, and Boost Public
licenses.

%description devel -l pl.UTF-8
Paczka %{name}-devel zawiera biblioteki i nagłówki do rozwijania
aplikacji używających %{name}.

Różne pliki źródłowe i nagłówki dostarcozne z tym pakietem są
licencjonowane pod zeminioną licencją BSD, zlib/libpng i Boost
Public.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	boost-static
Requires:	openssl-static

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q -n "libtorrent-%{version}"
## Some of the sources and docs are executable, which makes rpmlint against
## the resulting -debuginfo and -devel packages, respectively, quite angry. :]
find src/ docs/ -type f -exec chmod a-x '{}' \;
find . -type f -regex '.*\.[hc]pp' -exec chmod a-x '{}' \;
## The RST files are the sources used to create the final HTML files; and are
## not needed.
rm -f docs/*.rst
## Fix the installed pkgconfig file: we don't need linkage that the
## libtorrent DSO already takes care of.
sed -i -e 's/^Libs:.*$/Libs: -L${libdir} -ltorrent/' libtorrent.pc.in

%build
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
## Do the renaming due to the somewhat limited %%{_bindir} namespace.
rename client torrent_client $RPM_BUILD_ROOT%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README
%attr(755,roor,root) %{_bindir}/*torrent*
%attr(755,root,root) %{_libdir}/libtorrent.so.*

%files devel
%defattr(644,root,root,755)
%doc docs/
%{_pkgconfigdir}/libtorrent.pc
%dir %{_includedir}/libtorrent
%{_includedir}/libtorrent/
%{_libdir}/libtorrent.so
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
