%define		realname	tolua++
Summary:	Extended version of tolua, a tool to integrate C/C++ code with Lua - Mingw32 cross version
Summary(pl.UTF-8):	Rozszerzona wersja tolua, narzędzia integrującego kod C/C++ z Lua - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.0.4
Release:	1
License:	Free
Group:		Development/Tools
Source0:	http://www.codenix.com/~tolua/%{realname}-%{version}.tar.bz2
# Source0-md5:	8785100f7c9d9253cb47b530d97a32f6
URL:		http://www.codenix.com/~tolua/
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-lua50
BuildRequires:	crossmingw32-w32api
BuildRequires:	scons
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

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

%package dll
Summary:	%{realname} - DLL library for Windows
Summary(pl.UTF-8):	%{realname} - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
%{realname} - DLL library for Windows.

%description dll -l pl.UTF-8
%{realname} - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB
LDSHARED="%{target}-gcc -shared" ; export LDSHARED
TARGET="%{target}" ; export TARGET

for i in src/lib/tolua_{event,is,map,push,to}.c
do %{__cc} %{rpmcflags} $i -c -I%{arch}/include/lua50 -Iinclude
done

# static
$AR rcu tolua++.a *.o
$RANLIB tolua++.a

# shared
%{__cc} \
	--shared *.o -llualib50 -llua50 -lm -o tolua++.dll \
	-Wl,--enable-auto-image-base -Wl,--out-implib,tolua++.dll.a

%if 0%{!?debug:1}
%{target}-strip *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install include/tolua++.h $RPM_BUILD_ROOT%{arch}/include
install *.a $RPM_BUILD_ROOT%{arch}/lib
install *.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system/*
