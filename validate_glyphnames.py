# -*- coding: utf-8 -*-
import argparse
import codecs
import json
import re
import subprocess
import unittest
import yappi

__doc__ = """
Glyph names validator. This tool uses HarfBuzz shaper to get the glyph sequence
from the input text. Also predict the glyph sequence based on Unicode values of
input text.
"""


class GlyphNameTests(unittest.TestCase):
    pass


def _get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('test_file',
                        help='path to test file')
    parser.add_argument('font_file',
                        help='Path to font file')
    parser.add_argument('-p', '--glyph-prefix',
                        help='glyph prefix used in font', default='uni')
    return parser.parse_args()


def exec_cmd(cmd, env=None):
    """
    Executes the shell command and returns (rc, out, error)
    """
    p = subprocess.Popen(cmd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env=env,
                         close_fds=True)

    (out, err) = p.communicate()
    return (p.returncode, out, err)


def get_glyphseq_from_unicode(txt):
    """
    Hex Code of each char can be extacted using hex(ord(<input letter))
    print hex(ord("A")) will return 0x41 which will be converted into
    0041
    """
    glyphs = []
    for t in txt:
        glyphs.append(hex(ord(t)).upper().replace("0X", "").zfill(4))

    return "_".join(glyphs)


def get_glyphseq_from_font(txt, font_path):
    """
    Executes hb-shape for given text and extracts the glyph sequence from the
    output. hb-shape <font name> --text <sample text> --output-format=json
    And removes all suffix in glyph name(like .abvs, .alt etc)
    """
    cmd = ["hb-shape", font_path, "--text", txt, "--output-format=json"]
    rc, out, err = exec_cmd(cmd)
    glyphs = []
    if rc == 0:
        data = json.loads(out)
        for d in data:
            glyphs.append(d["g"])

    g_list = []
    # Ignore any suffix in glyph name
    for g in glyphs:
        g = g.replace(args.glyph_prefix, "")
        g_list.append(re.sub("\..+", "", g))

    return "_".join(g_list)


def test_generator(line_num, line, font_path):
    """
    Returns a test case lambda func
    """
    expected = get_glyphseq_from_unicode(line.strip())
    actual = get_glyphseq_from_font(line, font_path)

    return lambda self: self.assertEqual(expected,
                                         actual,
                                         'LINE %s: %s != %s' % (line_num,
                                                                expected,
                                                                actual))


def validate_glyph_names(font_path, txt_file):
    """
    Reads the input test file line by line and adds a test
    to GlyphNameTests class. each line from input text will
    become a testcase
    """
    with codecs.open(txt_file, "r", "utf-8") as f:
        l = 1
        for line in f:
            func = test_generator(l, line, font_path)
            setattr(GlyphNameTests, "test_l%s" % l, func)
            l += 1

    runner = unittest.TextTestRunner(verbosity=2)
    itersuite = unittest.TestLoader().loadTestsFromTestCase(GlyphNameTests)
    runner.run(itersuite)


if __name__ == "__main__":
    yappi.start()
    args = _get_args()
    validate_glyph_names(args.font_file, args.test_file)
    yappi.print_stats()
