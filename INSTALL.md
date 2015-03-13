# Setup

## Repo

RPMs are available via [copr](https://copr.fedoraproject.org/coprs/cgtx/umirr/).

Repo configuration:
* [EL7](https://copr.fedoraproject.org/coprs/cgtx/umirr/repo/epel-7/cgtx-umirr-epel-7.repo)
* [Fedora 21](https://copr.fedoraproject.org/coprs/cgtx/umirr/repo/fedora-21/cgtx-umirr-fedora-21.repo)
* [Fedora 22](https://copr.fedoraproject.org/coprs/cgtx/umirr/repo/fedora-22/cgtx-umirr-fedora-22.repo)

Please note, the EL7 repo contains a few additional RPMs besides umirr.  These are currently necessary to run umirr, but should be removed at some point in the future.

* python-six
    * stock version is missing `six.PY2`
    * [Red Hat bug](https://bugzilla.redhat.com/show_bug.cgi?id=1185409)
* python-falcon
    * request Fedora maintainer to create a branch for EPEL7
    * python-six bug must be resolved first
* GeoIP
    * stock version is missing IPv6 data
    * [Red Hat bug](https://bugzilla.redhat.com/show_bug.cgi?id=1201857)

The RPM for umirr has gunicorn and nginx as dependencies.  I'm sure that other WSGI servers or webservers can work, but I have only used these so far.  If you want to rebuild the RPM without those dependencies, modify the [spec file](contrib/umirr.spec) and change the macros `with_nginx` and/or `with_gunicorn` from 1 to 0.

## Configuration

Everything about umirr is controlled in two yaml files.  Customize these files to your needs.  Changes to either file requires restarting the umirr service.

settings.yaml:
* `/etc/umirr/settings.yaml` or `./settings.yaml`
* [example](example-configs/settings.yaml)

mirrors.yaml:
* `/etc/umirr/mirrors.yaml` or `./mirrors.yaml`
* [example](example-configs/mirrors.yaml)

## Services

To run umirr, you can use a [regular service](http://www.freedesktop.org/software/systemd/man/systemd.service.html) or an [instantiated service](http://0pointer.de/blog/projects/instances.html).

Regular:
```
systemctl enable umirr.service
systemctl start umirr.service
```

Instantiated:
```
systemctl enable umirr@1.service
systemctl enable umirr@2.service
systemctl start umirr@1.service
systemctl start umirr@2.service
```

Instantiated services give you an easy option for scaling out the application.  Just ensure that you adjust your [nginx pool configuration](contrib/umirr.nginx#L9-L16) to point to the correct socket(s).
