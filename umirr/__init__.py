import falcon
from .config import settings, mirrors
from .resources import MainResource, MirrorsResource, MirrorListResource


application = falcon.API()

# main page
main_settings = settings.get('main')
main_resource = MainResource()
application.add_route(main_settings.get('route'), main_resource)

# expose mirror data
mirrors_settings = settings.get('mirrors')
mirrors_resource = MirrorsResource(mirrors_settings, mirrors)
application.add_route(mirrors_settings.get('route'), mirrors_resource)

# generate the list of mirrors
mirrorlist_settings = settings.get('mirrorlist')
mirrorlist_resource = MirrorListResource(mirrorlist_settings, mirrors)
application.add_route(mirrorlist_settings.get('route'), mirrorlist_resource)
