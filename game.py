

class Game():
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    # Gets the move of the specified player (0 or 1), p could be rock, paper or sissor
    def get_player_move(self, p):
        # p could only be (0 or 1)
        return self.moves[p]

    #Check to see which player made the move, takes a player parameter(0 or 1) and move (rock, paper, or sissor)
    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    #Adds the functionality to know if two players are connected
    def connected(self):
        return self.ready

    #If both of the players made their move
    def bothWent(self):
        return self.p1Went and self.p2Went

    # Game logic goes here, nine possible outcomes. Rock, Paper, or Sissor
    def winner(self):
        # 'R' for Rock
        # 'P' for Paper
        # 'S' for Sissor
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner
        
    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
        