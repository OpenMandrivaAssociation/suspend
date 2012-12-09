# Not really used yet, so disable for now
%bcond_with	uclibc

Summary:	Userland tools for suspend-to-disk and suspend-to-RAM
Name:		suspend
Version:	1.0
Release:	3
%define distname %{name}-utils-%{version}
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

License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://suspend.sourceforge.net/
BuildRequires:	pciutils-devel libx86-devel liblzo-devel 
BuildRequires:	zlib-devel
# (tv) fix upgrade ordering (libpci3 needs to be updaded from 3.0 to 3.1 before ldetect is upgraded):
Requires:	%{mklibname pci 3} >= 3.1
ExcludeArch:	ppc
Obsoletes:	wltool
Obsoletes:	suspend-wltool
Requires:   dracut
Requires(post):	drakxtools-backend >= 10.4.97-1mdv2007.1
BuildRequires:	plymouth-devel >= 0.8.6.1-2
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

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
%setup -q -n %{distname}
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


%changelog
* Mon Aug 13 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0-1
+ Revision: 814667
- bump versioned dependency on plymouth-devel
- add Dell Latitude E6510 to whitelist
- clean out old junk
- new version
- fix dependency on mkinitrd

* Fri May 06 2011 Oden Eriksson <oeriksson@mandriva.com> 0.8-12.20080612
+ Revision: 670250
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8-11.20080612mdv2011.0
+ Revision: 607758
- rebuild

* Wed May 26 2010 Pascal Terjan <pterjan@mandriva.org> 0.8-10.20080612mdv2010.1
+ Revision: 546161
- fix resume when splash = n in suspend.conf

* Wed Apr 21 2010 Frederic Crozat <fcrozat@mandriva.com> 0.8-9.20080612mdv2010.1
+ Revision: 537679
- Update plymouth patch to work with plymouth 0.8.x

  + Luis Daniel Lucio Quiroz <dlucio@mandriva.org>
    - BR fix
    - Rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.8-8.20080612mdv2010.1
+ Revision: 524138
- rebuilt for 2010.1

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - disable uClibc build for now
    - really use same layout for uclibc root
    - build uclibc linked resume binary
    - correct license tag

* Wed Sep 09 2009 Frederic Crozat <fcrozat@mandriva.com> 0.8-6.20080612mdv2010.0
+ Revision: 435629
- Improve plymouth patch to no hide text when plymouth isn't install

* Mon Sep 07 2009 Frederic Crozat <fcrozat@mandriva.com> 0.8-5.20080612mdv2010.0
+ Revision: 432674
- Patch105: add support for plymouth
- switch to plymouth

* Tue Sep 01 2009 Thierry Vignaud <tv@mandriva.org> 0.8-4.20080612mdv2010.0
+ Revision: 423621
- fix upgrade ordering (libpci3 needs to be updaded from 3.0 to 3.1 before
  ldetect is upgraded) (#53347)
- fix build

* Fri Mar 27 2009 Olivier Blin <blino@mandriva.org> 0.8-3.20080612mdv2009.1
+ Revision: 361593
- kill splashy before resume binary starts it (#44639)

* Wed Feb 04 2009 Andrey Borzenkov <arvidjaar@mandriva.org> 0.8-2.20080612mdv2009.1
+ Revision: 337346
- BuildRequires zlib-devel
- actually add printf format fixes
- patch103 - fix printf format errors
- rediff fuzzy patch101
- rediff fuzzy patch100

* Fri Sep 12 2008 Olivier Blin <blino@mandriva.org> 0.8-1.20080612mdv2009.0
+ Revision: 284200
- remove unwanted comments in config file from opensuse patch
- do not require glibc-static-devel, resume binary is not static anymore (thanks spuk)
- whitelist update for MacBook1,1 (for kernel >= 2.6.25, from opensuse)
- more verbose logging to stderr -> pm-utils logfile (from opensuse)
- workaround temporary vbetool failures (patch from opensuse)
- read keyboard events from /dev/input instead of stdin, to cope with splashy (from CVS/opensuse)
- enable compression by default (from opensuse)
- add mulithreaded image saving patch (from opensuse)
- add config file comments patch from opensuse (maybe not totally relevant, but needed to apply cleanly multithreading patch)
- use opensuse patch to enable splash by default
- update doc files list
- drop merged splashy detection patch
- update to cvs snapshot 20080612 (from opensuse package)

* Thu Sep 04 2008 Olivier Blin <blino@mandriva.org> 0.8-1mdv2009.0
+ Revision: 280474
- build dynamic resume binary (static splashy support would require a libgcc_s.a)
- fix splashy detection (from upstream CVS)
- enable splashy
- remove suspend dir hack, configure defaults to /usr/sbin
- remove old config hack for udev
- enable lzo compression
- package resume utility in its new location and add a compatibility symlink
- rediff no_s2ram_quirks patch (and keep including s2ram.h)
- buildrequire libx86-devel
- run configure
- 0.8

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.5-13mdv2009.0
+ Revision: 225538
- rebuild

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.5-12mdv2008.1
+ Revision: 179550
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

