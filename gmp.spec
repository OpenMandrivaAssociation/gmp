# XXX this should really be the default behaviour of rpm..
%define __requires_exclude_from %{_docdir}

%define major 10
%define major_xx 4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define libgmpxx %mklibname %{name}xx %{major_xx}
%define devgmpxx %mklibname %{name}xx -d
# Turn 6.0.0a etc. into 6.0.0
%define majorversion %(echo %{version} | sed -e 's/[a-z]//')

# Overriding default flags because of https://llvm.org/bugs/show_bug.cgi?id=26711
# (tpg) seems like tests still segfaults 2016-12-27
# (tpg) still valid 2017-12-21
# (tpg) do not ad %optlfags here as gmp will crash 2018-07-31
%global optflags -O3 -gdwarf-4 -Wstrict-aliasing=2 -pipe -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2 -fstack-protector --param=ssp-buffer-size=4  -fPIC

Summary:	A GNU arbitrary precision library
Name:		gmp
Version:	6.1.2
Release:	6
License:	GPLv3
Group:		System/Libraries
Url:		http://gmplib.org/
Source0:	ftp://ftp.gmplib.org/pub/%{name}-%{majorversion}/%{name}-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
Patch0:		gmp-5.1.0-x32-build-fix.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands.

GNU MP is fast for several reasons:
   - it uses fullwords as the basic arithmetic type,
   - it uses fast algorithms,
   - it carefully optimizes assembly code for many CPUs' most common
     inner loops
   - it generally emphasizes speed over simplicity/elegance in its
     operations

%package -n %{libname}
Summary:	A GNU arbitrary precision library
Group:		System/Libraries

%description -n %{libname}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package -n %{libgmpxx}
Summary:	C++ support for GMP
Group:		System/Libraries

%description -n %{libgmpxx}
C++ support for GMP.

%package -n %{devgmpxx}
Summary:	C++ Development tools for the GMP
Group:		Development/C++
Requires:	%{libgmpxx} >= %{EVRD}
Requires:	%{devname} = %{EVRD}
Provides:	gmpxx-devel = %{EVRD}

%description -n %{devgmpxx}
C++ Development tools for the GMP.

%prep
%autosetup -n %{name}-%{majorversion} -p1
autoreconf -fi

%build
autoreconf -ifv

if as --help | grep -q execstack; then
  # the object files do not require an executable stack
  export CCAS="%{__cc} -c -Wa,--noexecstack"
fi

%configure \
	--enable-cxx \
	--enable-static \
	--enable-mpbsd \
	--enable-fft

sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|-lstdc++ -lm|-lstdc++|' \
    -i libtool
export LD_LIBRARY_PATH="$(pwd)/.libs"

%make_build

%if ! %cross_compiling
%check
# All tests must pass
make check
%endif

%install
%make_install

%if %{mdvver} <= 3000000
%multiarch_includes %{buildroot}%{_includedir}/gmp.h
%endif

%files -n %{libname}
%{_libdir}/libgmp.so.%{major}*

%files -n %{devname}
%doc doc demos
%doc NEWS README
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_includedir}/gmp.h
%if %{mdvver} <= 3000000
%{multiarch_includedir}/gmp.h
%endif
%{_infodir}/gmp.info*

%files -n %{libgmpxx}
%{_libdir}/libgmpxx.so.%{major_xx}*

%files -n %{devgmpxx}
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_includedir}/gmpxx.h
