import pkg_resources


__version__ = pkg_resources.get_distribution("pinax-forums").version
default_app_config = "pinax.forums.apps.AppConfig"
