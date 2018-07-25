# -*- coding: utf-8 -*-

import unittest
from command import XvfbRun

class TestFunctions(unittest.TestCase):

    def test_multiple_commands(self):
        xvfb_1 = XvfbRun()
        p1 = xvfb_1.run_xcommand_and_return('xclock')

        xvfb_2 = XvfbRun()
        p2 = xvfb_2.run_xcommand_and_return('xclock')

        p1.kill()
        p2.kill()

    def test_single_wait_command(self):
        xvfb = XvfbRun()
        self.assertEqual(
            '0',
            str(xvfb.run_xcommand_and_wait('ls')['exit_code'])
        )

    def test_unknown_wait_command(self):
        xvfb = XvfbRun()
        self.assertEqual(
            '127',
            str(xvfb.run_xcommand_and_wait('unknownwaitcommand')['exit_code'])
        )

    def test_unknown_return_command(self):
        xvfb = XvfbRun()
        self.assertEqual(
            '127',
            str(xvfb.run_xcommand_and_return('unknownreturncommand').wait())
        )

    def test_error_wait_command(self):
        xvfb = XvfbRun()
        self.assertEqual(
            '1',
            str(xvfb.run_xcommand_and_wait('xclock --foo')['exit_code'])
        )

    def test_error_return_command(self):
        xvfb = XvfbRun()
        self.assertEqual(
            '1',
            str(xvfb.run_xcommand_and_return('xclock --foo').wait())
        )

if __name__ == '__main__':
    unittest.main()