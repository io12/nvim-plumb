import neovim
import os
from subprocess import *

# Get the space-separated word at an index in a line
def get_word(line, index):
    # Get lower bound of word
    lo = 0
    for i in range(index, 0, -1):
        if line[i - 1].isspace():
            lo = i
            break
    # Get upper bound of word
    hi = len(line) - 1
    for i in range(index, len(line) - 1):
        if line[i + 1].isspace():
            hi = i
            break
    return line[lo:hi + 1]


@neovim.plugin
class Plumb(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('Plumb')
    def plumb_command(self):
        # Get word under the cursor
        (_, col) = self.nvim.current.window.cursor
        line = self.nvim.current.line
        data = get_word(line, col)
        # Expand environment variables and '~'
        # TODO: Make plumb do this
        data = os.path.expanduser(data)
        data = os.path.expandvars(data)
        # Run plumb and write errors
        p = Popen(['plumb', data], stdout=PIPE, stderr=PIPE)
        (stdout_data, stderr_data) = p.communicate()
        if p.returncode != 0:
            err_msg = '"' + data + '": ' + stderr_data.decode('utf-8')
            self.nvim.err_write(err_msg)
