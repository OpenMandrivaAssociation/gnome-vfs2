%define _disable_ld_no_undefined 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define	pkgname gnome-vfs
%define	api	2
%define	major	0
%define	libname	%mklibname %{name}_ %{major}
%define	devname %mklibname -d %{name}

Summary:	GNOME virtual file-system libraries
Name:		%{pkgname}%{api}
Version:	2.24.4
Release:	9
License:	GPLv2+ and LGPLv2+
Group:		Graphical desktop/GNOME
Url:		http://www.gnome.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/gnome-vfs/%{url_ver}/%{pkgname}-%{version}.tar.bz2
# (gw) 2.6.0-1mdk set default web browser
Patch5:		gnome-vfs-2.8.2-webclient.patch
# (fc) 2.8.2-1mdk handle about: url (Fedora)
Patch8:		gnome-vfs-2.7.90-schema_about_for_upstream.patch
# (fc) 2.8.3-5mdk support pamconsole mount option (Fedora)
Patch10:	gnome-vfs-2.24.1-console-mount-opt.patch
# (fc) 2.17.91-2mdv replace references to gnomemeeting with ekiga
Patch11:	gnome-vfs-2.17.91-fixh323.patch
# (fc) 2.17.91-3mdv allow OnlyShowIn=KDE .desktop to be used when running under KDE (Mdv bug #26999)
Patch12:	gnome-vfs-2.17.91-onlyshow.patch
# (fc) 2.18.0.1-2mdv fix crash when fstab is being edited (Ubuntu) (GNOME bug #300547)
Patch13:	gnome-vfs-2.20.0-fstab-edit-crash.patch
# (fc) 2.18.0.1-2mdv fix uuid and label mount point duplication (initial idea from Ubuntu bug #57701) (Mdv bug #32792)
Patch14:	gnome-vfs-2.20.0-uuid-label-mount.patch
# (fc) 2.18.0.1-2mdv resolve mount point fstab symlinks (Ubuntu)
Patch15:	gnome-vfs-2.20.0-resolve-fstab-symlinks.patch
# (fc) 2.24.2-3mdv add default media player schema (GNOME bug #435653) (Fedora)
Patch16:	gnome-vfs-2.24.2-default-media-application-schema.patch
# (fc) 2.24.2-3mdv ensure mailto evolution command is a mailer (RH bug #197868) (Fedora)
Patch17:	gnome-vfs-2.15.91-mailto-command.patch
# (fc) 2.24.2-3mdv fix dbus error (Fedora bug #486286) (Fedora)
Patch18:	gnome-vfs-2.24.xx-utf8-mounts.patch
# (fc) CVE-2009-2473 gnome-vfs2 embedded neon: billion laughs DoS attacck (Fedora)
Patch19:	gnome-vfs-2.24.3-CVE-2009-2473.patch

BuildRequires:	docbook-dtd412-xml
BuildRequires:	gawk
BuildRequires:	GConf2
BuildRequires:	gnome-mime-data
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	perl-XML-Parser
BuildRequires:	acl-devel
BuildRequires:	bzip2-devel
BuildRequires:	fam-devel
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0) >= 1.1.1
BuildRequires:	pkgconfig(glib-2.0) >= 2.9.3
BuildRequires:	pkgconfig(libssl)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(smbclient)
Requires(post,preun):	GConf2 >= 1.1.1
Requires:	dbus-x11
# needed for www-browser
Requires:	desktop-common-data
Requires:	gnome-mime-data >= 2.0.0
Requires:	shared-mime-info
Conflicts:	%{_lib}gnome-vfs2_0 < 2.24.4-5

%description
The GNOME Virtual File System provides an abstraction to common file
system operations like reading, writing and copying files, listing
directories and so on.  It is similar in spirit to the Midnight
Commander's VFS (as it uses a similar URI scheme) but it is designed
from the ground up to be extensible and to be usable from any
application.

%package -n %{libname}
Summary:	%{summary}
Group:		System/Libraries

%description -n %{libname}
This package contains the main GNOME VFS libraries, which is required
by the basic GNOME 2 system.

%package -n %{devname}
Summary:	Libraries and include files for gnome-vfs
Group:		Development/GNOME and GTK+
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package includes libraries and header files for developing
GNOME VFS applications.

%prep
%setup -qn %{pkgname}-%{version}
%apply_patches

# this is a hack for glib2.0 >= 2.31.0
sed -i -e 's/-DG_DISABLE_DEPRECATED//g' \
	./daemon/Makefile.* \
	./libgnomevfs/Makefile.*

%build
%configure2_5x \
	--enable-gtk-doc=yes \
	--disable-selinux \
	--disable-hal \
	--disable-static

%make

%install
%makeinstall_std

# multiarch policy
%multiarch_includes %{buildroot}%{_includedir}/gnome-vfs-2.0/libgnomevfs/gnome-vfs-file-size.h

# we ship our own files in drakconf and drakwizard
rm -f %{buildroot}%{_sysconfdir}/gnome-vfs-2.0/vfolders/{system,server}-settings.vfolder-info

%find_lang %{pkgname}-2.0

%define	schemas desktop_default_applications desktop_gnome_url_handlers system_dns_sd system_http_proxy system_smb 

%preun
%preun_uninstall_gconf_schemas %schemas

%files -n %{name} -f %{pkgname}-2.0.lang
%doc AUTHORS NEWS README
%config(noreplace) %{_sysconfdir}/%{pkgname}-*
%config(noreplace) %{_sysconfdir}/gconf/schemas/*
%{_bindir}/*
%{_datadir}/dbus-1/services/*.service
%dir %{_libdir}/%{pkgname}-2.0
%dir %{_libdir}/%{pkgname}-2.0/modules
%{_libdir}/%{pkgname}-2.0/modules/*.so
%{_libexecdir}/gnome-vfs-daemon

%files -n %{libname}
%{_libdir}/libgnomevfs-%{api}.so.%{major}*

%files -n %{devname}
%doc ChangeLog
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/gnome-vfs*2.0/*
%dir %{multiarch_includedir}/gnome-vfs-2.0
%dir %{multiarch_includedir}/gnome-vfs-2.0/libgnomevfs
%{multiarch_includedir}/gnome-vfs-2.0/libgnomevfs/gnome-vfs-file-size.h
%{_libdir}/*.so
%{_libdir}/%{pkgname}-*/include
%{_libdir}/pkgconfig/*.pc

