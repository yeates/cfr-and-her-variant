'''
author: yeates
---------
introduction:
apply regret matching algorithm to the RPS(rock-paper-scissors) game.
among this game, two players iteratively calculate a strategy profile by performing regret matching offline.
the game will reach Nash equilibrium in the end.
---------
time:
2019.7.31
'''

from numpy.random import *

MAX_ACTION_NUM = 3


class GamePlayer:
    def __init__(self):
        # generate initial strategy, them sums equal to 1
        self.sigma = [random() / MAX_ACTION_NUM for _ in range(MAX_ACTION_NUM)]
        self.regret = [0.00000001 for _ in range(MAX_ACTION_NUM)]  # cumulative regrets


class RPSGame:
    def play(self, players):
        # compute player1's regrets
        enemy_act = self.get_action(players[1])
        self.cumulate_regret(players[0], enemy_act)
        # compute player2's regrets
        enemy_act = self.get_action(players[0])
        self.cumulate_regret(players[1], enemy_act)
        # update strategy
        players[0].sigma = [r / sum(players[0].regret) for r in players[0].regret]
        players[1].sigma = [r / sum(players[1].regret) for r in players[1].regret]

    def get_action(self, player: GamePlayer):   # pick action by player's strategy
        return player.sigma.index(max(player.sigma))

    def cumulate_regret(self, player: GamePlayer, enemy_act):
        cls = ["Rock", "Paper", "Scissors"]
        real_act = self.get_action(player)
        real_score = self.get_score(cls[real_act], cls[enemy_act])[0]
        for act in range(MAX_ACTION_NUM):
            if act == real_act:
                continue
            regret = self.get_score(cls[real_act], cls[act])[0] - real_score
            player.regret[act] += max(regret, 0)    # must be nonnegative

    def get_score(self, player_1, player_2):
        class_table = {"Rock": 1, "Paper": 2, "Scissors": 3}
        score = [0, 0]   # init
        # compare by class index size
        if class_table[player_1] > class_table[player_2]:
            score = [1, -1]
        elif class_table[player_1] < class_table[player_2]:
            score = [-1, 1]
        # special situation: rock beat scissors
        if [class_table[player_1], class_table[player_2]] in [[1,3], [3,1]]:
            score = [-i for i in score] # reverse
        return score


if __name__ == "__main__":
    RPS = RPSGame()
    Ps = [GamePlayer() for _ in range(2)]  # Players
    iteration_num = 1000
    while iteration_num:
        iteration_num -= 1
        RPS.play(Ps)
    # in the end, every player's strategy will be [1/3, 1/3, 1/3] (that's Nash equilibrium status in RPS game)
    print([p.sigma for p in Ps])



