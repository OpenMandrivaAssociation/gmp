# gmp is used by isl, isl is used by Polly,
# Polly is used by Mesa, Mesa is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# Workaround for broken libtool messing with rpaths
%if %{cross_compiling}
%define prefer_gcc 1
%endif

# XXX this should really be the default behaviour of rpm..
%define __requires_exclude_from %{_docdir}

%define major 10
%define major_xx 4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define libgmpxx %mklibname %{name}xx %{major_xx}
%define devgmpxx %mklibname %{name}xx -d
%define lib32name lib%{name}%{major}
%define dev32name lib%{name}-devel
%define lib32gmpxx lib%{name}xx%{major_xx}
%define dev32gmpxx lib%{name}xx-devel
# Turn 6.0.0a etc. into 6.0.0
%define majorversion %(echo %{version} | sed -e 's/[a-z]//')

# (tpg) configure script is broken when LTO is used
# so disable it and push LTO at make_build stage
%define _disable_lto 1

%global optflags %{optflags} -O3

Summary:	A GNU arbitrary precision library
Name:		gmp
Version:	6.3.0
Release:	1
License:	GPLv3
Group:		System/Libraries
Url:		http://gmplib.org/
Source0:	https://gmplib.org/download/gmp/gmp-%{version}.tar.xz
Source1:	%{name}.rpmlintrc
Patch1:		gmp-6.1.2-execstackfix.patch
# (tpg) https://bugzilla.opensuse.org/show_bug.cgi?id=1179751
Patch2:		gmp-6.2.1-arm64-invert_limb.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(ncurses)
%if %{with compat32}
BuildRequires:	devel(libncurses)
BuildRequires:	libc6
%endif

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
Requires:	%{libgmpxx} = %{EVRD}
Requires:	%{devname} = %{EVRD}
Provides:	gmpxx-devel = %{EVRD}

%description -n %{devgmpxx}
C++ Development tools for the GMP.

%if %{with compat32}
%package -n %{lib32name}
Summary:	A GNU arbitrary precision library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains a shared library for %{name}.

%package -n %{dev32name}
Summary:	Development tools for the GNU MP arbitrary precision library (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}
Requires:	%{devname} = %{EVRD}
Requires:	libc6

%description -n %{dev32name}
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package -n %{lib32gmpxx}
Summary:	C++ support for GMP (32-bit)
Group:		System/Libraries

%description -n %{lib32gmpxx}
C++ support for GMP.

%package -n %{dev32gmpxx}
Summary:	C++ Development tools for the GMP (32-bit)
Group:		Development/C++
Requires:	%{lib32gmpxx} = %{EVRD}
Requires:	%{dev32name} = %{EVRD}
Requires:	%{devgmpxx} = %{EVRD}

%description -n %{dev32gmpxx}
C++ Development tools for the GMP.
%endif

%prep
%autosetup -n %{name}-%{majorversion} -p1
autoreconf -fi

export CONFIGURE_TOP="$(pwd)"

%if %{with compat32}
mkdir build32
cd build32
CC="gcc -m32" CXX="g++ -m32" \
CFLAGS="%(echo %{optflags} |sed -e 's,-m64,,g;s,-flto,,g')" \
CXXFLAGS="%(echo %{optflags} |sed -e 's,-m64,,g;s,-flto,,g')" \
LDFLAGS="%(echo %{build_ldflags} |sed -e 's,-m64,,g;s,-flto,,g') -m32" \
../configure \
	--host=i686-openmandriva-linux-gnu \
	--prefix=%{_prefix} \
	--enable-cxx \
	--enable-fat \
	--enable-static

cd ..
%endif

mkdir build
cd build
CC="%{__cc}" CXX="%{__cxx}" \
CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}" \
../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
%if %{cross_compiling}
	--host=%{_target_platform} \
	--target=%{_target_platform} \
%endif
	--enable-cxx \
	--enable-fat \
	--enable-static

sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|-lstdc++ -lm|-lstdc++|' \
    -i libtool

%build
%define noconftarget 1

export LD_LIBRARY_PATH=$(pwd)/.libs

%if %{with compat32}
%make_build -C build32
%endif

# (tpg) configure script is sensitive on LTO so disable it and re-enable on make stage
%make_build -C build CFLAGS="%{optflags} -flto" CXXFLAGS="%{optflags} -flto" LDFLAGS="%{build_ldflags} -flto"

%if ! %cross_compiling
%check
%if %{with compat32}
export LD_LIBRARY_PATH=$(pwd)/build32/.libs
make check -C build32
cat build32/tests/*/test-suite.log
%endif

export LD_LIBRARY_PATH=$(pwd)/build/.libs
# All tests must pass
make check -C build
cat build/tests/*/test-suite.log
%endif

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

# Fix hardcoded size of mp_limb_t (long) with GCC predefined macros
sed -i '/#define GMP_LIMB_BITS/s/64/(__SIZEOF_LONG__ * __CHAR_BIT__)/' %{buildroot}%{_includedir}/gmp.h

%files -n %{libname}
%{_libdir}/libgmp.so.%{major}*

%files -n %{devname}
%doc doc demos
%doc NEWS README
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_includedir}/gmp.h
%{_infodir}/gmp.info*
%{_libdir}/pkgconfig/gmp.pc

%files -n %{libgmpxx}
%{_libdir}/libgmpxx.so.%{major_xx}*

%files -n %{devgmpxx}
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_includedir}/gmpxx.h
%{_libdir}/pkgconfig/gmpxx.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libgmp.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libgmp.so
%{_prefix}/lib/libgmp.a
%{_prefix}/lib/pkgconfig/gmp.pc

%files -n %{lib32gmpxx}
%{_prefix}/lib/libgmpxx.so.%{major_xx}*

%files -n %{dev32gmpxx}
%{_prefix}/lib/libgmpxx.so
%{_prefix}/lib/libgmpxx.a
%{_prefix}/lib/pkgconfig/gmpxx.pc
%endif
