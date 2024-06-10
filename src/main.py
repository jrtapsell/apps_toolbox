import json
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader
import requests
import zipfile
import pathlib
import shutil
import yaml
import segno


CACHE_DIR = pathlib.Path("cache")
FA_URL = "https://use.fontawesome.com/releases/v6.5.1/fontawesome-free-6.5.1-web.zip"
FONT_URL = "https://gwfh.mranftl.com/api/fonts/open-sans?download=zip&subsets=latin&variants=800,regular&formats=woff2"
OUT_DIR = pathlib.Path("out")
DATA_FILE = pathlib.Path("data") / "apps.yaml"
STATIC_DIR = pathlib.Path("static")

def ensure_downloaded(url: str, out_path: pathlib.Path):
    if out_path.exists():
        return
    resp = requests.get(url, allow_redirects=True)
    resp.raise_for_status()
    with out_path.open("wb") as fd:
        fd.write(resp.content)
        fd.flush()


def load_data_file():
    with DATA_FILE.open("r") as fd:
        data = yaml.load(fd, Loader=yaml.SafeLoader)

    for d in data:
        if not d.get("app_id") or not d.get("name"):
            raise AssertionError("Bad data file")

    for item in data:
        if 'apple_id' in item:
            item["apple_id_str"] = str(item["apple_id"])
        if 'apple_id' in item:
            item["link_apple"] = f"https://apps.apple.com/gb/app/redirect/id{item['apple_id']}"
        if 'android_id' in item:
            item["link_android"] = f"https://play.google.com/store/apps/details?id={item['android_id']}"
    return data


def main():
    shutil.rmtree(OUT_DIR, ignore_errors=True)
    OUT_DIR.mkdir()
    CACHE_DIR.mkdir(exist_ok=True)

    data = load_data_file()

    fa_tmp = (CACHE_DIR / "fa.zip")

    ensure_downloaded(FA_URL, fa_tmp)

    for (file_name, url, color) in [
        (f"apple_{x['apple_id']}", x["link_apple"], "#000099" ) for x in data if "link_apple" in x
    ] + [
        (f"android_{x['android_id']}", x["link_android"], "#009900") for x in data if "link_android" in x
    ]:
        cached_file = CACHE_DIR / f"{file_name}.svg"
        (OUT_DIR / "qr_codes").mkdir(exist_ok=True)
        out_file = OUT_DIR / "qr_codes" / f"{file_name}.svg"

        qrcode = segno.make(url, micro=False, error="h")
        qrcode.save(str(cached_file), dark=color, light=None)
            
        shutil.copy(cached_file, out_file)
        


    
    with zipfile.ZipFile(fa_tmp, 'r') as zip_ref:
        for file_name in [
            "fontawesome-free-6.5.1-web/css/fontawesome.css",
            "fontawesome-free-6.5.1-web/css/brands.css",
            "fontawesome-free-6.5.1-web/css/solid.css",
            "fontawesome-free-6.5.1-web/webfonts/fa-brands-400.ttf",
            "fontawesome-free-6.5.1-web/webfonts/fa-brands-400.woff2",
            "fontawesome-free-6.5.1-web/webfonts/fa-solid-900.ttf",
            "fontawesome-free-6.5.1-web/webfonts/fa-solid-900.woff2"
        ]:
            zip_ref.extract(file_name, OUT_DIR)
    (OUT_DIR / "fontawesome-free-6.5.1-web").rename(OUT_DIR / "fontawesome")

    font_cache = CACHE_DIR / "opensans.zip"
    ensure_downloaded(FONT_URL, font_cache)
    with zipfile.ZipFile(font_cache, 'r') as zip_ref:
        zip_ref.extract("open-sans-v40-latin-800.woff2", OUT_DIR)
    

    loader = FileSystemLoader("templates")
    env = Environment(loader=loader)
    temp = env.get_template("index.html.jinja")

    comp = temp.render(data_file=data)

    with (OUT_DIR / "index.html").open("w") as fd:
        fd.write(comp)
    
    shutil.copytree(STATIC_DIR, OUT_DIR/"static")

    icon_dir = OUT_DIR / "icons"
    icon_dir.mkdir()
    for current in data:
        if "icon" not in current:
            continue
        tmp_file = CACHE_DIR / f"icon_{current['app_id']}.png"
        out_file = icon_dir / f"{current['app_id']}.png"
        ensure_downloaded(current["icon"], tmp_file)
        shutil.copy(tmp_file, out_file)

    shutil.copy("_headers", OUT_DIR / "_headers")
