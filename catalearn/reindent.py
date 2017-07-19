
import tokenize
import os, shutil
import sys


# very hacky
def correct_indentation(source):
    temp_file = open("temp.py", "w")
    temp_file.write(source) 
    temp_file.close()
    temp_file = open("temp.py", "r")
    r = Reindenter(temp_file)
    r.run()
    temp_file.close()
    temp_file = open("temp.py", "w")
    r.write(temp_file)
    temp_file.close()
    temp_file = open("temp.py", "r")
    new_source = temp_file.read()
    temp_file.close()
    return new_source


def _rstrip(line, JUNK='\n \t'):
    i = len(line)
    while i > 0 and line[i - 1] in JUNK:
        i -= 1
    return line[:i]


class Reindenter:

    def __init__(self, f):
        self.find_stmt = 1  
        self.level = 0    
        self.raw = f.readlines()
        self.lines = [_rstrip(line).expandtabs() + "\n"
                      for line in self.raw]
        self.lines.insert(0, None)
        self.index = 1
        self.stats = []
        self.newlines = f.newlines

    def run(self):
        tokens = tokenize.generate_tokens(self.getline)
        for _token in tokens:
            self.tokeneater(*_token)
        lines = self.lines
        while lines and lines[-1] == "\n":
            lines.pop()
        stats = self.stats
        stats.append((len(lines), 0))
        have2want = {}
        after = self.after = []
        i = stats[0][0]
        after.extend(lines[1:i])
        for i in range(len(stats) - 1):
            thisstmt, thislevel = stats[i]
            nextstmt = stats[i + 1][0]
            have = getlspace(lines[thisstmt])
            want = thislevel * 4
            if want < 0:
                if have:
                    want = have2want.get(have, -1)
                    if want < 0:
                        for j in range(i + 1, len(stats) - 1):
                            jline, jlevel = stats[j]
                            if jlevel >= 0:
                                if have == getlspace(lines[jline]):
                                    want = jlevel * 4
                                break
                    if want < 0:
                        for j in range(i - 1, -1, -1):
                            jline, jlevel = stats[j]
                            if jlevel >= 0:
                                want = have + (getlspace(after[jline - 1]) -
                                               getlspace(lines[jline]))
                                break
                    if want < 0:
                        want = have
                else:
                    want = 0
            assert want >= 0
            have2want[have] = want
            diff = want - have
            if diff == 0 or have == 0:
                after.extend(lines[thisstmt:nextstmt])
            else:
                for line in lines[thisstmt:nextstmt]:
                    if diff > 0:
                        if line == "\n":
                            after.append(line)
                        else:
                            after.append(" " * diff + line)
                    else:
                        remove = min(getlspace(line), -diff)
                        after.append(line[remove:])
        return self.raw != self.after

    def write(self, f):
        f.writelines(self.after)

    def getline(self):
        if self.index >= len(self.lines):
            line = ""
        else:
            line = self.lines[self.index]
            self.index += 1
        return line

    def tokeneater(self, type, token, slinecol, end, line,
                   INDENT=tokenize.INDENT,
                   DEDENT=tokenize.DEDENT,
                   NEWLINE=tokenize.NEWLINE,
                   COMMENT=tokenize.COMMENT,
                   NL=tokenize.NL):

        if type == NEWLINE:
            self.find_stmt = 1

        elif type == INDENT:
            self.find_stmt = 1
            self.level += 1

        elif type == DEDENT:
            self.find_stmt = 1
            self.level -= 1

        elif type == COMMENT:
            if self.find_stmt:
                self.stats.append((slinecol[0], -1))

        elif type == NL:
            pass

        elif self.find_stmt:
            self.find_stmt = 0
            if line:  
                self.stats.append((slinecol[0], self.level))

def getlspace(line):
    i, n = 0, len(line)
    while i < n and line[i] == " ":
        i += 1
    return i