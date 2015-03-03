import falcon
from .resources import SettingsResource, MirrorsResource, MirrorListResource
from .config import settings, mirrors


application = falcon.API()

# simple resources to expose application settings
settings_resource = SettingsResource(settings)
application.add_route('/settings', settings_resource)

# simple resource to expose mirror data
mirrors_resource = MirrorsResource(mirrors)
application.add_route('/mirrors', mirrors_resource)

# the main resource
mirrorlist_resource = MirrorListResource(settings, mirrors)
application.add_route('/mirrorlist', mirrorlist_resource)
application.add_route('/', mirrorlist_resource)
