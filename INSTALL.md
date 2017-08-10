# Setup

## Repo

RPMs are available via [copr](https://copr.fedoraproject.org/coprs/carlwgeorge/umirr/).

Repo configuration:
* [EL7](https://copr.fedoraproject.org/coprs/carlwgeorge/umirr/repo/epel-7/carlwgeorge-umirr-epel-7.repo)

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
