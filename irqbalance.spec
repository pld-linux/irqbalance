Summary:	Balancing of IRQs between multiple CPUs
Name:		irqbalance
Version:	0.06
Release:	1
License:	OSL v1.1
Group:		Applications/System
Source0:	http://people.redhat.com/arjanv/irqbalance/%{name}-%{version}.tar.gz
# Source0-md5:	db5416b6675cae70804d700f42b1a671
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Balancing of IRQs between multiple CPUs.

%prep
%setup -q -n %{name}

%build
%{__make}

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
