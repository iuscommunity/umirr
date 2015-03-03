import falcon
from .config import settings, mirrors
from .resources import MainResource, SettingsResource, MirrorsResource, \
    MirrorListResource


application = falcon.API()

# home page
main_resource = MainResource()
application.add_route('/', main_resource)

# expose application settings
settings_resource = SettingsResource(settings)
application.add_route('/settings', settings_resource)

# expose mirror data
mirrors_resource = MirrorsResource(settings, mirrors)
application.add_route('/mirrors', mirrors_resource)

# generate the list of mirrors
mirrorlist_resource = MirrorListResource(settings, mirrors)
application.add_route('/mirrorlist', mirrorlist_resource)
