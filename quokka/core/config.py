import os
import logging
import quokka.core.models as m
import redis as redislib
from flask.config import Config
from quokka.utils import parse_conf_data
from cached_property import cached_property_ttl, cached_property

logger = logging.getLogger()

def load_redis():
    redis_url = os.environ.get('REDIS_URL', None)
    return redislib.Redis() if redis_url is None else redislib.from_url(redis_url)
    

class QuokkaConfig(Config):
    """A Config object for Flask that tries to ger vars from
    database and then from Config itself"""

    _cache_key = None
    _cache = None

    def __init__(self, *args, **kwargs):
        if self._cache_key is None:
            if 'cache_key' in kwargs:
                _cache_key = kwargs.pop('cache_key')
            else:
                _cache_key = self.__class__.__name__
            self._cache_key = _cache_key
        super(QuokkaConfig, self).__init__(*args, **kwargs)        

    @property
    def cache(self):
        if self._cache is None:
            self._cache = load_redis()
        return self._cache

    @cached_property
    def store(self):
        return dict(self)

    @cached_property_ttl(300)
    def all_setings_from_db(self):
        """
        As config reads data from database on every app.config.get(key)/[key]
        This data is cached as a cached_property
        The TTL is fixed in 5 minutes because we can't read it from
        config itself.

        Find a way to set the config parameter in a file
        maybe in a config_setting.ini
        It takes 5 minutes for new values to be available
        and Make it possible to use REDIS as a cache
        """
        try:
            return {
                item.name: item.value
                for item in m.config.Config.objects.get(
                    group='settings'
                ).values
            }
        except Exception as e:
            logger.warning('Error reading all settings from db: %s' % e)
            return {}

    @cached_property_ttl(500)
    def all_settings_from_cache(self):        
        try:
            return {
                name: value
                for name, value in 
                zip(
                    self.get_from_cache('SETTINGS_KEYS'),
                    map(lambda x: self.get_from_cache(x), self.cache.keys("{}:*".format(self._cache_key)))
                )
            }
        except Exception as e:
            logger.warning('Error reading from cache: {}'.format(e))
            return {}

    def set_to_cache(self, key, val):
        _key = self._load_cache_key(key)
        self.cache.set(_key, val)

    def set_all_to_cache(self):
        [self.set_to_cache(k, v) for k, v in self.all_setings_from_db.items()]

    def get_from_db(self, key, default=None):
        return self.all_setings_from_db.get(key, default)

    def get_from_cache(self, key):
        _key = self._load_cache_key(key)
        return self.cache.get(_key)

    def _load_cache_key(self, key):
        return "{}:{}".format(self._cache_key, key)
        
    def __getitem__(self, key):
        return self.get_from_db(key) or dict.__getitem__(self, key)

    def get(self, key, default=None):
        return self.get_from_db(key) or self.store.get(key) or default

    def from_object(self, obj, silent=False):
        try:
            super(QuokkaConfig, self).from_object(obj)
        except ImportError as e:
            if silent:
                return False
            e.message = 'Unable to load configuration obj (%s)' % e.message
            raise

    def from_envvar_namespace(self, namespace='QUOKKA', silent=False):
        try:
            data = {
                key.partition('_')[-1]: parse_conf_data(data)
                for key, data
                in os.environ.items()
                if key.startswith(namespace)
            }
            self.update(data)
        except Exception as e:
            if silent:
                return False
            e.message = 'Unable to load config env namespace (%s)' % e.message
            raise

    def load_quokka_config(self, config=None, mode=None, test=None, **sets):
        self.from_object(config or 'quokka.settings')
        mode = mode or 'test' if test else os.environ.get(
            'QUOKKA_MODE', 'local')
        self.from_object('quokka.%s_settings' % mode, silent=True)
        path = "QUOKKA_SETTINGS" if not test else "QUOKKATEST_SETTINGS"
        self.from_envvar(path, silent=True)
        self.from_envvar_namespace(namespace='QUOKKA', silent=True)
        self.update(sets)
