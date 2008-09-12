%define name suspend
%define version 0.8
%define cvs 20080612
%if %{cvs}
%define distname %{name}-%{version}.%{cvs}
%define release %mkrel 1.%{cvs}
%else
%define distname %{name}-%{version}
%define release %mkrel 1
%endif

Summary: Userland tools for suspend-to-disk and suspend-to-RAM
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/%{name}/%{distname}.tar.bz2

#- opensuse patches
Patch1: suspend-comment-configfile-options.diff
# not needed in Mandriva
#Patch2: suspend-susescripts.diff
Patch3: suspend-default-compress.diff
# no more bootsplash in kernel and thus no /proc/splash, patch not needed
#Patch4: suspend-disable-bootsplash.diff
Patch5: suspend-default-splash.diff
# user interruption could be considered as an error, don't apply
#Patch6: suspend-0.80-dont-return-eintr-on-abort.diff
Patch10: suspend-use-input-device.diff
# we don't test whitelist
#Patch11: suspend-0.80-make-whitelist-test.diff
# not needed, builds fine
#Patch12: suspend-buildfixes.diff
Patch13: suspend-0.80-vbetool-retry-on-errors.diff
Patch14: suspend-multithreaded-image-saving.diff
Patch15: suspend-0.80-suspend-output-to-logfile.diff
# we don't use bootsplash, not needed
#Patch16: suspend-splash-verbose-debug.diff
Patch70: suspend-0.80-whitelist-openSUSE11.diff
# opensuse-specific
#Patch99: suspend-0.80-opensuse.org.diff

#- Mandriva patches
Patch100: suspend-0.8-no_s2ram_quirks.patch
Patch101: suspend-0.5-bootsplash.patch

License: GPL
Group: System/Kernel and hardware
Url: http://suspend.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: pciutils-devel glibc-static-devel libx86-devel liblzo-devel splashy-devel
ExcludeArch: ppc
Obsoletes: wltool
Obsoletes: suspend-wltool
Requires(post): drakxtools-backend >= 10.4.97-1mdv2007.1
Requires(post): mkinitrd >= 4.2.17-27mdv2007.1

%description
The goal of the project is to create a tool that can handle the so
called "suspend-to-both". Suspend to both means that prior putting the
system in STR (suspend to ram) a snapshot of the running system is
taken and stored on disk (as suspend to disk); if for any reason
(e.g. battery depleted) the state store in the RAM is lost the user
can resume from the disk without loosing data.

Currenty suspend-to-ram and suspend-to-disk are handled by two
different program, s2ram and s2disk.

%package s2ram
Summary: Suspend-to-RAM utility
Group: System/Kernel and hardware
Conflicts: suspend < 0.5-4mdv2007.1

%description s2ram
s2ram is a suspend-to-RAM utility.

%prep
%setup -q -n %{distname}
#- opensuse patches
%patch1 -p1
#%patch2 -p0
%patch3 -p0
#%patch4 -p0
%patch5 -p0
#%patch6 -p1
%patch10 -p1
#%patch11 -p0
#%patch12 -p0
%patch13 -p0
%patch14 -p1
%patch15 -p1
#%patch16 -p1
%patch70 -p1
#%patch99 -p1

#- Mandriva patches
%patch100 -p1 -b .no_s2ram_quirks
%patch101 -p1 -b .bootsplash

%build
%configure \
  --enable-compress \
  --enable-splashy \
  --enable-threads \
  --disable-resume-static
%make

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_sysconfdir}
%makeinstall_std
ln -sf %{_libdir}/%{name}/resume %{buildroot}%{_sbindir}

%clean
rm -rf %{buildroot}

%post
/usr/sbin/bootloader-config --action rebuild-initrds || :

%files
%defattr(-,root,root)
%doc HOWTO README README.s2ram-whitelist TODO
%{_sbindir}/resume
%{_sbindir}/s2both
%{_sbindir}/s2disk
%{_sbindir}/swap-offset
%{_libdir}/%{name}/resume
%config(noreplace) %{_sysconfdir}/%{name}.conf

%files s2ram
%defattr(-,root,root)
%{_sbindir}/s2ram
