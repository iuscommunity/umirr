import copy
import json
import six
import falcon
from .utils import calculate_distance


class MainResource:
    ''' Welcome page. '''
    def __init__(self, settings):
        self.settings = settings

    def on_get(self, req, resp):
        resp.content_type = 'text/html'
        resp.body = self.settings.get('body')


class MirrorsResource:
    ''' Expose mirror data. '''
    def __init__(self, settings, mirrors):
        self.mirrors = copy.deepcopy(mirrors)
        if settings.get('hide_owners'):
            for host in self.mirrors:
                del self.mirrors[host]['owner']
                del self.mirrors[host]['contact']

    def on_get(self, req, resp):
        resp.body = json.dumps(self.mirrors, indent=4)


class MirrorListResource:
    ''' Generate list of mirrors relative to requestor's location. '''
    def __init__(self, settings, mirrors):
        self.settings = settings
        self.mirrors = {host: data for host, data in six.iteritems(mirrors)
                        if data.get('enabled')}

    def validate_query(self, req):
        ''' Parse query parameters and validate them. '''
        valid_repos = self.settings.get('repos')
        valid_architectures = self.settings.get('architectures')
        valid_protocols = self.settings.get('protocols')
        repo = req.get_param('repo', required=True)
        if repo not in valid_repos:
            err = '{} is not a valid repo'.format(repo)
            status = falcon.HTTP_404
            raise falcon.HTTPError(status, status, description=err)
        arch = req.get_param('arch', required=True)
        if arch not in valid_architectures:
            err = '{} is not a valid arch'.format(arch)
            status = falcon.HTTP_404
            raise falcon.HTTPError(status, status, description=err)
        protocol = req.get_param('protocol') or valid_protocols[0]
        if protocol not in valid_protocols:
            err = '{} is not a valid protocol'.format(protocol)
            status = falcon.HTTP_404
            raise falcon.HTTPError(status, status, description=err)
        return repo, arch, protocol

    def get_source_info(self, req):
        ip = req.get_header('X-Forwarded-For').split(',')[0]
        src = (req.get_header('X-Forwarded-For-Latitude'),
               req.get_header('X-Forwarded-For-Longitude'))
        if None in src:
            found = False
            fallback = self.settings.get('fallback')
            src = (fallback.get('coordinates').get('latitude'),
                   fallback.get('coordinates').get('longitude'))
            name = (fallback.get('city'),
                    fallback.get('region'),
                    fallback.get('country'))
        else:
            found = True
            name = (req.get_header('X-Forwarded-For-City'),
                    req.get_header('X-Forwarded-For-Region'),
                    req.get_header('X-Forwarded-For-Country'))
        return src, {'ip': ip, 'name': name, 'found': found}

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
            data = self.mirrors.get(host)
            resource = data.get('resources').get(protocol).rstrip('/')
            path = self.settings.get('repos').get(repo)
            url = '{}://{}{}{}'.format(protocol, host, resource, path)
            urls.append(url.replace('@arch@', arch))
        return urls

    def get_title_text(self):
        return ['# mirrorlist generated by umirr', '#']

    def get_source_text(self, src, ip, name, found):
        city, region, country = name
        msg = ['# source ip: {}'.format(ip)]
        if not found:
            msg.append('# status: not in database, using fallback location')
        else:
            msg.append('# status: found in database')
        if city:
            msg.append('# city: {}'.format(city))
        if region:
            msg.append('# region: {}'.format(region))
        if country:
            msg.append('# country: {}'.format(country))
        msg.append('# latitude: {}'.format(src[0]))
        msg.append('# longitude: {}'.format(src[1]))
        msg.append('#')
        return msg

    def get_distance_text(self, distance_data):
        msg = ['# approximate distances in miles:']
        for distance, host in distance_data:
            msg.append('# {:>10,.0f} - {}'.format(distance, host))
        msg.append('#')
        return msg

    def on_get(self, req, resp):
        repo, arch, protocol = self.validate_query(req)
        output = []
        if self.settings.get('show_title'):
            output.extend(self.get_title_text())
        src, info = self.get_source_info(req)
        if self.settings.get('show_source'):
            output.extend(self.get_source_text(src, **info))
        distance_data = self.get_distance_data(protocol, src)
        urls = self.get_urls(distance_data, repo, arch, protocol)
        if self.settings.get('show_distances'):
            output.extend(self.get_distance_text(distance_data))

        output.extend(urls)
        resp.content_type = 'text/plain'
        resp.body = '\n'.join(output)
