#
# Conditional build:
%bcond_without	numa	# disable NUMA support
%bcond_with	systemd	# systemd journal support
#
Summary:	Balancing of IRQs between multiple CPUs
Summary(pl.UTF-8):	Rozdzielanie IRQ pomiędzy wiele procesorów
Name:		irqbalance
Version:	1.1.0
Release:	1
License:	GPL v2
Group:		Daemons
Source0:	https://github.com/Irqbalance/irqbalance/archive/v%{version}.tar.gz
# Source0-md5:	b15d975336080bcac4be0c1752d43cf3
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
URL:		https://github.com/Irqbalance/irqbalance
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	glib2-devel >= 1:2.28
BuildRequires:	libtool
# due to -fpie
BuildRequires:	gcc >= 5:3.4
BuildRequires:	libcap-ng-devel
%{?with_numa:BuildRequires:	numactl-devel}
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.647
%{?with_systemd:BuildRequires:	systemd-devel}
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
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_numa:--disable-numa} \
	--with-libcap-ng \
	%{?with_systemd:--with-systemd}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdunitdir} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}

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
