from Daily_Scrape import *
import sqlite3

conn = sqlite3.Connection("n.db")
conn.execute("DROP TABLE IF EXISTS daily_players;")
conn.execute("CREATE TABLE daily_players(name, proj_score, price);")
for p in player_list:
    conn.execute("INSERT INTO daily_players VALUES (?, ?, ?)", (p.get_name(), p.get_proj_score(), p.get_price()))

def find_best_value():
    """
    Finds the best projected score per price players
    :return: A list of 40 tuples, with each tuple consisting of player name and 1000 * proj_score/price
    """
    print(conn.execute("SELECT name, 1000 * proj_score/price FROM daily_players ORDER BY -proj_score/price LIMIT 40;").fetchall())

def optimal_lineup(remaining_players, lineup):
    """
    Tree recursive method to find the optimal lineup given a player budget of $50000
    Called with an initial lineup of [None]
    :param remaining_players: players that can still be added to the lineup
    :param lineup: players that are already added to the lineup
    :return: list of players in the order [PG, SG, SF, PF, C, G, F, UTIL]
    """
    total_salary = lineup_salary(lineup)
    print(total_salary)
    if total_salary > 50000:
        return 0
    if len(lineup) == 6 and lineup[0] is not None:
        return lineup
    if remaining_players == []:
        return 0
    else:
        player = remaining_players[0]
        captain_available = lineup[0] is None
        flex_available = len(lineup) < 6
        possible_lineups = [lineup]
        if captain_available:
            set_captain = lineup[:]
            set_captain[0] = player
            possible_lineups.append(set_captain)
        if flex_available:
            set_flex = lineup[:]
            set_flex.append(player)
            possible_lineups.append(set_flex)
        return max([optimal_lineup(remaining_players[1:], a) for a in possible_lineups], key=lambda x: lineup_score(x))

def preference_optimal_lineup(remaining_players, lineup):
   """
   Tree recursive method to find the optimal lineup given a player budget of $50000
   Called with a lineup which is a 6-item list, with each item either a player name or None
   :param remaining_players: players that can still be added to the lineup
   :param lineup: players that are already added to the lineup
   :return: list of players in the order [PG, SG, SF, PF, C, G, F, UTIL]
   """
   total_salary = lineup_salary(lineup)
   print(total_salary)
   if total_salary > 50000:
       return 0
   if None not in lineup:
       return lineup
   if remaining_players == []:
       return 0
   else:
       player = remaining_players[0]
       available_slots = []
       for slot in [0, 1, 2, 3, 4, 5]:
           if lineup[slot] is None:
               available_slots.append(slot)
       possible_lineups = [lineup]
       for i in available_slots:
           possible_lineups.append(insertion(lineup, i, player))
       return max([preference_optimal_lineup(remaining_players[1:], a) for a in possible_lineups], key=lambda x: lineup_score(x))

def insertion(lineup, slot, player):
    """
    Inserts a player into a slot in a lineup
    :param lineup: DraftKings lineup
    :param slot: slot number for player to be entered into
    :param player: Player object to be entered into lineup
    :return: the new lineup with the Player object entered
    """
    new_lineup = lineup[:]
    new_lineup[slot] = player
    return new_lineup

def lineup_salary(players_chosen):
    total_salary = 0
    for x in range(len(players_chosen)):
        if players_chosen[x] is not None:
            if isinstance(players_chosen[x], str):
                for player in player_list:
                    if player.get_name() == players_chosen[x]:
                        if x == 0:
                            total_salary += 1.5 * player.get_price()
                        else:
                            total_salary += player.get_price()
                        break
            else:
                if x == 0:
                    total_salary += 1.5 * players_chosen[x].get_price()
                else:
                    total_salary += players_chosen[x].get_price()
    return total_salary

def lineup_score(players_chosen):
    """
    Sums the projected scores of the players in a lineup
    :param players_chosen: either 0 or a list representing a DraftKings lineup
    :return: Projected score of the lineup of a valid lineup
    """
    if players_chosen == 0:
        return 0
    elif len(players_chosen) != 6 or None in players_chosen:
        return 0
    else:
        proj_score = 0
        for x in range(len(players_chosen)):
            if isinstance(players_chosen[x], str):
                for player in player_list:
                        if players_chosen[x] == player.get_name():
                            if x == 0:
                                proj_score += 1.5 * player.get_proj_score()
                            else:
                                proj_score += player.get_proj_score()
                            break
            else:
                if x == 0:
                    proj_score += 1.5 * players_chosen[x].get_proj_score()
                else:
                    proj_score += players_chosen[x].get_proj_score()
        return proj_score

new_player_list = []
inactives = ['Will Barton']

for p in player_list:
    if p.get_name() not in inactives and p.get_proj_score() > 10:
        new_player_list.append(p)
"""best_preferred = preference_optimal_lineup(new_player_list, ['LeBron James', None, None, None, None, None])"""
best = optimal_lineup(new_player_list, [None])

total = 0
captain = True
for p in best:
    if isinstance(p, str):
        print(p)
        for player in player_list:
            if player.get_name() == p:
                if captain:
                    print(1.5 * player.get_price())
                    total += 1.5 * player.get_price()
                    captain = False
                else:
                    print(player.get_price())
                    total += player.get_price()

    else:
        print(p.get_name())
        if captain:
            print(1.5 * p.get_price())
            total += 1.5 * p.get_price()
            captain = False
        else:
            print(p.get_price())
            total += p.get_price()
print(lineup_score(best))
print(total)

