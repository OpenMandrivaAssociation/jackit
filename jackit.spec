# To enable real-time sheduling (SCHED_FIFO), rebuild this package adding
# '--with realtime'.  This will require a kernel with the capabilities patch
# and may be a security risk to your system.  Non-root users will be able
# to run jack with real-time priorities by executing 'jackstart'.
%define enable_capabilities 0
%{?_with_realtime: %{expand: %%define enable_capabilities 1}}

%define enable_optimization 0
%{?_with_optimization: %{expand: %%define enable_optimization 1}}

%define svn_rev 1092

%define		lib_name_orig libjack
%define		lib_major 0
%define		lib_name %mklibname jack %{lib_major} 
%define		lib_name_devel%mklibname jack %{lib_major} -d
Summary:	The Jack Audio Connection Kit
Name:		jackit
Version:	0.109.2
Release:	%mkrel 0.%{svn_rev}.1
License:	GPL
Group:		System/Servers
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:	jackit-%{svn_rev}.tar.bz2
Patch1:		jack-driver-inline.patch
URL:		http://jackit.sourceforge.net
Buildrequires:	alsa-lib-devel
Buildrequires:	libsndfile-devel
BuildRequires:  glib2-devel
BuildRequires:	libfltk-devel
Buildrequires:  doxygen
BuildRequires:  readline-devel
BuildRequires:  ncurses-devel
BuildRequires:  libtermcap-devel
%if %enable_capabilities
BuildRequires:	libcap-devel
%endif
BuildRequires:	libraw1394-devel >= 1.2.1
BuildRequires:	libavc1394-devel
BuildRequires:	libiec61883-devel >= 1.1.0
BuildRequires:	libfreebob-devel

%description
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

%package -n	%{lib_name}
Summary:	Library associated with jack kit , needed for jackd
Group:		System/Libraries
Requires:	%{name} >= %{version}

%description -n	%{lib_name}
This library is mandatory for the Jack Audio Connection Kit

%package -n	%{lib_name_devel}
Summary:	Header files for Jack 
Group:		Development/C
Requires:	%{lib_name} = %{version}
Provides:	%{lib_name_orig}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release} 
Requires:	pkgconfig

%description -n	%{lib_name_devel}
Header files for the Jack Audio Connection Kit.

%package	example-clients
Summary:	Example clients that use Jack 
Group:		Sound
Requires:	%{name} = %{version}

%description	example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%setup -q -n jack-audio-connection-kit-%{version}
#%patch1 -p1 -b .x86_64

%build
# ./autogen.sh
%configure2_5x --with-html-dir=%{_docdir} --enable-stripped-jackd --enable-shared --disable-portaudio \
%if %enable_capabilities
	--enable-capabilities \
%endif
%if %enable_optimization
	--enable-optimize
%endif

%make

%install
rm -rf %buildroot
%{makeinstall_std}
rm -fr $RPM_BUILD_ROOT/%{_docdir}
%if ! %enable_capabilities
rm -f %buildroot%_mandir/man1/jackstart.1
%endif

%post -n %{lib_name} -p /sbin/ldconfig
%postun -n %{lib_name} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-,root,root)
%doc AUTHORS TODO
%if %enable_capabilities
%attr(4755,root,root) %{_bindir}/jackstart
%{_mandir}/man1/jackstart.1*
%endif
%{_bindir}/jackd
%dir %{_libdir}/jack
%{_libdir}/jack/jack_alsa.so
%{_libdir}/jack/jack_oss.so
%{_libdir}/jack/jack_dummy.so
%{_libdir}/jack/jack_freebob.so
%{_mandir}/man1/jackd.1*

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libjack.so.*

%files -n %{lib_name_devel}
%defattr(-,root,root)
%doc doc/reference
%{_includedir}/jack
%{_libdir}/lib*.so
#%{_libdir}/lib*.a
%{_libdir}/lib*.la
%dir %{_libdir}/jack
%{_libdir}/jack/*a
%{_libdir}/pkgconfig/jack.pc

%files example-clients
%defattr(-,root,root)
%{_bindir}/jackrec
%{_bindir}/jack_alias
%{_bindir}/jack_bufsize
%{_bindir}/jack_connect
%{_bindir}/jack_disconnect
%{_bindir}/jack_evmon
%{_bindir}/jack_freewheel
%{_bindir}/jack_impulse_grabber
%{_bindir}/jack_lsp
%{_bindir}/jack_metro
%{_bindir}/jack_showtime
%{_bindir}/jack_monitor_client
%{_bindir}/jack_simple_client
%{_bindir}/jack_load
%{_bindir}/jack_unload
%{_bindir}/jack_transport
%{_bindir}/jack_midiseq
%{_bindir}/jack_midisine
%{_libdir}/jack/inprocess.so
%{_libdir}/jack/intime.so
