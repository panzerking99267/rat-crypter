import importlib
import os

def load_plugins(app):
    plugins_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')
    for fname in os.listdir(plugins_dir):
        if fname.endswith('.py') and fname != '__init__.py':
            modname = fname[:-3]
            module = importlib.import_module(f'plugins.{modname}')
            if hasattr(module, "register"):
                module.register(app)