import bisect
import re


def clear_input_space(doc):
    sl = doc.splitlines()
    o = ""
    bl = 0
    for b in sl:
        if b.strip():
            if bl >= 1:
                o = o + "\n"
                bl = 0
            o = o + b.strip() + "\n"
        else:
            bl = bl + 1
    return o


def extract_long_formulas(formula):
    return re.split(r"\$\$", formula, flags=re.MULTILINE | re.DOTALL)


def extract_formula_tag(formula, remove_tag=False):
    r"""
    get formula tag for \\Tag{xxx}

    :param formula:
    :param remove_tag:
    :return: tag in {xxx}, formula removed \\Tag if remove_tag is True
    """
    m = re.search(r'\\[Tt]ag\{(.+?)\}', formula, re.MULTILINE)
    if m is None:
        return None

    tag = m.group(1)

    if remove_tag:
        formula = m.re.sub("", formula)

    return tag, formula


def extract_literal_formula_tag(tag):
    if tag.startswith("l:"):
        return True, tag[2:]
    else:
        return False, tag


def replace_formula_tag(formula, tag):
    formula = formula.strip()

    r = re.compile(r'\\[Tt]ag\{(.+?)\}', re.MULTILINE)
    stag = str(tag)

    if stag.strip():
        return r.sub(r"\\tag{{{0}}}".format(stag.strip()), formula)
    else:
        return r.sub("", formula)


def replace_formula_tag_qquad(formula, tag):
    formula = formula.strip()

    r = re.compile(r'\\[Tt]ag\{(.+?)\}', re.MULTILINE)
    return r.sub("", formula).strip() + "\\qquad\\qquad({0})".format(tag)


def arrange_formulas(doc, tag_style=replace_formula_tag):
    breaks = extract_long_formulas(doc)
    return rearrange_formulas_ref(breaks, tag_style, False)


def rearrange_formulas_ref(breaks, tag_style, strip_formulas=True):
    formula_dict = {}

    # gather long formulas
    dump_formulas_flag = False

    index = 0
    for i in range(1, len(breaks), 2):
        b = breaks[i]
        formula_tag = extract_formula_tag(b, False)
        if formula_tag is not None:
            (tag_literal, tag) = extract_literal_formula_tag(formula_tag[0])

            if tag_literal:
                index_tag = tag
            else:
                index += 1
                index_tag = index

            if tag not in formula_dict:
                formula_dict[tag] = {"formula": formula_tag[1], "tag_literal": tag_literal, "index_tag": index_tag,
                                     "def": 1, "ref": 0,
                                     "order": i}

                breaks[i] = "%%ref_{0}".format(tag)

            else:
                formula_dict[tag]["def"] += 1
                dump_formulas_flag = True

    if dump_formulas_flag:
        # report dump formulas
        for (key, value) in filter(lambda v: v[1]["def"] > 1, formula_dict.items()):
            print(r"ERROR:detected formula {{{0}}} defined dumped {1} times".format(key, value["def"]))
        return ""
        # TODO raise exception

    # count refs
    for (i, b) in enumerate(breaks):
        if i % 2 == 0:  # txt
            b_line = b.splitlines()
            for b in b_line:
                bc = re.split(r"\%", b)
                for j in range(0, len(bc)):
                    if j % 2 == 1:
                        if bc[j] in formula_dict:  # formula ref
                            formula_dict[bc[j]]["ref"] += 1

    # TODO report outside
    print("\t formulas ref count:")
    for (key, value) in formula_dict.items():
        print("\t\t{{{0}}}\t{1}".format(key, value["ref"]))

    # strip formula index
    if strip_formulas:
        index = 1
        for (key, value) in sorted(formula_dict.items(), key=lambda k: k[1]["order"]):
            if not value["tag_literal"]:
                if (value["ref"]) >= 1:
                    value["index_tag"] = index
                    index += 1
                else:
                    value["index_tag"] = ""

    # TODO python debug cmd
    # TODO python type hints

    # regenerate documents
    c_o = []
    for (i, b) in enumerate(breaks):
        c_b = ""

        if i % 2 == 1:  # formulas
            if b.startswith("%%ref_"):
                ft = formula_dict[b[len("%%ref_"):]]
                ft = tag_style(ft["formula"], ft["index_tag"])
            else:
                ft = b

            c_b = f"$$\n{ft.strip()}\n$$"

        else:  # txt
            b_line = b.splitlines()

            for bl in b_line:
                bc = re.split(r"\%", bl)

                c_l = ""
                for j in range(0, len(bc)):
                    if j % 2 == 1:
                        if bc[j] in formula_dict:
                            formula_dict[bc[j]]["ref"] += 1
                            c_c = r"$\left(\mathrm{{{0}}}\right)$".format(str(formula_dict[bc[j]]["index_tag"]))
                        else:
                            # TODO line number
                            # TODO report outside
                            print(f"formula ref cannot identify:{bc[j]}")
                            c_c = f"%bad reference:{bc[j]}%"
                        c_l = c_l + c_c

                    else:
                        c_l = c_l + bc[j]
                c_b += c_l + "\n"
        c_o.append(c_b)

    return "".join(c_o)


