import neovim
import os
from subprocess import *

@neovim.plugin
class Plumb(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Plumb')
    def plumb_command(self):
        # Get string from cursor to end of line
        (_, col) = self.nvim.current.window.cursor
        data = self.nvim.current.line[col:]
        # Expand environment variables and '~'
        # TODO: Make plumb do this
        data = os.path.expanduser(data)
        data = os.path.expandvars(data)
        # Run plumb and write errors
        p = Popen(['plumb', data], stdout=PIPE, stderr=PIPE)
        (stdout_data, stderr_data) = p.communicate()
        self.nvim.err_write(stderr_data)
