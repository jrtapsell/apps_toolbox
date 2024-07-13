"""
Gets the links to the configured apps
"""
from bs4 import BeautifulSoup
from requests import session

from .main import load_data_file


def main():
    """
    The main method
    """
    data = load_data_file()
    r = session()
    for current in data:
        if "link_android" in current:
            resp = r.get(current["link_android"])
        elif "link_apple" in current:
            resp = r.get(current["link_apple"])
        else:
            raise ValueError("Can't find icon")
        resp.raise_for_status()
        soup = BeautifulSoup(markup=resp.text, features="html.parser")
        meta = soup.select_one("meta[property='og:image']")
        print(current["name"], meta.attrs["content"])


if __name__ == "__main__":
    main()
