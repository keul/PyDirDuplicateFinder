# -*- coding: utf-8 -*-

try:
    import readline
    READLINE_AVAILABLE = True
except ImportError:
    READLINE_AVAILABLE = False

def _input_default(prompt, default):
   def startup_hook():
       readline.insert_text(default)
   readline.set_startup_hook(startup_hook)
   try:
       return raw_input(prompt)
   finally:
       readline.set_startup_hook(None)

def raw_input_defaulted(msg, default=''):
    """A raw_input implementation with default value already specified
    Is based on readline module, avaiable only on UNIX systems; if the readline if not found
    no default is given.
    """
    if not default or not READLINE_AVAILABLE:
        return raw_input(msg)
    return _input_default(msg, default=default)