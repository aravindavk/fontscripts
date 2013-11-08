import sys
import fontforge

LSPACE=60
RSPACE=60

# Kannada Base glyphs Ex: U+0C85
glyphs = ["82 83 85 86 87 88 89 8A 8B 8C 8E 8F 90 92 93 94",
          "95 96 97 98 99 9A 9B 9C 9D 9E 9F A0 A1 A2 A3 A4",
          "A5 A6 A7 A8 AA AB AC AD AE AF B0 B1 B2 B3 B5 B6",
          "B7 B8 B9 DE E0 E1 E6 E7 E8 E9 EA EB EC ED EE EF F1 F2"]

glyphs_set = " ".join(glyphs)


def adjust_space():
    for glyph in glyphs_set.split(" "):
        glyphname = "uni0C%s" % glyph
        if not glyphname in font:
            continue

        left_space = font[glyphname].left_side_bearing
        right_space = font[glyphname].right_side_bearing
        print ("%s,%s,%s,%s,%s" % (glyphname, left_space, LSPACE, right_space, RSPACE))
        font[glyphname].left_side_bearing = LSPACE
        font[glyphname].right_side_bearing = RSPACE


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: python adjust_spacing.py <sfd file>"
        sys.exit(1)

    sfd_name = sys.argv[1]
    font = fontforge.open(sfd_name)
    print ("name,left_old,left_new,right_old,right_new")
    adjust_space()
    font.save()
    font.close()


    
