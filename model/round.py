"""Class Round"""
# coding: utf-8

from model.player import Player


class Round:
    """ Class Round """

    def __init__(self, name, start_date, end_date, pairs):
        """Initialisation"""
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.pairs = pairs

    @staticmethod
    def index_player_by_point_by_rank(sort_index_players_by_points):
        index_player_by_point_by_rank = list()
        for point, index_player in sort_index_players_by_points:
            if len(index_player) == 1:
                index_player_by_point_by_rank.append(int(index_player[0]))
            else:
                players = [Player.get_players_db()[int(index)] for index in index_player]
                players_by_ranking = Player.get_players_by_ranking(players)
                for player__ in players_by_ranking:
                    index_player_by_point_by_rank.append(Player().find_index_player_by_last_name(player__.last_name))
        return index_player_by_point_by_rank

    @staticmethod
    def index_players_total_points(rounds):
        """ return the players (index) with their total game points  """
        index_players_total_points = dict()
        for turn in rounds:
            for match in turn.pairs:
                for data_player in match:
                    try:
                        index_players_total_points[data_player[0]] += float(data_player[1])
                    except KeyError:
                        index_players_total_points[data_player[0]] = float(data_player[1])
        return index_players_total_points

    @staticmethod
    def sort_index_players_by_points(index_player_by_point):
        point_index_players = dict()
        for key in index_player_by_point.keys():
            try:
                point_index_players[str(index_player_by_point[key])].append(str(key))
            except KeyError:
                point_index_players[str(index_player_by_point[key])] = [str(key)]
        return sorted(point_index_players.items(), key=lambda t: t[0], reverse=True)

    @staticmethod
    def get_all_pairs(rounds):
        pair = []
        for turn in rounds:
            for match in turn.pairs:
                pair.append([match[0][0], match[1][0]])
        return pair

    @staticmethod
    def check_pair(rounds, pair):
        all_pair = Round.get_all_pairs(rounds)
        print(all_pair)
        print(pair)
        if pair not in all_pair:
            return True
        return False


if __name__ == "__main__":
    pass
