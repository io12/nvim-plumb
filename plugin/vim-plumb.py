import vim
import subprocess

(row, _) = vim.current.window.cursor
data = vim.current.line[row:]
subprocess.call(['plumb', data])
