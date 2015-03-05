# umirr: micro mirror service

Umirr is an application for generating a geographically-relative list of
mirrors for Fedora or RHEL based distributions.  The output is designed to be
parsed by yum, configured via the `mirrorlist` parameter in yum repo files.  It
is designed to be as simple as possible.

## Why create a new mirror service?

All of the existing solutions I could find seemed over complicated.  The only
thing I wanted was an API that returns the mirrorlist text.  I didn't care
about a pretty web portal or managing users.  All the existing solutions
depended on a database backend.  Because of the simplicity of umirr, all
configuration and data is contained in simple yaml files.

## How does it work?

Umirr is a python WSGI application.  To keep things as lean as possible, it
doesn't lookup geoip information itself.  Instead, it relies on HTTP headers
for generating results.  Typically this mean running it behind a webserver
capable of looking up the geoip information for request source IPs.

Required headers:
* `X-Forwarded-For-Latitude`
* `X-Forwarded-For-Longitude`

Optional headers:
* `X-Forwarded-For`
* `X-Forwarded-For-City`
* `X-Forwarded-For-Region`
* `X-Forwarded-For-Country`

## Python requirements

* falcon
* PyYAML
* six

## Deployment requirements

* python WSGI HTTP server
* web server capable of looking up geoip information of request source IPs

## Recommended deployment

* Fedora
* gunicorn
* nginx
