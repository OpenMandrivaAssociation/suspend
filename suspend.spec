%define name suspend
%define version 0.8
%define release %mkrel 1

Summary: Userland tools for suspend-to-disk and suspend-to-RAM
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0: suspend-0.8-no_s2ram_quirks.patch
Patch1: suspend-0.5-bootsplash.patch
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
%setup -q
%patch0 -p1 -b .no_s2ram_quirks
%patch1 -p1 -b .bootsplash
perl -pi -e 's/^#splash = y$/splash = y/' conf/suspend.conf

%build
%configure \
  --enable-compress \
  --enable-splashy
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
%doc ChangeLog HOWTO README README.s2ram-whitelist ReleaseNotes TODO
%{_sbindir}/resume
%{_sbindir}/s2both
%{_sbindir}/s2disk
%{_sbindir}/swap-offset
%{_libdir}/%{name}/resume
%config(noreplace) %{_sysconfdir}/%{name}.conf

%files s2ram
%defattr(-,root,root)
%{_sbindir}/s2ram


