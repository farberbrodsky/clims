import requests
from urllib import parse as urlparse

def login(username, my_id, password):
    """Returns a Requests session which is logged in. Raises ConnectionRefusedError if login info is incorrect."""
    s = requests.Session()
    data = {"txtUser": username, "txtId": my_id, "txtPass": password, "enter": "כניסה", "javas": "1", "src": ""}
    login_result = s.post("https://www.ims.tau.ac.il/Tal/Login_Chk.aspx", data=data)
    # Login was successful if it redirects to /Tal/Sys/Main.aspx?...
    if not "://www.ims.tau.ac.il/Tal/Sys/Main.aspx" in login_result.url:
        raise ConnectionRefusedError
    return s

def login_and_fetch_or_exit(raw_url, auth_data):
    url = urlparse.urlparse(raw_url)
    query = urlparse.parse_qs(url.query)
    query["id"] = 215064114
    encoded_queries = urlparse.urlencode(query)
    final_url = urlparse.urlunparse((url.scheme, url.netloc, url.path, '', encoded_queries, ''))
    try:
        sess = login(auth_data["username"], auth_data["id"], auth_data["password"])
    except ConnectionRefusedError:
        print("Login failed.")
        exit(1)
    return sess.get(final_url).text

