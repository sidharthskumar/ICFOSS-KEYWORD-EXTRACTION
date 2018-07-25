# -*- coding: utf-8 -*-

import errno, os, time, tempfile, subprocess, time


class XvfbRun(object):
    servernum = 99
    servernum_lockfile = None
    xvfb_process = None
    xvfb_start_timeout = 3

    xvfb_bin = os.popen('which Xvfb').read()[:-1]
    xvfb_args = [
        '-screen 0',
        '640x480x8',
        '-nolisten tcp'
    ]

    def __init__(self, xvfb_bin=None, xvfb_args=None, xvfb_start_timeout=None):
        if xvfb_bin: self.xvfb_bin = xvfb_bin
        if xvfb_args: self.xvfb_args = xvfb_args
        if xvfb_start_timeout: self.xvfb_start_timeout = xvfb_start_timeout

        # get servernum_lockfile
        path = tempfile.gettempdir()
        servernum_lockfile_fh = None
        while True:
            self.servernum_lockfile = '%s/.X%d-lock' % (path, self.servernum)

            try:
                servernum_lockfile_fh = os.open(self.servernum_lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            except (OSError, IOError):
                time.sleep(.1)
                self.servernum += 1
                continue
            else:
                break

        # run Xvfb
        self.xvfb_process = subprocess.Popen([self.xvfb_bin, ':%d %s' % (self.servernum, ' '.join(self.xvfb_args))])
        xvfb_process_start_time = time.time()

        while True:
            try:
                os.kill(self.xvfb_process.pid, 0)
            except OSError:
                if time.time() - xvfb_process_start_time > self.xvfb_start_timeout:
                    raise Exception(
                        'Unable to start %s. Error was: %s' % (self.xvfb_bin, self.xvfb_process.stderr.read()))
                time.sleep(.1)
            else:
                break

        if self.xvfb_process.poll():
            raise Exception('Unable to start %s. Error was: %s' % (self.xvfb_bin, self.xvfb_process.stdout))

        # write pid to lockfile
        os.write(servernum_lockfile_fh, str(self.xvfb_process.pid).strip())
        os.close(servernum_lockfile_fh)

    def run_xcommand_and_wait(self, command):
        process = subprocess.Popen('DISPLAY=:%d %s' % (self.servernum, command), shell=True, stderr=subprocess.PIPE,
            stdout=subprocess.PIPE)
        return {
            'exit_code': process.wait(),
            'stdout': process.stdout,
            'stderr': process.stderr
        }

    def run_xcommand_and_return(self, command):
        return subprocess.Popen('DISPLAY=:%d %s' % (self.servernum, command), shell=True)

    def close(self):
        del(self)

    def __del__(self):
        if self.xvfb_process:
            self.xvfb_process.kill()

        if os.path.exists(self.servernum_lockfile):
            os.unlink(self.servernum_lockfile)

