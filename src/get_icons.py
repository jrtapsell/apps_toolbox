from requests import session
from .main import load_data_file
from bs4 import BeautifulSoup

def main():
    data = load_data_file()
    r = session()
    for current in data:
        if "android_id" not in current:
            continue
        resp = r.get(f"https://play.google.com/store/apps/details?id={current['android_id']}")
        resp.raise_for_status()
        soup = BeautifulSoup(markup=resp.text, features="html.parser")
        meta = soup.select_one("meta[property='og:image']")
        print(current["name"], meta.attrs["content"])

if __name__ == "__main__":
    main()