def render_formulas_inline(formula):
    return "${0}$".format(formula.strip())


def render_formulas_embed(formula):
    return "\n$$\n{0}\n$$\n".format(formula.strip())


def render_formulas(document, inline=render_formulas_inline, embed=render_formulas_embed):
    long_breaks = extract_long_formulas(document)
    c_o = []

    for (i, b) in enumerate(long_breaks):

        if (i % 2 == 1):  # long formulas
            c_o.append(embed(b))
        else:  # txt lines
            c_c = ""
            for (j, c) in enumerate(re.split("[$]", b)):
                if (j % 2 == 1):  # short formulas
                    c_c = c_c + inline(c)
                else:
                    c_c = c_c + c

            c_o.append(c_c)

    return "".join(c_o)


def make_img_URL(url, pref):
    return r"{0}{1}".format(pref, url)


def replace_txt_link(txt):
    return re.sub(r"(\[(.+?)\]\((.+?)\))", r"""<a href="\3">\2</a>""", txt)


def img_markdown_style(ll, pref):
    h = r"""![{tag}]({url})
{txt}
"""

    t = ll["img_txt"].strip()
    txt = "_{txt}_".format(txt=t) if t else ""

    hh = h.format(tag=ll["img_tag"], url=make_img_URL(ll["img_url"], pref), txt=txt)

    return hh, ""


def img_html_style_1(ll, pref):
    h = r"""
<div class="polaroid {width}">{img}{txt}</div>
"""
    h1 = r"""<img src="{img}" alt={alt}>"""
    h2 = r"""<p>{text}</p>"""

    img = h1.format(img=make_img_URL(ll["img_url"], pref), alt=ll["img_tag"]) if ll["img_url"].strip() else ""
    aaa = "<br />".join(replace_txt_link(ll["img_txt"]).strip().splitlines())
    txt = h2.format(text=aaa if ll["img_txt"].strip() else "")
    return h.format(width=parse_img_width_to_CSS_tag(ll["img_css_width"]), txt=txt, img=img), ""


def parse_img_width_to_CSS_tag(width):
    l = [
        (30, "smalli"),
        (50, "mediumi"),
        (80, "largei"),
        (100, "fulli")
    ]
    l.sort()
    return l[bisect.bisect_right(l, (width,))][1]


def parse_img_desc(img_desc):
    '''
    parse image desc

    image desc file:

    [t]image tag

    image url

    image desc

    image width

    :param img_desc:
    :return:
    '''
    # r1 = re.compile(r"(\[t\].*?)(?=\[t\])", re.MULTILINE | re.DOTALL)
    # r2 = re.compile(r"\[t\](.+)")
    r3 = re.compile(r"^(\d{1,3})\s*$")

    ll = []
    sp = re.split(r"\[t\]", img_desc, flags=re.MULTILINE | re.DOTALL)

    for mt in sp:
        if mt.strip():
            sl = mt.splitlines()
            if len(sl) > 1 and sl[0].strip():
                width = 100
                txt = ""
                for s in sl[2:]:
                    m = r3.match(s)
                    if m:
                        width = int(m.group(1))
                    elif s.strip():
                        txt = txt + s.strip() + "\n"

                ll.append(
                    {"img_tag": sl[0], "img_url": sl[1], "img_txt": txt,
                     "img_css_width": width})
    return ll


def refill_img_style_html(document, img_desc, pref=r"https://goolyuyi.synology.me:8889/md/pbr/",
                          style=img_html_style_1):
    """


    :param style:
    :param pref:
    :param document:
    :param img_desc:
    :return:
    """
    imgdesc = parse_img_desc(img_desc)

    d1 = document
    d2 = "\n"

    for l in imgdesc:
        to, end = style(l, pref)
        d1 = re.sub(r"^(\[t\]{0}\s*)$".format(re.escape(l['img_tag'])), to, d1, flags=re.MULTILINE)

        d2 += end + "\n"
    return d1 + d2.strip()
