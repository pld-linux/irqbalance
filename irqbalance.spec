Summary:	Balancing of IRQs between multiple CPUs
Summary(pl):	Rozdzielanie IRQ pomiêdzy wiele procesorów
Name:		irqbalance
Version:	0.10
Release:	1
License:	OSL v1.1
Group:		Applications/System
Source0:	http://people.redhat.com/arjanv/irqbalance/%{name}-%{version}.tar.gz
# Source0-md5:	aa22849eb4f3735c983adc9612f65003
Source1:	%{name}.init
Patch0:		%{name}-opt.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Balancing of IRQs between multiple CPUs.

%description -l pl
Narzêdzie do rozdzielania przerwañ IRQ pomiêdzy wiele procesorów.

%prep
%setup -q -n %{name}
%patch -p1

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
if [ -f /var/lock/subsys/irqbalance ]; then
        /etc/rc.d/init.d/irqbalance restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/irqbalance start\" to start irqbalance daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/irqbalance ]; then
                /etc/rc.d/init.d/irqbalance stop 1>&2
        fi
        /sbin/chkconfig --del irqbalance
fi

%files
%defattr(644,root,root,755)
%doc Changelog TODO
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man1/*
%attr(754,root,root) /etc/rc.d/init.d/irqbalance
