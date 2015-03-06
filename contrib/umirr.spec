# Umirr doesn't technically require nginx, it just requires a webserver that
# has geoip intergration and can set the X-Forwarded-For header.  Nginx has
# those things.
%global with_nginx 1

# Umirr doesn't technically require gunicorn.  It is a standard WSGI
# application.  Gunicorn is simple, so use that.  The user/group/home macros
# are used for the gunicorn process.
%global with_gunicorn 1
%global umirr_user umirr
%global umirr_group umirr
%global umirr_home /run/umirr


Name: umirr
Version: 0.3
Release: 1%{?dist}
Summary: Micro mirror service
License: ASL 2.0
URL: https://github.com/cgtx/umirr
Source0: https://github.com/cgtx/umirr/archive/%{version}.tar.gz
Source1: umirr.service
Source2: umirr.socket
Source3: umirr.tmpfiles
Source4: umirr.nginx

BuildRequires: python-devel
%if 0%{?with_gunicorn} || 0%{?with_nginx}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

Requires: python-six
Requires: python-falcon
Requires: PyYAML
%if 0%{?with_gunicorn}
Requires: python-gunicorn
%endif
%if 0%{?with_nginx}
Requires: nginx
%endif


%description
Umirr is an application for generating a geographically relative list of
mirrors.  The output is designed to be parsed by the mirrorlist parameter of
yum repo configuration.  It is designed to be as simple as possible.  All
configuration and data is contained in simple yaml files.  The app does require
geoip information to be passed to it via headers.  Fortunately, this is very
easy to do in nginx.


%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python2} setup.py build


%install
%{__python2} setup.py install --optimize 1 --skip-build --root %{buildroot}

install -Dpm 0644 example-configs/settings.yaml %{buildroot}%{_sysconfdir}/umirr/settings.yaml
install -Dpm 0644 example-configs/mirrors.yaml %{buildroot}%{_sysconfdir}/umirr/mirrors.yaml

%if 0%{?with_gunicorn}
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/umirr.service
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/umirr.socket
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_tmpfilesdir}/umirr.conf
%endif

%if 0%{?with_nginx}
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/nginx/conf.d/umirr.conf
%endif


%if 0%{?with_gunicorn}

%pre
getent group %{umirr_group} > /dev/null || groupadd -r %{umirr_group}
getent passwd %{umirr_user} > /dev/null || \
    useradd -r -d %{umirr_home} -g %{umirr_group} \
    -s /sbin/nologin -c "umirr mirror service" %{umirr_user}
exit 0

%post
%systemd_post umirr.service

%preun
%systemd_preun umirr.service

%postun
%systemd_postun umirr.service

%endif # with_gunicorn


%files
%doc README.md
%{python2_sitelib}/umirr
%{python2_sitelib}/umirr-%{version}-py?.?.egg-info
%{_sysconfdir}/umirr
%config(noreplace) %{_sysconfdir}/umirr/settings.yaml
%config(noreplace) %{_sysconfdir}/umirr/mirrors.yaml
%if 0%{?with_gunicorn}
%{_unitdir}/umirr.service
%{_unitdir}/umirr.socket
%{_tmpfilesdir}/umirr.conf
%endif
%if 0%{?with_nginx}
%config(noreplace) %{_sysconfdir}/nginx/conf.d/umirr.conf
%endif


%changelog
* Fri Mar 06 2015 Carl George <carl.george@rackspace.com> - 0.3-1
- Switch to building against Python 2
- Use default ownership on the socket file
- Mark config files as %%config(noreplace)

* Thu Mar 05 2015 Carl George <carl.george@rackspace.com> - 0.2-2
- Install example configs

* Wed Mar 04 2015 Carl George <carl.george@rackspace.com> - 0.2-1
- Initial package
