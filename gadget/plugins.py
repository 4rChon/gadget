import os
import importlib
import traceback

from gadget import find_modules_in_package

_plugins = []

def load_plugins():
    for moduleName in find_modules_in_package("gadget.plugins"):
        try:
            plugin = importlib.import_module("gadget.plugins.%s" % moduleName)
            
            if hasattr(plugin, "initialize"):
                plugin.initialize()
            else:
                print "Warning: plugin %s does not have an initialize function" % (moduleName,)
        except Exception as e:
            print "Exception raised when loading plugin %s:" % (moduleName,)
            
            traceback.print_exc()
