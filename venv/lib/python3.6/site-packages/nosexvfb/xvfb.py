#-*- coding: utf-8 -*-

import logging

from nose.plugins import Plugin
from xvfbwrapper import Xvfb as XvfbWrapper

logger = logging.getLogger('nose.plugins.xvfb')


class Xvfb(Plugin):
    def options(self, parser, env):
        super(Xvfb, self).options(parser, env)
        parser.add_option("--with-xvfb-options", action="store",
            dest="xvfb_options",
            default=env.get("NOSE_WITH_XVFB_OPTIONS"),
            help="Options to pass to Xvfb. Comma delimited with "
            "equals as separators if necessary. "
            "E.g. \"extension=SELINUX, once\". Currently, there is no "
            "way to provide options that begin with a +. This is a limitation "
            "in xvfbwrapper. Repetition is not allowed. [NOSE_WITH_XVFB_OPTIONS]")

    def configure(self, options, noseconfig):
        super(Xvfb, self).configure(options, noseconfig)
        self.xvfb_options = {}
        if options.xvfb_options:
            opts = [x.strip() for x in options.xvfb_options.split(",")]
            for item in opts:
                key, sign, value = item.partition("=")
                if not value:
                    value = ''
                self.xvfb_options[key] = value

    def begin(self):
        logger.info('Starting xvfb virtual display 1024x768 with %s' % self.xvfb_options)
        self.vdisplay = XvfbWrapper(width=1024, height=768, **self.xvfb_options)
        self.vdisplay.start()

    def finalize(self, result):
        logger.info('Stopping xvfb virtual display')
        self.vdisplay.stop()
