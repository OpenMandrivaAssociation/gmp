# XXX this should really be the default behaviour of rpm..
%define	__noautoreqfiles	%{_docdir}

%define major 10
%define major_xx 4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define libgmpxx %mklibname %{name}xx %{major_xx}
%define devgmpxx %mklibname %{name}xx -d
# Turn 6.0.0a etc. into 6.0.0
%define majorversion %(echo %{version} | sed -e 's/[a-z]//')

%bcond_without	uclibc

Summary:	A GNU arbitrary precision library
Name:		gmp
Version:	6.0.0a
Release:	4
License:	GPLv3
Group:		System/Libraries
Url:		http://gmplib.org/
Source0:	ftp://ftp.gmplib.org/pub/%{name}-%{majorversion}/%{name}-%{version}.tar.lz
Source1:	ftp://ftp.gmplib.org/pub/%{name}-%{majorversion}/%{name}-%{version}.tar.lz.sig
Patch0:		gmp-5.1.0-x32-build-fix.patch
Patch1:		gmp-01-arm-asm-conditional-on-no-thumb-1.patch
Patch2:		gmp-02-arm-asm-conditional-on-no-thumb-2.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(ncurses)
# For unpacking the tarball
BuildRequires:	lzip
%if %{with uclibc}
BuildRequires:	uClibc-devel
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

%package -n	%{libname}
Summary:	A GNU arbitrary precision library
Group:		System/Libraries

%description -n	%{libname}
This package contains a shared library for %{name}.

%package -n	uclibc-%{libname}
Summary:	A GNU arbitrary precision library (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package -n	%{libgmpxx}
Summary:	C++ support for GMP
Group:		System/Libraries

%description -n	%{libgmpxx}
C++ support for GMP.

%package -n	%{devgmpxx}
Summary:	C++ Development tools for the GMP
Group:		Development/C++
Requires:	%{libgmpxx} >= %{version}-%{release}
Provides:	gmpxx-devel = %{version}-%{release}

%description -n	%{devgmpxx}
C++ Development tools for the GMP.

%prep
%setup -qn %{name}-%{majorversion}
%apply_patches
autoreconf -fi

%build
CONFIGURE_TOP=$PWD
%define	noconftarget 1
%if %{with uclibc}
# workaround segfault...
%global uclibc_cflags %{uclibc_cflags} -O2
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--disable-cxx \
	--enable-static \
	--enable-fft
%make
popd
%endif

mkdir -p glibc
pushd glibc
%configure \
	--enable-cxx \
	--enable-static \
	--enable-mpbsd \
	--enable-fft
%make
popd

%if ! %cross_compiling
%check
# All tests must pass
make -C glibc check
%endif

%install
%if %{with uclibc}
%makeinstall_std -C uclibc

%multiarch_includes %{buildroot}%{uclibc_root}%{_includedir}/gmp.h

%endif
%makeinstall_std -C glibc

%multiarch_includes %{buildroot}%{_includedir}/gmp.h

%files -n %{libname}
%doc NEWS README
%{_libdir}/libgmp.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}%{_libdir}/libgmp.so.%{major}*
%endif

%files -n %{devname}
%doc doc demos
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_includedir}/gmp.h
%{multiarch_includedir}/gmp.h
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libgmp.so
%{uclibc_root}%{_libdir}/libgmp.a
%{uclibc_root}%{_includedir}/gmp.h
%{uclibc_root}%{multiarch_includedir}/gmp.h
%endif
%{_infodir}/gmp.info*

%files -n %{libgmpxx}
%{_libdir}/libgmpxx.so.%{major_xx}*

%files -n %{devgmpxx}
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_includedir}/gmpxx.h
