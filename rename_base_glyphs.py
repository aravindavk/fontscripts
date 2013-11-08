import sys
import fontforge

def _rename_glyph(glyph):
    if glyph.unicode != -1:
        newname = "uni" + hex(glyph.unicode).replace("0x", "").upper().zfill(4)
        if newname != glyph.glyphname:
            print ("%s,%s" % (glyph.glyphname, newname))
            font[glyph.glyphname].glyphname = newname


def rename_glyphs(sfd_name):
    for glyph in font.glyphs():
        _rename_glyph(glyph)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "USAGE: python rename_base_glyphs.py <sfd file>"
        sys.exit(1)

    sfd_name = sys.argv[1]
    font = fontforge.open(sfd_name)
    print ("oldname,newname")
    rename_glyphs(sfd_name)
    font.save()
    font.close()
