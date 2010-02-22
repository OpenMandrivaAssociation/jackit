# D-Bus support enabled by default, set flag "--with nodbus" to disable
%define enable_dbus 1
%{?_with_nodbus: %{expand: %%define enable_dbus 0}}

# Build classic jackd executable as well
%define enable_classic 1
%{?_with_noclassic: %{expand: %%define enable_noclassic 0}}

%define     lib_name_orig libjack
%define     lib_major 0
%define     lib_name %mklibname jack %{lib_major} 
%define     lib_name_devel %mklibname jack -d

Summary:    The Jack Audio Connection Kit 2
Name:       jackit
Version:    1.9.5
Release:    %mkrel 1
# Lib is LGPL, apps are GPL
License:    LGPLv2+ and GPLv2+
Group:      System/Servers
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:    http://www.grame.fr/~letz/jack-%{version}.tar.bz2
URL:        http://jackaudio.org/
BuildRequires:  waf
Buildrequires:  alsa-lib-devel
Buildrequires:  libsndfile-devel
BuildRequires:  libsamplerate-devel
BuildRequires:  glib2-devel
BuildRequires:  fltk-devel
Buildrequires:  doxygen
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  libtermcap-devel
BuildRequires:  celt-devel
BuildRequires:  libraw1394-devel >= 1.2.1
BuildRequires:  libavc1394-devel
BuildRequires:  libiec61883-devel >= 1.1.0
BuildRequires:  libfreebob-devel
%if %enable_dbus
BuildRequires:  libdbus-1-devel
BuildRequires:  libexpat-devel
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

%package -n %{lib_name}
Summary:    Library associated with jack kit, needed for jackd/jackdbus
Group:      System/Libraries
Requires:   %{name} >= %{version}

%description -n %{lib_name}
This library is mandatory for the Jack Audio Connection Kit

%package -n %{lib_name_devel}
Summary:    Header files for Jack 
Group:      Development/C
Requires:   %{lib_name} = %{version}
Provides:   %{lib_name_orig}-devel = %{version}-%{release}
Provides:   %{name}-devel = %{version}-%{release}
Obsoletes:  %{mklibname jack 0 -d}
Requires:   pkgconfig
Requires:   libsamplerate-devel
Requires:   celt-devel

%description -n %{lib_name_devel}
Header files for the Jack Audio Connection Kit.

%package    example-clients
Summary:    Example clients that use Jack 
Group:      Sound
Requires:   %{name} = %{version}

%description    example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%setup -q -n jack-%{version}

%build
./waf configure --prefix=%{_prefix} \
      		--libdir=/%{_lib} \
%if %enable_dbus
    --dbus \
%if %enable_classic
    --classic \
%endif
%endif
--doxygen

./waf

%install
rm -rf %buildroot
./waf install --destdir=%{buildroot}

rm -fr %{buildroot}/%{_docdir}

%if %mdkversion < 200900
%post -n %{lib_name} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{lib_name} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc README README_NETJACK2

%{_bindir}/jack_zombie
%{_bindir}/jack_bufsize
%{_bindir}/jack_rec
%{_bindir}/jack_test
%{_bindir}/jack_cpu
%{_bindir}/jack_server_control
%{_bindir}/jack_thru
%{_bindir}/jack_delay
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

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libjack.so.%{lib_major}*
%{_libdir}/libjackserver.so.%{lib_major}*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%doc %{_datadir}/jack-audio-connection-kit/reference/html
%{_includedir}/jack
%{_libdir}/lib*.so
%dir %{_libdir}/jack
%{_libdir}/pkgconfig/jack.pc

%files example-clients
%defattr(-,root,root)
%{_bindir}/jack_metro
%{_bindir}/jack_midiseq
%{_bindir}/jack_midisine
%{_bindir}/jack_multiple_metro
%{_bindir}/jack_samplerate
%{_bindir}/jack_showtime
%{_bindir}/jack_simple_client
%{_bindir}/jack_transport
%{_bindir}/jack_wait
