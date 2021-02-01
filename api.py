import requests

def login(username, my_id, password):
    """Returns a Requests session which is logged in. Raises ConnectionRefusedError if login info is incorrect."""
    s = requests.Session()
    data = {"txtUser": username, "txtId": my_id, "txtPass": password, "enter": "כניסה", "javas": "1", "src": ""}
    login_result = s.post("https://www.ims.tau.ac.il/Tal/Login_Chk.aspx", data=data)
    # Login was successful if it redirects to /Tal/Sys/Main.aspx?...
    if not "://www.ims.tau.ac.il/Tal/Sys/Main.aspx" in login_result.url:
        raise ConnectionRefusedError
    return s
