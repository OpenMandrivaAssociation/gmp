%define major 3
%define major_xx 4
%define major_mp 3

%define lib_name	%mklibname %{name} %{major}
%define lib_name_gmpxx	%mklibname %{name}xx %{major_xx}
%define	lib_name_mp	%mklibname %{name}mp %{major_mp} 

Summary:	A GNU arbitrary precision library
Name:		gmp
Version:	4.2.2
Release:	%mkrel 1
License:	LGPLv2+ 
Group:		System/Libraries
URL:		http://www.swox.com/gmp/
Source0:	ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.bz2
Source1:	ftp://ftp.gnu.org/pub/gnu/gmp/%{name}-%{version}.tar.bz2.sig
BuildRequires:	autoconf2.5
BuildRequires:  automake1.7

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

%package -n	%{lib_name}
Summary:	A GNU arbitrary precision library
Group:		System/Libraries
Provides:	lib%{name} = %{version}-%{release}

%description -n	%{lib_name}
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

%package -n	%{lib_name}-devel
Summary:	Development tools for the GNU MP arbitrary precision library
Group:		Development/C
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires:	%{lib_name} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
The static libraries, header files and documentation for using the GNU MP
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package -n	%{lib_name_gmpxx}
Summary:	C++ support for GMP
Group:		System/Libraries
Requires:	%{lib_name} = %{version}-%{release}
Provides:	libgmpxx = %{version}-%{release}
Obsoletes:	%mklibname %{name}xx 3

%description -n	%{lib_name_gmpxx}
C++ support for GMP.

%package -n	%{lib_name_gmpxx}-devel
Summary:	C++ Development tools for the GMP
Group:		Development/C++
Requires:	%{lib_name}-devel = %{version}-%{release}
Requires:	%{lib_name_gmpxx} = %{version}-%{release}
Provides:	lib%{name}xx-devel = %{version}-%{release}
Provides:	gmpxx-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name}xx 3 -d

%description -n	%{lib_name_gmpxx}-devel
C++ Development tools for the GMP.

%package -n	%{lib_name_mp}
Summary:	Berkley MP compatibility library for GMP
Group:		System/Libraries
Provides:	libgmp_mp = %{version}-%{release}

%description -n	%{lib_name_mp}
Berkley MP compatibility library for GMP.

%package -n	%{lib_name_mp}-devel
Summary:	Development tools for Berkley MP compatibility library for GMP
Group:		Development/C
Requires:	%{lib_name_mp} = %{version}-%{release}
Provides:	lib%{name}mp-devel = %{version}-%{release}
Provides:	mp-devel = %{version}-%{release}

%description -n	%{lib_name_mp}-devel
Development tools for Berkley MP compatibility library for GMP.

%prep
%setup -q

%build
%{configure2_5x} --enable-cxx --enable-mpbsd
%{make}

%check
# All tests must pass
make check

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%post -n %{lib_name_gmpxx} -p /sbin/ldconfig
%postun -n %{lib_name_gmpxx} -p /sbin/ldconfig

%post -n %{lib_name_mp} -p /sbin/ldconfig
%postun -n %{lib_name_mp} -p /sbin/ldconfig

%post -n %{lib_name}-devel
%_install_info %{name}.info

%preun -n %{lib_name}-devel
%_remove_install_info %{name}.info

%clean
%{__rm} -rf %{buildroot}

%files -n %{lib_name}
%defattr(-,root,root)
%doc COPYING.LIB NEWS README
%{_libdir}/libgmp.so.%{major}*

%files -n %{lib_name}-devel
%defattr(-,root,root)
%doc doc demos
%{_libdir}/libgmp.so
%{_libdir}/libgmp.a
%{_libdir}/libgmp.la 
%{_includedir}/gmp.h
%{_infodir}/gmp.info*

%files -n %{lib_name_gmpxx}
%defattr(-,root,root)
%{_libdir}/libgmpxx.so.%{major_xx}*

%files -n %{lib_name_gmpxx}-devel
%defattr(-,root,root)
%{_libdir}/libgmpxx.so
%{_libdir}/libgmpxx.a
%{_libdir}/libgmpxx.la
%{_includedir}/gmpxx.h

%files -n %{lib_name_mp}
%defattr(-,root,root)
%{_libdir}/libmp.so.%{major_mp}*

%files -n %{lib_name_mp}-devel
%defattr(-,root,root)
%{_includedir}/mp.h
%{_libdir}/libmp.a
%{_libdir}/libmp.so
%{_libdir}/libmp.la
