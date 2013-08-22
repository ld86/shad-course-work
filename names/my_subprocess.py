#!/usr/bin/python3.2
import os
import time
import fcntl
import subprocess

class IPopen(subprocess.Popen):
    def __init__(self, *args, **kwargs):
        """Construct interactive Popen."""
        keyword_args = {
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE}
        keyword_args.update(kwargs)
        subprocess.Popen.__init__(self, *args, **keyword_args)
        # Make stderr and stdout non-blocking.
        for outfile in (self.stdout, self.stderr):
            if outfile is not None:
                fd = outfile.fileno()
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def correspond(self, text, sleep=0.0001):
        """Communicate with the child process without closing stdin."""
        self.stdin.write(bytes(text + '\n', 'utf-8'))
        self.stdin.flush()
        str_buffer = ''
        while not str_buffer:
            try:
                for bin_str in self.stdout:
                    str_buffer += bin_str.decode('utf-8')
            except IOError:
                time.sleep(sleep) 
        return str_buffer

