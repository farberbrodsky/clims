import api
import re
from bs4 import BeautifulSoup
from util import parse_table

my_re = re.compile(r'<tr.+>.+<\/tr')

def scans_list_cli(args, auth_data):
    html = api.login_and_fetch_or_exit("/Tal/Scans/Scans_P.aspx?first=yes", auth_data)
    soup = BeautifulSoup(html, features="lxml")
    table = soup.find("table")
    tochniot = parse_table(table)
    printed_result = []
    for tochnit in tochniot:
        if tochnit["מצב"] == "01-פעיל":
            # Go into this and list inside of it
            tochnit_id = tochnit["בחר"]["value"]
            # Go to /Tal/Scans/Scans_L.aspx with this tochnit_id
            url = api.format_url("/Tal/Scans/Scans_L.aspx?first=yes", auth_data)
            session = api.login_or_cached(auth_data)
            result = session.post(url, data={
                "tckey": tochnit_id,
                "javas": 1,
                "peula": 3,
                "caller": "scans_p",
                "sem": "20201",
                "currsem": "20201"
            }).text
            # Get the lines inside of it
            matches = [x + '>' for x in my_re.findall(result)[2:]]
            for match in matches:
                soup2 = BeautifulSoup(match, features="lxml")
                tds = [x.text.replace("\xa0", "") for x in soup2.select("td")]
                status = tds[0]
                course = tds[2]
                printed_result.append({"status": status, "course": course})
    print(printed_result)
