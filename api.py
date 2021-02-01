import pickle  # Yeah, I know it's insecure, but it's the only way to store cookies
import requests
from urllib import parse as urlparse
from util import timestamp
from appdirs import AppDirs
from pathlib import Path


def login(auth_data):
    """Returns a Requests session which is logged in. Raises ConnectionRefusedError if login info is incorrect."""
    s = requests.Session()
    data = {
        "txtUser": auth_data["username"],
        "txtId": auth_data["id"],
        "txtPass": auth_data["password"],
        "enter": "כניסה",
        "javas": "1",
        "src": ""
    }
    login_result = s.post(
        "https://www.ims.tau.ac.il/Tal/Login_Chk.aspx",
        data=data)
    # Login was successful if it redirects to /Tal/Sys/Main.aspx?...
    if "://www.ims.tau.ac.il/Tal/Sys/Main.aspx" not in login_result.url:
        raise ConnectionRefusedError
    return s


sess_file = Path(AppDirs("clims").user_config_dir) / "cached_session"


def login_or_cached(auth_data, cache_path=sess_file):
    """Tries to use a cached session, if it's from the last hour"""
    time = timestamp()
    try:
        with open(cache_path, "rb") as f:
            pickled_data = pickle.load(f)
            if pickled_data["username"] == auth_data["username"] and \
                pickled_data["id"] == auth_data["id"] and \
                    pickled_data["password"] == auth_data["password"] and \
                    pickled_data["time"] > (time - 3600):
                # From the last hour, and is of the same parameters
                session = requests.Session()
                session.cookies.update(pickled_data["cookies"])
                return session
    except FileNotFoundError:
        pass
    # Save a new session to the cache
    new_session = login(auth_data)
    with open(cache_path, "wb") as f:
        data = {
            "username": auth_data["username"],
            "id": auth_data["id"],
            "password": auth_data["password"],
            "time": time,
            "cookies": new_session.cookies
        }
        pickle.dump(data, f)
    return new_session


def format_url(raw_url, auth_data):
    url = urlparse.urlparse(raw_url)
    query = urlparse.parse_qsl(url.query)
    query.append(("id", auth_data["id"]))
    encoded_queries = urlparse.urlencode(query)
    final_url = urlparse.urlunparse(
        (url.scheme or "https",
         url.netloc or "www.ims.tau.ac.il",
         url.path,
         '',
         encoded_queries,
         ''))
    return final_url


def login_and_fetch_or_exit(raw_url, auth_data):
    final_url = format_url(raw_url, auth_data)
    try:
        sess = login_or_cached(auth_data, sess_file)
    except ConnectionRefusedError:
        print("Login failed.")
        exit(1)
    return sess.get(final_url).text
