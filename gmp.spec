# XXX this should really be the default behaviour of rpm..
%define	__noautoreqfiles %{_docdir}

%define major 10
%define major_xx 4
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define libgmpxx %mklibname %{name}xx %{major_xx}
%define devgmpxx %mklibname %{name}xx -d
# Turn 6.0.0a etc. into 6.0.0
%define majorversion %(echo %{version} | sed -e 's/[a-z]//')

%global optflags %{optflags} -Ofast

Summary:	A GNU arbitrary precision library
Name:		gmp
Version:	6.1.2
Release:	4
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

%package -n	%{libname}
Summary:	A GNU arbitrary precision library
Group:		System/Libraries

%description -n	%{libname}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

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
Requires:	%{libgmpxx} >= %{EVRD}
Provides:	gmpxx-devel = %{EVRD}

%description -n	%{devgmpxx}
C++ Development tools for the GMP.

%prep
%setup -qn %{name}-%{majorversion}
%apply_patches
autoreconf -fi

%build
%define	noconftarget 1

%configure \
	--enable-cxx \
	--enable-static \
	--enable-mpbsd \
	--enable-fft
%make

%if ! %cross_compiling
%check
# All tests must pass
make check
%endif

%install
%makeinstall_std

%files -n %{libname}
%{_libdir}/libgmp.so.%{major}*

%files -n %{devname}
%doc doc demos
%doc NEWS README
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_includedir}/gmp.h
%{_infodir}/gmp.info*

%files -n %{libgmpxx}
%{_libdir}/libgmpxx.so.%{major_xx}*

%files -n %{devgmpxx}
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_includedir}/gmpxx.h
