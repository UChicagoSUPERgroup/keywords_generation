import html
import re
import sys

# template strings for regular expression based parsing
reg_str1 = "|".join([
            r"(?:^ ?\|.*)",
            r"(?:\<ref.*?\>.*?\<\/ref\>)",
            r"(?:\{\{[^\{\}]+\}\})",
            r"(?:===?[^=]+===?)",
            r"(?:<!--[^>]+-->)",
            r"(?:\<\/?br.*?\>)",
            r"(?:&[^ \;]+;)",
            r"(?:\[http[^\]]+\])"
        ])
reg1 = re.compile(reg_str1)

reg_str3 = r"(?:\[\[[^\]]+?\|)(.+?)\]\]"
reg3 = re.compile(reg_str3)

reg_str4 = r"(\[\[(:[^\]]+)\]\])"
reg4 = re.compile(reg_str4)

reg2 = re.compile(r"(?:\{\{[^\{\}]+\}\})|" + reg_str3 + r"|" + reg_str4)

reg5 = re.compile(r"[\{\}\[\]\|\*]")
        
def parse(txt):
    """
    Parse given text from Wikipedia article into plain text without links and
    references.
    """

    # unescape html
    txt = html.unescape(txt)       

    # remove non-links (like references and html tags)
    txt = reg1.sub("", txt)

    # replace links with their contained text (may be on right side of |)
    txt = reg3.sub(r"\1", txt)

    txt = reg4.sub(r"\1", txt)

    # remove outer nested brackets
    txt = reg2.sub("", txt)

    # remove certain characters, like {, [, and |
    return txt #reg5.sub("", txt)

print(parse(sys.stdin.read()))
