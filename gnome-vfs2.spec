%define req_gconf2_version	1.1.1
%define req_orbit_version	2.9.0

%define pkgname gnome-vfs
%define api_version	2
%define lib_major	0
%define lib_name	%mklibname %{name}_ %{lib_major}

%if %mdkver >= 200610
%define enable_hal 1
%else
%define enable_hal 0
%endif

Summary:	GNOME virtual file-system libraries
Name:		%{pkgname}%{api_version}
Version: 2.18.0.1
Release: %mkrel 1
License:	LGPL
Group:		Graphical desktop/GNOME
URL:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{pkgname}/%{pkgname}-%{version}.tar.bz2
# (gw) 2.6.0-1mdk set default web browser
Patch5:		gnome-vfs-2.8.2-webclient.patch
# (fc) 2.8.2-1mdk handle about: url (Fedora)
Patch8:		gnome-vfs-2.7.90-schema_about_for_upstream.patch
# (fc) 2.8.3-5mdk support pamconsole mount option (Fedora)
Patch10:	gnome-vfs-2.8.1-console-mount-opt.patch
# (fc) 2.17.91-2mdv replace references to gnomemeeting with ekiga
Patch11:	gnome-vfs-2.17.91-fixh323.patch
# (fc) 2.17.91-3mdv allow OnlyShowIn=KDE .desktop to be used when running under KDE (Mdv bug #26999)
Patch12:	gnome-vfs-2.17.91-onlyshow.patch

BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	gawk
BuildRequires:  avahi-client-devel avahi-glib-devel
BuildRequires:  libacl-devel
%if %enable_hal
BuildRequires:  hal-devel >= 0.5
BuildRequires:  dbus-glib-devel
%endif
BuildRequires:  perl-XML-Parser
BuildRequires:  gnome-mime-data
BuildRequires:	libcdda-devel bzip2-devel openssl-devel fam-devel
BuildRequires:  libsmbclient-devel >= 3.0.20
BuildRequires:	libGConf2-devel >= %{req_gconf2_version}
BuildRequires:	libORBit2-devel >= %{req_orbit_version}
BuildRequires:  gtk-doc
BuildRequires:	intltool
BuildRequires:  glib2-devel >= 2.9.3
BuildRequires:  dbus-devel
BuildRequires:	libxml2-devel
Requires:	%{lib_name} = %{version}
Requires(post):	GConf2 >= %{req_gconf2_version}
Requires(preun):	GConf2 >= %{req_gconf2_version}
Requires:	dbus-x11
Conflicts:	libgnome2 <= 2.4.0
Requires:	shared-mime-info, libsmbclient
Requires:	mandrake_desk >= 10.1-6mdk
Obsoletes:	gnome-vfs-extras
Provides:	gnome-vfs-extras

%description
The GNOME Virtual File System provides an abstraction to common file
system operations like reading, writing and copying files, listing
directories and so on.  It is similar in spirit to the Midnight
Commander's VFS (as it uses a similar URI scheme) but it is designed
from the ground up to be extensible and to be usable from any
application.



%package -n %{lib_name}
Summary:	%{summary}
Group:		%{group}
Provides:	lib%{name} = %{version}-%{release}
Requires:	gnome-mime-data >= 2.0.0
Requires:   %{name} >= %{version}-%{release}
Conflicts: %{name} < 2.10.1-9mdk

%description -n %{lib_name}
The GNOME Virtual File System provides an abstraction to common file
system operations like reading, writing and copying files, listing
directories and so on.

This package contains the main GNOME VFS libraries, which is required
by the basic GNOME 2 system.


%package -n %{lib_name}-devel
Summary:	Libraries and include files for gnome-vfs
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Requires:	%{lib_name} = %{version}-%{release}
Requires:	libbonobo2_x-devel
Requires:   libGConf2-devel >= %{req_gconf2_version}

%description -n %{lib_name}-devel
The GNOME Virtual File System provides an abstraction to common file
system operations like reading, writing and copying files, listing
directories and so on.

This package includes libraries and header files for developing
GNOME VFS applications.


%prep
%setup -q -n %{pkgname}-%{version}
%patch5 -p1 -b .webclient
%patch8 -p1 -b .about
%patch10 -p1 -b .pamconsole
%patch11 -p1 -b .fixh323
%patch12 -p1 -b .onlyshow

%build

%configure2_5x --enable-gtk-doc=yes --disable-selinux \
%if %enable_hal
--enable-hal
%else
--disable-hal
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

# multiarch policy
%multiarch_includes $RPM_BUILD_ROOT%{_includedir}/gnome-vfs-2.0/libgnomevfs/gnome-vfs-file-size.h


# we ship our own files in drakconf and drakwizard
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/gnome-vfs-2.0/vfolders/{system,server}-settings.vfolder-info

# don't package these
rm -f %buildroot%{_libdir}/%{pkgname}-*/modules/*a

%{find_lang} %{pkgname}-2.0

%clean
rm -rf %{buildroot}

%define schemas desktop_default_applications desktop_gnome_url_handlers system_dns_sd system_http_proxy system_smb 

%post 
%post_install_gconf_schemas %schemas

%preun
%preun_uninstall_gconf_schemas %schemas

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%files -n %{name} -f %{pkgname}-2.0.lang
%defattr(-, root, root)
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/%{pkgname}-*
%config(noreplace) %{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%_datadir/dbus-1/services/*.service

%files -n %{lib_name}
%defattr(-, root, root)
%{_libdir}/lib*.so.*
%dir %{_libdir}/%{pkgname}-*
%dir %{_libdir}/%{pkgname}-*/modules
%{_libdir}/%{pkgname}-2.0/modules/*.so

%files -n %{lib_name}-devel
%defattr(-, root, root)
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/*
%{_libdir}/*.a
%attr(644,root,root) %{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/%{pkgname}-*/include
%{_libdir}/pkgconfig/*.pc


