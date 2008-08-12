from dojango.conf import settings # using the app-specific settings

class Config:
    
    profile = None
    version = None
    config = None
    dojo_base_url = None
    
    def __init__(self, profile=settings.DOJO_PROFILE, version=settings.DOJO_VERSION):
        self.profile = profile
        self.version = version
        self.config = self._get_config()
        self.dojo_base_url = self._get_dojo_url()
        
    def _get_config(self):
        '''Getting a config dictionary using the giving profile. See the profile list in conf/settings.py'''
        try:
            config = settings.DOJO_PROFILES[self.profile]
            return config
        except KeyError:
            pass
        return None
    
    def _get_dojo_url(self):
        '''Getting the dojo-base-path dependend on the profile and the version'''
        # the configuration of this profile (e.g. use crossdomain, uncompressed version, ....)
        # if no version is set you are free to use your own
        if self.config == None or not self.version in self.config.get('versions', (self.version)):
            return None
        # and putting the complete url together
        return "%(base)s/%(version)s" % {"base":self.config.get('base_url', ''), 
            "version":self.version}
        
    def get_context_dict(self):
        ret = {}
        # all constants must be uppercase
        for key in self.config:
            ret[key.upper()] = self.config[key]
        ret['IS_LOCAL_BUILD'] = self.config.get("is_local_build", False)
        ret['IS_LOCAL'] = self.config.get("is_local", False)
        ret['UNCOMPRESSED'] = self.config.get("uncompressed", False)
        ret['USE_GFX'] = self.config.get("use_gfx", False)
        ret['VERSION'] = self.version
        # preparing all dojo related urls here
        ret['THEME_CSS_URL'] = self.theme_css_url()
        ret['THEME'] = settings.DOJO_THEME
        ret['BASE_MEDIA_URL'] = settings.BASE_MEDIA_URL
        ret['DOJO_BASE_PATH'] = self.dojo_base_path()
        ret['DOJO_URL'] = self.dojo_url()
        ret['DIJIT_URL'] = self.dijit_url()
        ret['DOJOX_URL'] = self.dojox_url()
        ret['DOJO_SRC_FILE'] = self.dojo_src_file()
        ret['DOJANGO_SRC_FILE'] = self.dojango_src_file()
        ret['DEBUG'] = settings.DOJO_DEBUG
        return ret
    
    def dojo_src_file(self):
        '''Get the main dojo javascript file
        Look in conf/settings.py for available profiles.'''
        # set some special cases concerning the configuration
        uncompressed_str = ""
        gfx_str = ""
        xd_str = ""
        if self.config.get('uncompressed', False):
            uncompressed_str = ".uncompressed.js"
        if self.config.get('use_gfx', False):
            gfx_str = "gfx-"
        if self.config.get('use_xd', False):
            xd_str = ".xd"
        return "%(path)s/dojo/%(gfx)sdojo%(xd)s.js%(uncompressed)s" % {"path":self.dojo_base_url,
            "xd": xd_str,
            "gfx": gfx_str,
            "uncompressed": uncompressed_str}
    
    def dojango_src_file(self):
        '''Getting the main javascript profile file url of this awesome app :-)
        You need to include this within your html to achieve the advantages
        of this app.
        TODO: Listing some advantages!
        '''
        return "%s/dojango/dojango.js" % settings.BASE_MEDIA_URL

    def dojo_url(self):
        '''Like the "dojango_dojo_src_file" templatetag, but just returning the base path
        of dojo.'''
        return "%s/dojo" % self.dojo_base_url
    
    def dijit_url(self):
        '''Like the "dojango_dojo_src_file" templatetag, but just returning the base path
        of dijit.'''
        return "%s/dijit" % self.dojo_base_url
    
    def dojox_url(self):
        '''Like the "dojango_dojo_src_file" templatetag, but just returning the base path
        of dojox.'''
        return "%s/dojox" % self.dojo_base_url
    
    # TODO: we should add the dojoc path, if we can do that
    
    def dojo_base_path(self):
        '''djConfig.baseUrl can be used to mix an external xd-build with some local dojo modules.
        If we use an external build it must be '/' and for a local version, we just have to set the
        path to the dojo path.
        '''
        base_url = "/"
        if self.config.get('is_local', False):
            base_url = "%s/dojo/" % self.dojo_base_url # last slash is needed
        return base_url
    
    def theme_css_url(self):
        '''Like the "dojango_dojo_src_file" templatetag, but returning the theme css path. It uses the
        DOJO_THEME and DOJO_THEME_PATH settings to determine the right path.'''
        if settings.DOJO_THEME_URL:
            # if an own them is used, the theme must be located in themename/themename.css
            return settings.DOJO_THEME_URL + "/%s/%s.css" % (settings.DOJO_THEME, settings.DOJO_THEME)
        return "%s/dijit/themes/%s/%s.css" % (self.dojo_base_url, settings.DOJO_THEME, settings.DOJO_THEME)
    
    def theme(self):
        return settings.DOJO_THEME