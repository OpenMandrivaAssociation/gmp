%define major 10
%define major_xx 4
%define major_mp 3

%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define libname_gmpxx %mklibname %{name}xx %{major_xx}
%define develname_gmpxx %mklibname %{name}xx -d

Summary:	A GNU arbitrary precision library
Name:		gmp
Version:	5.1.0
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		http://gmplib.org/
Source0:	ftp://ftp.gmplib.org/pub/%{name}-%version/%{name}-%{version}.tar.xz
Source1:	ftp://ftp.gmplib.org/pub/%{name}-%version/%{name}-%{version}.tar.xz.sig
Patch0:		gmp-5.1.0-x32-build-fix.patch
Patch2:		gmp-5.0.5-automake-1.13.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
# XXX this should really be the default behaviour of rpm..
%define	__noautoreqfiles	%{_docdir}

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
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands.

GNU MP is fast for several reasons:
  - it uses fullwords as the basic arithmetic type,
  - it uses fast algorithms
  - it carefully optimizes assembly code for many CPUs' most common
    inner loops
  - it generally emphasizes speed over simplicity/elegance in its
    operations

%package -n	%{develname}
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires(post):	rpm-helper
Requires(preun):rpm-helper
Requires:	%{libname} >= %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 3 -d} < 4.2.4

%description -n	%{develname}
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package -n	%{libname_gmpxx}
Summary:	C++ support for GMP
Group:		System/Libraries
Requires:	%{libname} >= %{version}-%{release}
Obsoletes:	%mklibname %{name}xx 3

%description -n	%{libname_gmpxx}
C++ support for GMP.

%package -n	%{develname_gmpxx}
Summary:	C++ Development tools for the GMP
Group:		Development/C++
Requires:	%{develname} >= %{version}-%{release}
Requires:	%{libname_gmpxx} >= %{version}-%{release}
Provides:	gmpxx-devel = %{version}-%{release}
Obsoletes:	%{mklibname %{name}xx 4 -d} < 4.2.4

%description -n	%{develname_gmpxx}
C++ Development tools for the GMP.

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
%configure2_5x	--enable-cxx \
		--enable-mpbsd \
		--enable-fft
%make

%check
# All tests must pass
make check

%install
%makeinstall_std

%multiarch_includes %{buildroot}%{_includedir}/gmp.h

%files -n %{libname}
%doc NEWS README
%{_libdir}/libgmp.so.%{major}*

%files -n %{develname}
%doc doc demos
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_includedir}/gmp.h
%{_infodir}/gmp.info*
%{multiarch_includedir}/gmp.h


%files -n %{libname_gmpxx}
%{_libdir}/libgmpxx.so.%{major_xx}*

%files -n %{develname_gmpxx}
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_includedir}/gmpxx.h
