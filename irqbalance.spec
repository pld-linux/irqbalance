Summary:	Balancing of IRQs between multiple CPUs
Summary(pl):	Rozdzielanie IRQ pomiêdzy wiele procesorów
Name:		irqbalance
Version:	0.08
Release:	1
License:	OSL v1.1
Group:		Applications/System
Source0:	http://people.redhat.com/arjanv/irqbalance/%{name}-%{version}.tar.gz
# Source0-md5:	da39e9ff770b01329796ad8258e972d6
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
install -d $RPM_BUILD_ROOT%{_sbindir}

install %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changelog TODO
%attr(755,root,root) %{_sbindir}/*
