#define debug_package          {nil}

# D-Bus support enabled by default, set "--with nodbus" to disable
%define enable_dbus 1
# Build classic jackd executable as well
%define enable_classic 1

%define	major 0
%define	libname %mklibname jack %{major}
%define	libnet %mklibname jacknet %{major}
%define	libserver %mklibname jackserver %{major}
%define	devname %mklibname jack -d

Summary:	The Jack Audio Connection Kit 2
Name:		jackit
Version:	1.9.10
Release:	1
# Lib is LGPL, apps are GPL
License:	LGPLv2+ and GPLv2+
Group:		System/Servers
Url:		http://jackaudio.org/
Source0:	https://dl.dropboxusercontent.com/u/28869550/jack-%{version}.tar.bz2
Patch0:		aarch64-sigsegv.patch
Buildrequires:	doxygen
BuildRequires:	fltk-devel
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libavc1394)
BuildRequires:	pkgconfig(libiec61883) >= 1.1.0
#BuildRequires:	pkgconfig(libffado) >= 1.999.17
BuildRequires:	pkgconfig(libraw1394) >= 1.2.1
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sndfile)
%if %enable_dbus
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(expat)
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
work. This means that it focuses on two key areas:	synchronous
execution of all clients, and low latency operation.

%package -n %{libname}
Summary:	Library associated with jack
Group:		System/Libraries
Conflicts:	%{_lib}jack0 < 1.9.8-5

%description -n %{libname}
This package contains a shared library for the Jack Audio Connection Kit.

%package -n %{libnet}
Summary:	Library associated with jack
Group:		System/Libraries
Conflicts:	%{_lib}jack0 < 1.9.8-5

%description -n %{libnet}
This package contains a shared library for the Jack Audio Connection Kit.

%package -n %{libserver}
Summary:	Library associated with jack server, needed for jackd/jackdbus
Group:		System/Libraries
Conflicts:	%{libname} < 1.9.8-1

%description -n %{libserver}
This package contains a shared library for the Jack Audio Connection Kit 
Server.

%package -n %{devname}
Summary:	Header files for Jack
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libnet} = %{version}-%{release}
Requires:	%{libserver} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{mklibname jack 0 -d} < %{version}-%{release}

%description -n %{devname}
Header files for the Jack Audio Connection Kit.

%package    example-clients
Summary:	Example clients that use Jack
Group:		Sound
Requires:	%{name} = %{version}-%{release}

%description    example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%setup -qn jack-%{version}
%apply_patches

%build
%setup_compile_flags
cd jack-%{version}
export CC=%{__cc}
export CXX=%{__cxx}
export cc=%{__cc}
export AR=%{__ar}
export RANLIB=%{__ranlib}

# still disable ffado firewire
./waf configure \
	--prefix=%{_prefix} \
	--libdir=/%_lib \
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

%files -n %{libnet}
%{_libdir}/libjacknet.so.%{major}*

%files -n %{libserver}
%{_libdir}/libjackserver.so.%{major}*

%files -n %{devname}
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
