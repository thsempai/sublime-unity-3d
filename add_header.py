# -*- conding: utf-8 -*-

import sublime
import sublime_plugin
import getpass
import os
import re
import datetime

K_TAG_USER_NAME = 'author'
K_TAG_FILE_NAME = 'name'
K_TAG_MODIFIED = 'modified'
K_TAG_PREFIX = '// *'
K_TAG_REGEX = '// \* .*:'
K_COMMENT_DELIMITER_REGEX = '// \*\*+'
K_NCHAR = 14


class AddheaderCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        if not self.__check_hearder(edit):

            file_name = self.__get_file_name()
            user_name = unicode(getpass.getuser(), errors='replace')
            header = self.__make_header(user_name, file_name)
            self.view.insert(edit, 0, header)

    def __check_hearder(self, edit):

        ok = False
        lines = self.view.lines(sublime.Region(0, self.view.size()))
        for line in lines:

            line_str = self.view.substr(line)

            if ok:
                regex = re.compile(K_TAG_REGEX)
                regex_end = re.compile(K_COMMENT_DELIMITER_REGEX)

                if regex.match(line_str):
                    line_str = line_str[len(regex_str)-1:]
                    line_str = line_str.split(':')
                    tag = line_str[0].strip()
                    value = line_str[1].strip()

                    if tag == K_TAG_FILE_NAME:

                        file_name = self.__get_file_name()
                        tag = '%s:' % tag
                        tag = tag + ' ' * (K_NCHAR - len(tag))
                        text = '%s %s %s' % (K_TAG_PREFIX, tag, file_name)

                        self.view.replace(edit, line, text)

                    elif tag == K_TAG_MODIFIED:

                        modfied = datetime.date.today()
                        tag = '%s:' % tag
                        tag = tag + ' ' * (K_NCHAR - len(tag))
                        text = '%s %s %s' % (K_TAG_PREFIX, tag, modfied)

                        self.view.replace(edit, line, text)

                elif regex_end.match(line_str):

                    break

            else:
                regex_str = '// \**'
                regex = re.compile(K_COMMENT_DELIMITER_REGEX)

                if regex.match(line_str):
                    ok = True

        return ok

    def __make_header(self, user_name, file_name):

        header = u'// ***************************************\n'
        header += u'// *\n'
        header += u'// * name:          %s\n' % file_name
        header += u'// * author:        %s\n' % user_name
        header += u'// * project:       -\n'
        header += u'// * created:       %s\n' % datetime.date.today()
        header += u'// * modified:      %s\n' % datetime.date.today()
        header += u'// * description:   -\n'
        header += u'// *\n'
        header += u'// ***************************************\n'

        return header

    def __get_file_name(self):

        file_name = self.view.file_name()

        if file_name:
            file_name = os.path.basename(self.view.file_name())
            file_name = os.path.splitext(file_name)[0]
        else:
            file_name = '-'

        return file_name
