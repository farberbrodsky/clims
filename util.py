from bs4 import BeautifulSoup
from datetime import datetime


def timestamp():
    """Returns timestamp in seconds"""
    return datetime.utcnow().timestamp()


def list_or_first_value(l):
    if len(l) == 1:
        return l[0]
    else:
        return l


def parse_table(table):
    rows = table.find_all("tr")
    if len(rows) == 0:
        return {}
    else:
        first_row = rows[0]
        columns = [x.text for x in first_row.select("td,th")]
        result = []
        for row in rows[1:]:
            values = [
                list_or_first_value(
                    list(
                        x.children)) or x for x in row.select("td,th")]
            result.append({columns[i]: values[i] for i in range(len(columns))})
        return result
