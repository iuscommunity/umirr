import falcon
from .resources import SettingsResource, MirrorsResource, MirrorListResource
from .config import settings_data, mirrors_data


application = falcon.API()

# simple resources to expose application settings
settings_resource = SettingsResource(settings_data)
application.add_route('/settings', settings_resource)

# simple resource to expose mirror data
mirrors_resource = MirrorsResource(mirrors_data)
application.add_route('/mirrors', mirrors_resource)

# the main resource
mirrorlist_resource = MirrorListResource(settings_data, mirrors_data)
application.add_route('/mirrorlist', mirrorlist_resource)
application.add_route('/', mirrorlist_resource)
