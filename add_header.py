# -*- conding: utf-8 -*-

import sublime
import sublime_plugin
import getpass


class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        user_name = unicode(getpass.getuser(), errors='replace')

        header = u'// ***************************************\n'
        header += u'// *\n'
        header += u'// * name:      monsterMove\n'
        header += u'// * author:    %s\n' % unicode(user_name)
        header += u'// * project:      Get Well Soon\n'
        header += u'// * description:\n'
        header += u'// *\n'
        header += u'// ***************************************\n'

        self.view.insert(edit, 0, header)
