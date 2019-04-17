import mdmake


def img_github_style(ll, pref):
    h = r'''
<p>
<center><img src="{img_url}" alt={alt} width="{width}%"><br><font size=-1 color=gray><i>{text}</i></font></center>
</p>
'''

    csdn_pref=r'''https://github.com/goolyuyi/known-PBR-better/blob/master/001_PBR2/img/{img_url}?raw=true'''

    txt = "<br />".join(mdmake.replace_txt_link(ll["img_txt"]).strip().splitlines())

    img_url= csdn_pref.format(img_url=ll["img_url"])

    img = h.format(img_url=img_url, width=ll["img_css_width"], alt=ll["img_tag"],
                   text=txt) if ll["img_url"].strip() else ""
    return img,""