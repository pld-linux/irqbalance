Summary:	Balancing of IRQs between multiple CPUs
Summary(pl.UTF-8):	Rozdzielanie IRQ pomiędzy wiele procesorów
Name:		irqbalance
Version:	0.55
Release:	5
License:	GPL
Group:		Daemons
Source0:	http://www.irqbalance.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	9f6b314ff1fdc14173abeb40592d4edf
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.service
Patch0:		%{name}-opt.patch
Patch1:		%{name}-pie.patch
Patch2:		%{name}-cputree-parse.patch
URL:		http://www.irqbalance.org/
BuildRequires:	glib2-devel
# due to -fpie
BuildRequires:	gcc >= 5:3.4
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	xorg-util-gccmakedep
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%description -l pl.UTF-8
Narzędzie do rozdzielania przerwań IRQ pomiędzy wiele procesorów
w celu zwiększenia wydajności systemu.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p2

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}%{?debug: debug.c -DDEBUG}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,%{systemdunitdir}} \
	$RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

install %{name} $RPM_BUILD_ROOT%{_sbindir}
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
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/irqbalance
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{systemdunitdir}/irqbalance.service
