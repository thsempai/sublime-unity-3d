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

        begin = None
        end = None

        for line in self.view.lines(sublime.Region(0, self.view.size())):

            line_str = self.view.substr(line)
            regex = re.compile(K_COMMENT_DELIMITER_REGEX)
            if regex.match(line_str):
                print line.begin()
                if begin is None:
                    begin = line.begin()
                else:
                    end = line.end()
                    break

        print begin, end
        if end is None:
            return False

        header = self.view.substr(sublime.Region(begin, end)).split('\n')
        print begin, end
        header_text = ''

        for line in header:

            regex = re.compile(K_TAG_REGEX)

            if regex.match(line):
                line = line[len(K_TAG_PREFIX):]
                line = line.split(':')
                tag = line[0].strip()
                value = line[1].strip()

                if tag == K_TAG_FILE_NAME:
                    value = self.__get_file_name()

                elif tag == K_TAG_MODIFIED:
                    value = datetime.date.today()

                tag = '%s:' % tag
                tag = tag + ' ' * (K_NCHAR - len(tag))
                text = '%s %s %s' % (K_TAG_PREFIX, tag, value)
                line = text

            header_text += '%s\n' % line

        header_text = header_text[:-1]
        self.view.replace(edit, sublime.Region(begin, end), header_text)

        return True

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
