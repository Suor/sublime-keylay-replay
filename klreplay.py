import re
import sublime, sublime_plugin


# Added - to both to skip other it
RU_CHARS = """ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.йцукенгшщзхъфывапролджэячсмитьбю-"""
EN_CHARS = """QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>/qwertyuiop[]asdfghjkl;'zxcvbnm,.-"""

RU_RE = re.compile(r'([%s\s]*)$' % re.escape(RU_CHARS))
# Skip brackets because that we probably meant and then forgot to change layout
EN_CHARS_TO_MATCH = ''.join(set(EN_CHARS) - set('[]'))
EN_RE = re.compile(r'([%s\s]*)$' % re.escape(EN_CHARS_TO_MATCH))

TABLE = str.maketrans(RU_CHARS + EN_CHARS, EN_CHARS + RU_CHARS)


class KeylayReplayCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sel = self.view.sel()
        if len(sel) == 1 and sel[0].empty():
            pos = sel[0].a
            line_s = line_start_str(self.view, pos)
            ru_len = len(RU_RE.search(line_s).group())
            en_len = len(EN_RE.search(line_s).group())
            regions = [sublime.Region(pos - max(ru_len, en_len), pos)]
        else:
            regions = list(sel)

        for region in regions:
            text = self.view.substr(region)
            self.view.replace(edit, region, text.translate(TABLE))


# View tools

def line_start(view, pos):
    line = view.line(pos)
    return sublime.Region(line.begin(), pos)

def line_start_str(view, pos):
    return view.substr(line_start(view, pos))
