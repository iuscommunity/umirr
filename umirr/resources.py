import copy
import json
import six
import falcon
from .utils import calculate_distance


class MainResource:
    def on_get(self, req, resp):
        resp.body = '<html><h1>umirr</h1><h2>mirco mirror service</h2></html>'


class SettingsResource:
    ''' Expose application settings. '''
    def __init__(self, settings):
        self.settings = settings

    def on_get(self, req, resp):
        resp.body = json.dumps(self.settings)


class MirrorsResource:
    ''' Expose mirror data. '''
    def __init__(self, settings, mirrors):
        self.mirrors = copy.deepcopy(mirrors)
        if settings.get('mirrors').get('hide_owners'):
            for host in self.mirrors:
                del self.mirrors[host]['owner']
                del self.mirrors[host]['contact']

    def on_get(self, req, resp):
        resp.body = json.dumps(self.mirrors)


class MirrorListResource:
    ''' Generate list of mirrors relative to requestor's location. '''
    def __init__(self, settings, mirrors):
        self.settings = settings
        self.mirrors = {host: data for host, data in six.iteritems(mirrors)
                        if data.get('enabled')}

    def validate(self, req):
        ''' Parse request parameters and validate them. '''
        valid_repos = self.settings.get('repos')
        valid_arches = self.settings.get('arches')
        valid_protocols = self.settings.get('protocols')
        repo = req.get_param('repo', required=True)
        if repo not in valid_repos:
            raise falcon.HTTPInvalidParam('({})'.format(repo), 'repo')
        arch = req.get_param('arch', required=True)
        if arch not in valid_arches:
            raise falcon.HTTPInvalidParam('({})'.format(arch), 'arch')
        protocol = req.get_param('protocol') or valid_protocols[0]
        if protocol not in valid_protocols:
            raise falcon.HTTPInvalidParam('({})'.format(protocol), 'protocol')
        src = (req.get_header('X-Forwarded-For-Latitude'),
               req.get_header('X-Forwarded-For-Longitude'))
        if None in src:
            # coordinates are missing, set the source to center of the U.S.
            src = (39.0, -98.0)
        return repo, arch, protocol, src

    def get_distance_data(self, protocol, src):
        ''' Return a sorted list of (distance, host) tuples. '''
        distance_data = []
        for host, data in six.iteritems(self.mirrors):
            if data.get('resources').get(protocol):
                dst = (data.get('coordinates').get('latitude'),
                       data.get('coordinates').get('longitude'))
                distance = calculate_distance(src, dst)
                distance_data.append((distance, host))
        distance_data.sort()
        return distance_data

    def get_urls(self, distance_data, repo, arch, protocol):
        ''' Generate the url paths from the sorted mirror data. '''
        urls = []
        for distance, host in distance_data:
            data = self.mirrors.get('host')
            resource = data.get('resources').get(protocol)
            path = self.settings.get('repos').get(repo)
            url = '{}://{}/{}/{}/'.format(protocol,
                                          host,
                                          resource.strip('/'),
                                          path.strip('/'))
            urls.append(url.replace('@arch@', arch))
        return urls

    def get_title_text(self):
        return ['# mirrorlist generated by umirr', '#']

    def get_source_text(self, req):
        city = req.get_header('X-Forwarded-For-City')
        region = req.get_header('X-Forwarded-For-Region')
        country = req.get_header('X-Forwarded-For-Country')
        src = req.get_header('X-Forwarded-For').split(',')[0]
        msg = '# ordered for {}, {} {} ({})'.format(city, region, country, src)
        return [msg, '#']

    def on_get(self, req, resp):
        repo, arch, protocol, src = self.validate(req)
        distance_data = self.get_distance_data(protocol, src)
        urls = self.get_urls(distance_data, repo, arch, protocol)

        output = []
        if self.settings.get('mirrorlist').get('show_title'):
            output.extend(self.get_title_text())
        if self.settings.get('mirrorlist').get('show_source'):
            output.extend(self.get_source_text())
        mirrors = self.find_mirrors(repo, arch, protocol, src)
        if self.settings.get('mirrorlist').get('show_distances'):
            msg = ['# approximate distances:']
            urls = []
            for distance, host, url in mirrors:
                msg.append('#    {} - {} miles away'.format(host, distance))
                urls.append(url)
            output.extend(msg)
            output.append('#')
            output.extend(urls)
        else:
            for distance, host, url in mirrors:
                output.append(url)
        resp.content_type = 'text/plain'
        resp.body = '\n'.join(output)
