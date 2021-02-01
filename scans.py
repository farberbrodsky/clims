import api
from bs4 import BeautifulSoup
from util import parse_table


def scans_list_cli(args, auth_data):
    html = api.login_and_fetch_or_exit(
        "https://www.ims.tau.ac.il/Tal/Scans/Scans_P.aspx?first=yes", auth_data)
    soup = BeautifulSoup(html, features="lxml")
    table = soup.find("table")
    tochniot = parse_table(table)
    for tochnit in tochniot:
        if tochnit["מצב"] == "01-פעיל":
            # Go into this and list inside of it
            tochnit_id = tochnit["בחר"]["value"]
            # Go to /Tal/Scans/Scans_L.aspx with this tochnit_id
            url = "https://www.ims.tau.ac.il/Tal/Scans/Scans_L.aspx?first=yes"
    print(tochniot)
