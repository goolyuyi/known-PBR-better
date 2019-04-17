import math
from pathlib import *
from PIL import Image
import mdmake
import shutil

p=Path("img/")
o=Path("zhihu/")
zhihu_width=660

def zhihu_resize_curve(r):
    return 1-math.exp(-1.8*r)

def zhihu_resize(img_desc,img_path=p,output_path=o,max_width=zhihu_width,adjustment=1.3):
    if not img_path.is_dir():
        raise Exception("bad path:",p)

    dd= dict(map(lambda x:(x["img_url"],x),img_desc))

    if not output_path.is_dir():
        output_path.mkdir(parents=True)

    for i in img_path.iterdir():
        print("open:", i)
        try:
            img = Image.open(i)

            n=i.name
            df=False

            o=output_path/i.name

            if n in dd:#resize
                sz=int(dd[n]["img_css_width"])
                if sz <100:

                    df=True
                    ratio = float(img.width / img.height)
                    nw=round(float(zhihu_resize_curve(sz/100.0)*zhihu_width))
                    nh=round(float(nw/img.width)*img.height)
                    print(f"resize:[{img.width}x{img.height}]:{ratio}->[{nw}x{nh}]")
                    img=img.resize((nw,nh),Image.BICUBIC)

                    print("writing:",o,"\n")
                    img.save(o,quality=90)

            if not df:
                print("copy:",o,"\n")
                shutil.copy(i,o)
        except:
            pass



with open("img_desc.txt","r") as img_desc_file:
    img_desc=mdmake.parse_img_desc(img_desc_file.read())
    zhihu_resize(img_desc)
