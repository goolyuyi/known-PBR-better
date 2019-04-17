import mdcsdn
import mdmake
import mdzhihu

with open("input.txt", "r") as inputFile:
    with open("img_desc.txt", "r") as imgDescFile:
        doc = inputFile.read()
        img_desc = imgDescFile.read()

        print("* arrange formulas")
        arrange_formulas_output = mdmake.arrange_formulas(doc, tag_style=mdmake.replace_formula_tag)

        # general output
        print("* general output")
        print("\t- rendering formulas")
        normal_output = mdmake.render_formulas(arrange_formulas_output)

        print("\t- refill images")
        refill_output = mdmake.refill_img_style_html(normal_output, img_desc, style=mdmake.img_html_style_1)

    with open("output.md", "w") as outputFile:
        outputFile.write(refill_output)

        print("* general output done!")

        # md output
        # TODO for stackedit.io
        print("* md output")
        print("\t- rendering formulas")
        arrange_formulas_output = mdmake.arrange_formulas(doc, tag_style=mdmake.replace_formula_tag)
        normal_output = mdmake.render_formulas(arrange_formulas_output, inline=mdmake.render_formulas_inline,
                                               embed=mdmake.render_formulas_embed)

        print("\t- refill images")
        refill_output = mdmake.refill_img_style_html(normal_output, img_desc, style=mdmake.img_markdown_style)

    with open("output_markdown.md", "w") as outputFile:
        outputFile.write(refill_output)

        print("* md output done!")

        # csdn output
        print("* csdn output")
        print("\t- rendering formulas")
        arrange_formulas_output = mdmake.arrange_formulas(doc, tag_style=mdmake.replace_formula_tag)
        normal_output = mdmake.render_formulas(arrange_formulas_output)

        print("\t- refill images")
        refill_output = mdmake.refill_img_style_html(normal_output, img_desc, style=mdcsdn.img_github_style)

    with open("output_csdn.md", "w") as outputFile:
        outputFile.write(refill_output)

        print("* general output done!")



    # zhihu output
    print("* zhihu output")
    print("\t- rendering formulas")
    doc = mdzhihu.remove_footnotes(doc)
    arrange_formulas_output = mdmake.arrange_formulas(doc, tag_style=mdmake.replace_formula_tag)
    normal_output = mdmake.render_formulas(arrange_formulas_output, inline=mdzhihu.render_formulas_inline,
                                           embed=mdzhihu.render_formulas_embed)

    print("\t- refill images")
    refill_output = mdmake.refill_img_style_html(normal_output, img_desc, style=mdmake.img_markdown_style,
                                                 pref=r"https://goolyuyi.synology.me:8889/md/pbr/zhihu/")

    with open("output_zhihu.md", "w") as outputFile:
        outputFile.write(refill_output)

    print("* zhihu output done!")
    print("Done!")
