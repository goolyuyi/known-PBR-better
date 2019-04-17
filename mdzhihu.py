import re
import urllib.parse as ulp
import shutil
import urllib.request as rq
from pathlib import *


def render_formulas_inline(formula):
    embed = r'''<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex={encode}" alt="{raw}">'''
    # embed=r'''![{raw}]({encode})'''

    return embed.format(encode=ulp.quote(formula.strip()), raw=formula.strip())


def render_formulas_embed(formula):
    inline = r'''
<img class="Formula-image" data-eeimg="true" src="//www.zhihu.com/equation?tex={encode}" alt="{raw}">
'''

    formula = formula.strip() + "\\\\"

    formula= "".join(formula.splitlines())

    return inline.format(encode=ulp.quote(formula), raw=formula)


def remove_footnotes(doc):
    doc = re.sub(r"\[\^\w+\](?![:])", "", doc)
    doc = re.sub(r"\[\^\w+\]:", "- ", doc)
    return doc


p = Path("zhihu_svgs/")


def download_fomulas_from(formulas, path=p):
    if not path.is_dir():
        path.mkdir(parents=True)


    for (i, f) in enumerate(formulas):
        tex_url = r"https://www.zhihu.com/equation?tex={encode}"
        tex_url = tex_url.format(encode=ulp.quote(f.strip()))
        print(f"* progress:{i}/{len(formulas)}")
        print(f"\tdownloading:{tex_url}")

        with rq.urlopen(tex_url) as response:
            if response.status == 200:
                print("HTTP 200")
                with open(path / (str(i) + ".svg"), "wb+") as svg:
                    shutil.copyfileobj(response, svg)
                    print(response.msg)
