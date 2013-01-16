# Not really used yet, so disable for now
%bcond_with	uclibc
%define distname %{name}-utils-%{version}

Summary:	Userland tools for suspend-to-disk and suspend-to-RAM
Name:		suspend
Version:	1.0
Release:	4
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://suspend.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/%{name}/%{distname}.tar.bz2

#- opensuse patches
Patch1:		suspend-comment-configfile-options.diff
Patch3:		suspend-default-compress.diff
Patch5:		suspend-default-splash.diff
Patch13:	suspend-0.80-vbetool-retry-on-errors.diff
Patch15:	suspend-1.0-suspend-output-to-logfile.diff
Patch70:	suspend-0.80-whitelist-openSUSE11.diff

#- Mandriva patches
Patch100:	suspend-1.0-no_s2ram_quirks.patch
Patch101:	suspend-0.5-bootsplash.patch
Patch102:	suspend-0.8.20080612-mdvcomment.patch
Patch103:	suspend-0.8-printf_format.patch
# (blino) kill splashy before resume binary starts it
Patch104:	suspend-0.8.20080612-stopsplashy.patch
# (fc) plymouth support
Patch105:	suspend-1.0-plymouth.patch
# (proyvind): to get _GNU_SOURCE defined, fixes build with uclibc
Patch106:	suspend-0.8.20080612-configure-gnu-source.patch
Patch107:	suspend-utils-1.0-add-latitude-e6510-to-whitelist.patch
Patch108:	suspend-automake-1.13.patch
ExcludeArch:	ppc

BuildRequires:	liblzo-devel 
BuildRequires:	libx86-devel
BuildRequires:	pkgconfig(libpci)
BuildRequires:	pkgconfig(ply-splash-core)
BuildRequires:	pkgconfig(zlib)
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif
Requires:	dracut
#Requires(post):	drakxtools-backend

%description
The goal of the project is to create a tool that can handle the so
called "suspend-to-both". Suspend to both means that prior putting the
system in STR (suspend to ram) a snapshot of the running system is
taken and stored on disk (as suspend to disk); if for any reason
(e.g. battery depleted) the state store in the RAM is lost the user
can resume from the disk without loosing data.

Currenty suspend-to-ram and suspend-to-disk are handled by two
different program, s2ram and s2disk.

%package	s2ram
Summary:	Suspend-to-RAM utility
Group:		System/Kernel and hardware
Conflicts:	suspend < 0.5-4mdv2007.1

%description	s2ram
s2ram is a suspend-to-RAM utility.

%prep
%setup -qn %{distname}
#- opensuse patches
%patch1 -p1
%patch3 -p0
%patch5 -p0
%patch13 -p0
%patch15 -p1 -b .log~

#- Mandriva patches
%patch100 -p1 -b .no_s2ram_quirks~
%patch101 -p1 -b .bootsplash~
%patch102 -p1 -b .mdvcomment~
%patch103 -p1 -b .printf_format~
%patch104 -p1 -b .stopsplashy~
%patch105 -p1 -b .plymouth~
%patch106 -p1 -b .gnu_source~
%patch107 -p1 -b .e6510~
%patch108 -p1 -b .am113~

#needed by patch105
libtoolize --force
autoreconf

%build
export CONFIGURE_TOP=`pwd`
%if %{with uclibc}
mkdir -p uclibc
cd uclibc
%configure2_5x \
  CC="%{uclibc_cc}" \
  CFLAGS="%{uclibc_cflags}" \
  --enable-compress \
  --enable-plymouth \
  --enable-threads \
  --disable-resume-static
%make
cd ..
%endif

mkdir -p shared
cd shared
%configure2_5x \
  --enable-compress \
  --enable-plymouth \
  --enable-threads \
  --disable-resume-static
%make
cd ..

%install
install -d %{buildroot}{,%{uclibc_root}}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}
%if %{with uclibc}
install -m755 uclibc/resume -D %{buildroot}%{uclibc_root}%{_libdir}/%{name}/resume
ln -sf %{uclibc_root}%{_libdir}/%{name}/resume %{buildroot}%{uclibc_root}%{_sbindir}/resume
%endif

%makeinstall_std -C shared
rm -rf %{buildroot}%{_docdir}/suspend-utils
ln -sf %{_libdir}/%{name}/resume %{buildroot}%{_sbindir}

%post
/usr/sbin/bootloader-config --action rebuild-initrds || :

%files
%doc HOWTO README README.s2ram-whitelist
%{_sbindir}/resume
%{_sbindir}/s2both
%{_sbindir}/s2disk
%{_sbindir}/swap-offset
%{_libdir}/%{name}/resume
%config(noreplace) %{_sysconfdir}/%{name}.conf
%if %{with uclibc}
%{uclibc_root}%{_sbindir}/resume
%{uclibc_root}%{_libdir}/%{name}/resume
%endif

%files s2ram
%{_sbindir}/s2ram

