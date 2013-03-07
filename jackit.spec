# D-Bus support enabled by default, set "--with nodbus" to disable
%define enable_dbus 1
# Build classic jackd executable as well
%define enable_classic 1

%define     major 0
%define     libname %mklibname jack %{major}
%define     libserver %mklibname jackserver %{major}
%define     develname %mklibname jack -d

Summary:    The Jack Audio Connection Kit 2
Name:       jackit
Version:    1.9.8
Release:    4
# Lib is LGPL, apps are GPL
License:    LGPLv2+ and GPLv2+
Group:      System/Servers
URL:        http://jackaudio.org/
Source0:    http://www.grame.fr/~letz/jack-%{version}.tgz
Buildrequires:  doxygen
BuildRequires:  fltk-devel
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(ncursesw)
BuildRequires:  celt-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libavc1394)
BuildRequires:  pkgconfig(libiec61883) >= 1.1.0
# BuildRequires:  pkgconfig(libffado) >= 1.999.17
BuildRequires:  pkgconfig(libraw1394) >= 1.2.1
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
%if %enable_dbus
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  expat-devel
%endif

%description
This package provides the C++ multiprocessor implementation of the Jack
Audio Connection Kit (JACK), also known as JACK2. This package comes with
enabled D-Bus support for JACK2, which is required by the LADI
session handler.
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (ie. as a
normal application), or can they can run within a JACK server (ie. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.

%package -n %{libname}
Summary:    Library associated with jack
Group:      System/Libraries

%description -n %{libname}
This library is mandatory for the Jack Audio Connection Kit

%package -n %{libserver}
Summary:    Library associated with jack server, needed for jackd/jackdbus
Group:      System/Libraries
Conflicts:  %{libname} < 1.9.8-1

%description -n %{libserver}
This library is mandatory for the Jack Audio Connection Kit Server

%package -n %{develname}
Summary:    Header files for Jack
Group:      Development/C
Requires:   %{libname} = %{version}-%{release}
Requires:   %{libserver} = %{version}-%{release}
Provides:   %{name}-devel = %{version}-%{release}
Obsoletes:  %{mklibname jack 0 -d} < %{version}-%{release}

%description -n %{develname}
Header files for the Jack Audio Connection Kit.

%package    example-clients
Summary:    Example clients that use Jack
Group:      Sound
Requires:   %{name} = %{version}-%{release}

%description    example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%setup -qn jack-%{version}

%build
cd jack-%{version}

# still disable ffado firewire
./waf configure --prefix=%{_prefix} --libdir=/%_lib \
--alsa \
%if %enable_dbus
    --dbus \
%if %enable_classic
    --classic \
%endif
%endif
--doxygen \
-j1

./waf

%install
cd jack-%{version}
cp -a html build/default/
./waf install --destdir=%{buildroot}

# Fix permissions
chmod 0755 %{buildroot}%{_libdir}/*.so*
chmod 0755 %{buildroot}%{_libdir}/jack/*.so

%files
%doc jack-%{version}/README jack-%{version}/README_NETJACK2
%doc %{_mandir}/man1/*
%{_bindir}/jack_zombie
%{_bindir}/jack_bufsize
%{_bindir}/jack_rec
%{_bindir}/jack_test
%{_bindir}/jack_cpu
%{_bindir}/jack_server_control
%{_bindir}/jack_thru
%{_bindir}/jack_cpu_load
%{_bindir}/jack_load
%{_bindir}/jack_unload
%{_bindir}/jack_monitor_client
%{_bindir}/jack_connect
%{_bindir}/jack_disconnect
%{_bindir}/jack_lsp
%{_bindir}/jack_freewheel
%{_bindir}/jack_evmon
%{_bindir}/jack_alias
%{_bindir}/alsa_in
%{_bindir}/alsa_out
%{_bindir}/jack_netsource
%{_bindir}/jack_iodelay
%{_bindir}/jack_latent_client
%{_bindir}/jack_midi_dump
%{_bindir}/jack_session_notify
%{_bindir}/jack_midi_latency_test
%{_bindir}/jack_net_master
%{_bindir}/jack_net_slave
%if %enable_dbus
%{_bindir}/jackdbus
%{_datadir}/dbus-1/services/org.jackaudio.service
%{_bindir}/jack_control
%if %enable_classic
%{_bindir}/jackd
%endif
%else
%{_bindir}/jackd
%endif
%dir %{_libdir}/jack
%{_libdir}/jack/*.so

%files -n %{libname}
%{_libdir}/libjack.so.%{major}*
%{_libdir}/libjacknet.so.%{major}*

%files -n %{libserver}
%{_libdir}/libjackserver.so.%{major}*

%files -n %{develname}
%doc %{_datadir}/jack-audio-connection-kit/reference/html
%{_includedir}/jack
%{_libdir}/lib*.so
%dir %{_libdir}/jack
%{_libdir}/pkgconfig/jack.pc

%files example-clients
%{_bindir}/jack_metro
%{_bindir}/jack_midiseq
%{_bindir}/jack_midisine
%{_bindir}/jack_multiple_metro
%{_bindir}/jack_samplerate
%{_bindir}/jack_showtime
%{_bindir}/jack_simple_client
%{_bindir}/jack_transport
%{_bindir}/jack_wait
%{_bindir}/jack_simple_session_client



%changelog
* Thu Dec 22 2011 Frank Kober <emuse@mandriva.org> 1.9.8-1
+ Revision: 744360
- new version 1.9.8
  o doxygen path patch removed
  o doxygen path fixed in spec
  o file list adjusted
  o celt codec works again
  o ffado still disabled
  o explicit LDFLAGS removed (caused undefined symbols)

* Mon Dec 12 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.9.7-4
+ Revision: 740535
- rebuild
- split out server lib
- cleaned up spec
- removed mkrel, BuildRoot, clean section, defattr
- removed pre200900 scriptlets
- removed unneeded reqs/provides in devel pkg
- removed dep loop main<>lib
- converted BRs to pkgconfig provides

* Sat Sep 17 2011 Frank Kober <emuse@mandriva.org> 1.9.7-3
+ Revision: 700105
- Still disable firewire, fixed typo
- force single CPU for waf configure

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - pass %%ldflags

* Thu May 26 2011 Frank Kober <emuse@mandriva.org> 1.9.7-2
+ Revision: 679209
- firewire backend disabled until ffado crash gets fixed

* Sat Apr 30 2011 Frank Kober <emuse@mandriva.org> 1.9.7-1
+ Revision: 661057
- new version 1.9.7
  o file list adjusted
  o old wscript patch replaced by setting odd libdir variable
  o new patch made to fix doxygen doc build path

* Sun Oct 10 2010 Frank Kober <emuse@mandriva.org> 1.9.6-1mdv2011.0
+ Revision: 584674
- new version 1.9.6
  o add manpages
  o drop old patch0
  o add new patch0 fixing some issues in wscript

* Fri Aug 06 2010 Funda Wang <fwang@mandriva.org> 1.9.5-7mdv2011.0
+ Revision: 566617
- jackit does not like latest celt now :(

* Thu Apr 29 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.9.5-6mdv2010.1
+ Revision: 540829
- rebuild so that shared libraries are properly stripped again

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.9.5-5mdv2010.1
+ Revision: 540307
- rebuild so that shared libraries are properly stripped again

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 1.9.5-4mdv2010.1
+ Revision: 539579
- rebuild so that shared libraries are properly stripped again

* Sat Apr 17 2010 Frank Kober <emuse@mandriva.org> 1.9.5-3mdv2010.1
+ Revision: 535819
- add git patch from N. Arnaudov providing start failure handling

* Sat Feb 27 2010 Frank Kober <emuse@mandriva.org> 1.9.5-2mdv2010.1
+ Revision: 512474
-replace alsa-lib-devel BR by libalsa-devel
-add ffado firewire backend to BR

* Mon Feb 22 2010 Frank Kober <emuse@mandriva.org> 1.9.5-1mdv2010.1
+ Revision: 509856
- BR adjusted
- switch to Jack2 branch enabling multiprocessor and D-Bus support for upcoming LADI Session Handler

  + Stéphane Téletchéa <steletch@mandriva.org>
    - Add missing archive
    - Fix library path

* Wed Jan 27 2010 Götz Waschk <waschk@mandriva.org> 0.118.0-2mdv2010.1
+ Revision: 497123
- rebuild for new celt

* Sat Jan 16 2010 Jérôme Brenier <incubusss@mandriva.org> 0.118.0-1mdv2010.1
+ Revision: 492372
- new version 0.118.0
- remove old and unused Patch0
- fix files list

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.116.2-3mdv2010.0
+ Revision: 425392
- rebuild

* Thu Feb 26 2009 Götz Waschk <waschk@mandriva.org> 0.116.2-2mdv2009.1
+ Revision: 345150
- rebuild for new libreadline

* Fri Feb 13 2009 Emmanuel Andry <eandry@mandriva.org> 0.116.2-1mdv2009.1
+ Revision: 340163
- New version 0.116.2
- protect major

* Mon Dec 22 2008 Götz Waschk <waschk@mandriva.org> 0.116.1-2mdv2009.1
+ Revision: 317512
- fix devel deps

* Mon Dec 08 2008 Adam Williamson <awilliamson@mandriva.org> 0.116.1-1mdv2009.1
+ Revision: 311862
- buildrequires fltk-devel not libfltk-devel
- buildrequires libsamplerate-devel (for netjack)
- adjust file list for new version (now includes netjack)
- buildrequires celt-devel
- small cleanups
- new license policy, correct license
- new release 0.116.1
- new devel policy

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 0.109.2-2.1092.1mdv2009.0
+ Revision: 264712
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 05 2008 trem <trem@mandriva.org> 0.109.2-0.1092.1mdv2009.0
+ Revision: 201215
- update to 109.2

  + Thierry Vignaud <tv@mandriva.org>
    - fix no-buildroot-tag
    - kill re-definition of %%buildroot on Pixel's request

* Thu Dec 13 2007 David Walluck <walluck@mandriva.org> 0.107.7-0.1070.1mdv2008.1
+ Revision: 119512
- add sources
- 107.7 (SVN 1070)

* Sat Aug 18 2007 Austin Acton <austin@mandriva.org> 0.107.2-0.1051.1mdv2008.0
+ Revision: 65413
- new svn checkout for extreme awesomeness (and fewer segfaults)

* Fri Aug 17 2007 Thierry Vignaud <tv@mandriva.org> 0.103.0-0.20070314.3mdv2008.0
+ Revision: 64766
- rebuild


* Thu Mar 15 2007 Olivier Blin <oblin@mandriva.com> 0.103.0-0.20070314.2mdv2007.1
+ Revision: 144601
- move API doc in devel package

* Wed Mar 14 2007 Austin Acton <austin@mandriva.org> 0.103.0-0.20070314.1mdv2007.1
+ Revision: 143845
- new version with midi support
- don't build against portaudio for now
- Import jackit

* Sun May 28 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.102.5-0.20060518.2mdk
- patch1: fix build on x86-64

* Fri May 19 2006 Austin Acton <austin@mandriva.org> 0.102.5-0.20060518.1mdk
- update to 0.102.5 for MIDI support

* Fri May 05 2006 Austin Acton <austin@mandriva.org> 0.101.1-0.20060504.1mdk
- cvs now includes freebob directly
- mkrel

* Fri Feb 17 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.100.9-0.20060111.2mdk
- fix buildrequires

* Wed Jan 11 2006 Austin Acton <austin@mandriva.org> 0.100.9-0.20060111.1mdk
- snapshot
- add freebob driver

* Sat Dec 31 2005 Mandriva Linux Team <http://www.mandrivaexpert.com/> 0.100.1-0.20050702.2mdk
- Rebuild

* Sun Jul 03 2005 Austin Acton <austin@mandriva.org> 0.100.1-0.20050702.1mdk
- cvs snapshot to get ieee16883 driver
- relax requires

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.99.0-2mdk
- rebuild for new readline

* Sat Dec 18 2004 Laurent Culioli <laurent@mandrake.org> 0.99.0-1mdk
- 0.99.0

* Wed Jun 16 2004 Laurent Culioli <laurent@mandrake.org> 0.98.1-1mdk
- 0.98.1

* Thu Apr 22 2004 Laurent Culioli <laurent@mandrake.org> 0.98.0-1mdk
- 0.98.0

