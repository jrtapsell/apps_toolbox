from requests import session
from .main import load_data_file

def main():
    data = load_data_file()
    urls_to_check = [*(
        x["link_apple"] for x in data if "link_apple" in x
    ), *(
        x["link_android"] for x in data if "link_android" in x
    ), *(
        x["icon"] for x in data if "icon" in x
    )]
    r = session()
    for current in urls_to_check:
        resp = r.head(current, allow_redirects=True)
        resp.raise_for_status()

if __name__ == "__main__":
    main()