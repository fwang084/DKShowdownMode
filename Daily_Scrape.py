from Player import *
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import xlrd


def simple_get(url):
    """
    Attempts to get the content at 'url' by making an HTTP GET request.
    If the content-type of response is HTML/XML, return the text content, otherwise return None."""
    try:
        with closing(get(url, stream = True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
def is_good_response(resp):
    """ Returns True if the response seems to be HTML, False otherwise."""
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)
def log_error(e):
    print(e)

def create_players(player_list):
    """
    Loops through every NBA player, and for those who are playing on the given slate,
    creates a Player object to represent the player, and adds that to player_list
    :return: None
    """
    for i in range(roto_info.nrows):
        row = roto_info.row_values(i)
        player_list.append(Player(row[0], row[3], row[1], row[7]))

roto_spreadsheet = xlrd.open_workbook('nba-player.xls')
roto_info = roto_spreadsheet.sheet_by_index(0)

player_list=[]
create_players(player_list)