Summary:	Balancing of IRQs between multiple CPUs
Summary(pl):	Rozdzielanie IRQ pomiêdzy wiele procesorów
Name:		irqbalance
Version:	0.06
Release:	1
License:	OSL v1.1
Group:		Applications/System
Source0:	http://people.redhat.com/arjanv/irqbalance/%{name}-%{version}.tar.gz
# Source0-md5:	4dcdc15c7583fb6e82e498178f405208
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
	OPT="%{rpmcflags}"

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
