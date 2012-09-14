#
# Conditional build:
%bcond_without	numa	# disable NUMA support
#
Summary:	Balancing of IRQs between multiple CPUs
Summary(pl.UTF-8):	Rozdzielanie IRQ pomiędzy wiele procesorów
Name:		irqbalance
Version:	1.0.4
Release:	2
License:	GPL v2
Group:		Daemons
Source0:	http://irqbalance.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	f7ca283c46331db73f27e686a643dcfb
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
URL:		http://code.google.com/p/irqbalance/
BuildRequires:	glib2-devel >= 1:2.28
# due to -fpie
BuildRequires:	gcc >= 5:3.4
BuildRequires:	libcap-ng-devel
%{?with_numa:BuildRequires:	numactl-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.647
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	glib2 >= 1:2.28
Requires:	rc-scripts
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%description -l pl.UTF-8
Narzędzie do rozdzielania przerwań IRQ pomiędzy wiele procesorów w
celu zwiększenia wydajności systemu.

%prep
%setup -q

%build
%configure \
	%{!?with_numa:--disable-numa} \
	--with-libcap-ng

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add irqbalance
%service irqbalance restart "irqbalance daemon"
%systemd_post irqbalance.service

%preun
if [ "$1" = "0" ]; then
	%service irqbalance stop
	/sbin/chkconfig --del irqbalance
fi
%systemd_preun irqbalance.service

%postun
%systemd_reload

%triggerpostun -- irqbalance < 0.55-4
%systemd_trigger irqbalance.service

%files
%defattr(644,root,root,755)
%doc AUTHORS
%attr(755,root,root) %{_sbindir}/irqbalance
%attr(754,root,root) /etc/rc.d/init.d/irqbalance
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/irqbalance.service
%{_mandir}/man1/irqbalance.1*
