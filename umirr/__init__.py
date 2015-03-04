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
mirrors_settings = settings.get('mirrors')
mirrors_resource = MirrorsResource(mirrors_settings, mirrors)
application.add_route('/mirrors', mirrors_resource)

# generate the list of mirrors
mirrorlist_settings = settings.get('mirrorlist')
mirrorlist_resource = MirrorListResource(mirrorlist_settings, mirrors)
application.add_route('/mirrorlist', mirrorlist_resource)
