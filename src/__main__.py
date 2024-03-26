import json
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import requests
import zipfile
import pathlib
import shutil

CACHE_DIR = pathlib.Path("cache")
FA_URL = "https://use.fontawesome.com/releases/v6.5.1/fontawesome-free-6.5.1-web.zip"
OUT_DIR = pathlib.Path("out")
DATA_FILE = pathlib.Path("data") / "apps.json"
STATIC_DIR = pathlib.Path("static")

def main():
    shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir()
    CACHE_DIR.mkdir(exist_ok=True)
    with DATA_FILE.open("r") as fd:
        data = json.load(fd)

    for item in data:
        item["link_apple"] = f"https://itunes.apple.com/us/app/keynote/id{item['apple_id']}?mt=8"
        item["link_android"] = f"https://play.google.com/store/apps/details?id={item['android_id']}"

    fa_tmp = (CACHE_DIR / "fa.zip")

    if not fa_tmp.exists():
        fa = requests.get(FA_URL, allow_redirects=True)
        fa.raise_for_status()
        with fa_tmp.open("wb") as fd:
            fd.write(fa.content)
            fd.flush()

    for (file_name, url, color) in [
        (f"apple_{x['apple_id']}", x["link_apple"], "000099" ) for x in data
    ] + [
        (f"android_{x['android_id']}", x["link_android"], "009900") for x in data
    ]:
        generator_url = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={url}&color={color}"
        cached_file = CACHE_DIR / f"{file_name}.png"
        (OUT_DIR / "qr_codes").mkdir(exist_ok=True)
        out_file = OUT_DIR / "qr_codes" / f"{file_name}.png"

        if not cached_file.exists():
            r = requests.get(generator_url, allow_redirects=True)
            r.raise_for_status()
            with cached_file.open("wb") as fd:
                fd.write(r.content)
                fd.flush()
            
        shutil.copy(cached_file, out_file)
        


    
    with zipfile.ZipFile(fa_tmp, 'r') as zip_ref:
        for file_name in [
            "fontawesome-free-6.5.1-web/css/fontawesome.css",
            "fontawesome-free-6.5.1-web/css/brands.css",
            "fontawesome-free-6.5.1-web/css/solid.css",
            "fontawesome-free-6.5.1-web/webfonts/fa-brands-400.ttf",
            "fontawesome-free-6.5.1-web/webfonts/fa-brands-400.woff2",
            "fontawesome-free-6.5.1-web/webfonts/fa-solid-900.ttf",
            "fontawesome-free-6.5.1-web/webfonts/fa-solid-900.ttf"
        ]:
            zip_ref.extract(file_name, OUT_DIR)
    (OUT_DIR / "fontawesome-free-6.5.1-web").rename(OUT_DIR / "fontawesome")
    

    loader = FileSystemLoader("templates")
    env = Environment(loader=loader)
    temp = env.get_template("index.html.jinja")

    comp = temp.render(data_file=data)

    with (OUT_DIR / "index.html").open("w") as fd:
        fd.write(comp)
    
    shutil.copytree(STATIC_DIR, OUT_DIR/"static")

if __name__ == "__main__":
    main()