import importlib


class ColabPlugin(object):
    '''
    Class for declaring hotspots
    A hotspot that is called from the html will always pass the context of that
    file.
    A hotspot executed from the code can have any number of parameters.
    '''

    def html_proxy_hotspot(self, context):
        '''
        Example of html proxy, can be called in the html with:

        {% load proxy %}

        {% for proxy_label in proxy %}
          {% plugin_hotspot proxy_label menu %}
        {% endfor %}

        And at the plugin define a a function at plugiName_plugin.py

        def html_proxy_hotspot(self, context):
            return render_to_string('proxy/html_template.html',
                            {'context_variable': python_variable})
        '''
        pass

    def update_profile(self, user, request):
        '''
        Update the profile data, receives the user object and the UpdateView
        object. Returns nothing

        Example of code hotspot, might be called somewhere in the code from:

        from colab.proxy.utils.plugin import plugin_hotspot
        from colab.settings import PROXIED_APPS


        for plugin in PROXIED_APPS:
            plugin_hotspot(plugin, 'update_profile', var1, var2)
        '''
        pass


def plugin_hotspot(plugin_label, hotspot, *args):
    module_name = \
        'colab.proxy.' + plugin_label + '.' + plugin_label + \
        '_plugin'

    module = importlib.import_module(module_name)

    for module_item_name in dir(module):

        module_class = getattr(module, module_item_name)

        if not isinstance(module_class, type):
            continue

        if not issubclass(module_class, ColabPlugin):
            continue

        if module_class != ColabPlugin:
            api = module_class()
            break

    plugin_function = getattr(api, hotspot, None)

    if not plugin_function:
        return None

    return plugin_function(*args)
