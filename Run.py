from Calculate import *

def print_lineup(lineup):
    total = 0
    captain = True
    for p in lineup:
        if isinstance(p, str):
            for player in player_list:
                if player.get_name() == p:
                    if captain:
                        print("Captain:")
                        total += 1.5 * player.get_price()
                        captain = False
                    else:
                        print("Util:")
                        total += player.get_price()
                    break
            print(p)
        else:
            if captain:
                print("Captain:")
                total += 1.5 * p.get_price()
                captain = False
            else:
                print("Util:")
                total += p.get_price()
            print(p.get_name())
    print("Projected score:")
    print(lineup_score(lineup))
    print("Total salary:")
    print(total)

best = optimal_lineup(new_player_list, [None])
print_lineup(best)