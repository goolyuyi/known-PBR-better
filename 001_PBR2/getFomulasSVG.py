import mdmake
import mdzhihu

with open("input.txt", "r") as inputFile:
    doc = inputFile.read()
    arrange_formulas_output = mdmake.arrange_formulas(doc, tag_style=mdmake.replace_formula_tag)
    breaks=mdmake.extract_long_formulas(arrange_formulas_output)

    ll=[]
    for i in range(1,len(breaks),2):
        ll.append(breaks[i].strip())

    mdzhihu.download_fomulas_from(ll)
