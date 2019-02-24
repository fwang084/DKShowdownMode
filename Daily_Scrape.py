from Player import *
import xlrd

def create_players(player_list):
    """
    Loops through every NBA player, and for those who are playing on the given slate,
    creates a Player object to represent the player, and adds that to player_list
    :return: None
    """
    for i in range(draftkings_info.nrows):
        row = draftkings_info.row_values(i)
        if row[4] == 'UTIL':
            player_list.append(Player(row[2], row[7], row[5], 0))
    for p in player_list:
        for i in range(roto_info.nrows):
            row = roto_info.row_values(i)
            if p.get_name() == row[0]:
                p.set_proj_score(row[7])
                break
    return player_list
roto_spreadsheet = xlrd.open_workbook('nba-player.xls')
roto_info = roto_spreadsheet.sheet_by_index(0)

draftkings_spreadsheet = xlrd.open_workbook('DKSalaries.xls')
draftkings_info = draftkings_spreadsheet.sheet_by_index(0)


player_list = create_players([])
