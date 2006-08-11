Summary:	Balancing of IRQs between multiple CPUs
Summary(pl):	Rozdzielanie IRQ pomiêdzy wiele procesorów
Name:		irqbalance
Version:	0.13
Release:	1
License:	OSL v1.1
Group:		Applications/System
#Source0:	http://people.redhat.com/arjanv/irqbalance/%{name}-%{version}.tar.gz
# Currently no known URL - taken from FC6 src.rpm:
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	837f1d69e9b6ef0a58bbd4cf4e0d7f28
Source1:	%{name}.init
Patch0:		%{name}-opt.patch
Patch1:		%{name}-classes.patch
Patch2:		%{name}-norebalance-zeroints.patch
Patch3:		%{name}-pie.patch
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%description -l pl
Narzêdzie do rozdzielania przerwañ IRQ pomiêdzy wiele procesorów
w celu zwiêkszenia wydajno¶ci systemu.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p2
%patch2 -p2
# For gcc4 ?
#%patch3 -p2

%build
%{__make} %{?debug:debug} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man1,/etc/rc.d/init.d}

install %{name} $RPM_BUILD_ROOT%{_sbindir}
install %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add irqbalance
%service irqbalance restart "irqbalance daemon"

%preun
if [ "$1" = "0" ]; then
	%service irqbalance stop
	/sbin/chkconfig --del irqbalance
fi

%files
%defattr(644,root,root,755)
%doc Changelog TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%attr(754,root,root) /etc/rc.d/init.d/irqbalance
