%define debug_package %{nil}
%define pkgname {{pkgname}}
%define version {{version}}
%define bindir {{bindir}}
%define etcdir {{etcdir}}
%define iteration {{iteration}}
%define dist {{dist}}
%define manage_conf {{manage_conf}}

Name: %{pkgname}
Version: %{version}
Release: %{iteration}.%{dist}
Summary: NATS Streaming Server
License: MIT
URL: https://nats.io/
Group: System Tools
Source0: %{pkgname}-%{version}-linux-amd64.tgz
Packager: R.I.Pienaar <rip@devco.net>
BuildRoot: %{_tmppath}/%{pkgname}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
NATS Streaming is an extremely performant, lightweight reliable streaming platform built on NATS.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install
rm -rf %{buildroot}
%{__install} -d -m0755  %{buildroot}/etc/sysconfig
%{__install} -d -m0755  %{buildroot}/etc/init.d
%{__install} -d -m0755  %{buildroot}/etc/logrotate.d
%{__install} -d -m0755  %{buildroot}%{bindir}
%{__install} -d -m0755  %{buildroot}%{etcdir}
%{__install} -d -m0755  %{buildroot}/var/log
%{__install} -m0755 dist/server.init %{buildroot}/etc/init.d/%{pkgname}
%{__install} -m0644 dist/server.sysconfig %{buildroot}/etc/sysconfig/%{pkgname}
%{__install} -m0755 dist/nats-streaming-server-logrotate %{buildroot}/etc/logrotate.d/%{pkgname}
%if 0%{?manage_conf} > 0
%{__install} -m0640 dist/server.conf %{buildroot}%{etcdir}/%{pkgname}.conf
%endif
%{__install} -m0755 nats-streaming-server %{buildroot}%{bindir}/%{pkgname}

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add %{pkgname} || :

%postun
if [ "$1" -ge 1 ]; then
  /sbin/service %{pkgname}-server condrestart &>/dev/null || :
fi

%preun
if [ "$1" = 0 ] ; then
  /sbin/service %{pkgname}-server stop > /dev/null 2>&1
  /sbin/chkconfig --del %{pkgname}-server || :
fi

%files
%if 0%{?manage_conf} > 0
%config(noreplace)%{etcdir}/%{pkgname}.conf
%endif
%{bindir}/%{pkgname}
/etc/logrotate.d/%{pkgname}
/etc/init.d/%{pkgname}
/etc/sysconfig/%{pkgname}

%changelog
* Tue Dec 05 2017 R.I.Pienaar <rip@devco.net>
- Initial Release
