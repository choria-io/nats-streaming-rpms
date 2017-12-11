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
URL: https://nats.io
Group: System Tools
Packager: R.I.Pienaar <rip@devco.net>
Source0: %{pkgname}-%{version}-linux-amd64.tgz
BuildRoot: %{_tmppath}/%{pkgname}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
NATS Streaming is an extremely performant, lightweight reliable streaming platform built on NATS.

%prep
%setup -q -n %{pkgname}-%{version}

%build

%install
rm -rf %{buildroot}
%{__install} -d -m0755  %{buildroot}/usr/lib/systemd/system
%{__install} -d -m0755  %{buildroot}/etc/logrotate.d
%{__install} -d -m0755  %{buildroot}%{bindir}
%{__install} -d -m0755  %{buildroot}%{etcdir}
%{__install} -d -m0755  %{buildroot}/var/log
%{__install} -m0644 dist/server.service %{buildroot}/usr/lib/systemd/system/%{pkgname}.service
%{__install} -m0644 dist/nats-streaming-server-logrotate %{buildroot}/etc/logrotate.d/%{pkgname}
%if 0%{?manage_conf} > 0
%{__install} -m0640 dist/server.conf %{buildroot}%{etcdir}/%{pkgname}.conf
%endif
%{__install} -m0755 nats-streaming-server %{buildroot}%{bindir}/%{pkgname}

%clean
rm -rf %{buildroot}

%post
if [ $1 -eq 1 ] ; then
  systemctl --no-reload preset %{pkgname} >/dev/null 2>&1 || :
fi

%preun
if [ $1 -eq 0 ] ; then
  systemctl --no-reload disable --now %{pkgname} > /dev/null 2>&1 || :
fi

%files
%if 0%{?manage_conf} > 0
%config(noreplace)%{etcdir}/%{pkgname}.conf
%endif
%{bindir}/%{pkgname}
/etc/logrotate.d/%{pkgname}
/usr/lib/systemd/system/%{pkgname}.service


%changelog
* Tue Dec 05 2017 R.I.Pienaar <rip@devco.net>
- Initial Release
