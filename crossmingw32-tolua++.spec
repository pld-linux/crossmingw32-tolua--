%define		realname	tolua++
Summary:	Extended version of tolua, a tool to integrate C/C++ code with Lua - MinGW32 cross version
Summary(pl.UTF-8):	Rozszerzona wersja tolua, narzędzia integrującego kod C/C++ z Lua - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.0.4
Release:	4
License:	Free
Group:		Development/Tools
Source0:	http://www.codenix.com/~tolua/%{realname}-%{version}.tar.bz2
# Source0-md5:	8785100f7c9d9253cb47b530d97a32f6
URL:		http://www.codenix.com/~tolua/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-lua50 >= 5.0
BuildRequires:	crossmingw32-w32api
BuildRequires:	scons
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}

%define		_ssp_cflags		%{nil}
%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

%description
tolua++ is an extension of tolua, a tool to integrate C/C++ code with
Lua. tolua++ includes new features oriented to c++, such as class
templates.

tolua is a tool that greatly simplifies the integration of C/C++ code
with Lua. Based on a "cleaned" header file, tolua automatically
generates the binding code to access C/C++ features from Lua. Using
Lua-5.0 API and tag method facilities, the current version
automatically maps C/C++ constants, external variables, functions,
namespace, classes, and methods to Lua. It also provides facilities to
create Lua modules.

%description -l pl.UTF-8
tolua++ jest rozszerzeniem tolua, narzędzia integrującego kod C/C++ z
Lua. tolua++ zawiera nowe, zorientowane na c++ cechy takie jak wzorce
klas.

tolua jest narzędziem które znacznie upraszcza integracje kodu C/C++ z
Lua. Bazując na "oczyszczonych" plikach nagłówkowych tolua
automatycznie generuje kod umożliwiający Lua dostęp do struktur i
funkcji C/C++. Dzięki użyciu API Lua 5.0, bieżąca wersja automatycznie
mapuje stałe, zewnętrzne zmienne, funkcje, przestrzenie nazw, klasy i
metody z C/C++ do Lua. Umożliwia również tworzenie modułów Lua.

%package static
Summary:	Static tolua++ library - cross MinGW32 version
Summary(pl.UTF-8):	Statyczna biblioteka tolua++ - wersja skrośna MinGW32
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static tolua++ library - cross MinGW32 version.

%description static -l pl.UTF-8
Statyczna biblioteka tolua++ - wersja skrośna MinGW32.

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl.UTF-8):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-lua50-dll >= 5.0

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
AR=%{target}-ar ; export AR
RANLIB=%{target}-ranlib ; export RANLIB

for i in src/lib/tolua_{event,is,map,push,to}.c
do %{__cc} %{rpmcflags} $i -c -I%{_includedir}/lua50 -Iinclude
done

# static
$AR rcu libtolua++.a *.o
$RANLIB libtolua++.a

# shared
%{__cc} \
	--shared *.o -llualib50 -llua50 -lm -o tolua++.dll \
	-Wl,--enable-auto-image-base -Wl,--out-implib,libtolua++.dll.a

%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_dlldir}}

install include/tolua++.h $RPM_BUILD_ROOT%{_includedir}
install *.a $RPM_BUILD_ROOT%{_libdir}
install *.dll $RPM_BUILD_ROOT%{_dlldir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_includedir}/tolua++.h
%{_libdir}/libtolua++.dll.a

%files static
%defattr(644,root,root,755)
%{_libdir}/libtolua++.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/tolua++.dll
