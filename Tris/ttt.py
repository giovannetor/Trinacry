import threading
import time
import sopel.plugin as plugin
import sopel.tools as tools
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL

X = CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_CYAN + "X" + CONTROL_NORMAL
O = CONTROL_BOLD + CONTROL_COLOR + colors.RED + "O" + CONTROL_NORMAL
TRIS = CONTROL_BOLD + CONTROL_COLOR + colors.RED + "," + colors.WHITE + " Tic" + CONTROL_COLOR + colors.BLACK \
       + "," + colors.WHITE + "Tac" + CONTROL_COLOR + colors.LIGHT_CYAN + "," + colors.WHITE + "Toe " + CONTROL_NORMAL

gridlist = ["A1" , "A2"  , "A3" , "B1"   ,"B2"  , "B3" , "C1" , "C2", "C3"]

log_chan = "#trinacry-logs"
game_chan = ["#TicTacToe" , "#games"]
lock = threading.RLock()
max_player = 2

strings_eng = {"impos_unirsi": "I'm sorry %s , the max number of players is 4. Wait until next match :)",
               "cant_play": "You are not inside the match, please do not disturb the other players :)",
               "start" : "Players Reached! Let's play " + TRIS + "!!",
               "gia_dentro": " %s you are already inside the match of " + TRIS + ".",
               "turno" : "%s 's turn, please wait.",
               "noletter" : "You typed '%s', must type A, B or C instead.",
               "nonumber" : "You typed '%s', musts be 1, 2 or 3 instead.",
               "nogrid" : "'%s' isn't a proper slot in the grid.",
               "yours" : "This slot is already yours!",
               "altro" : "This slot belongs to the other player.",
               "ok" : "%s in %s by %s!",
               "win" : "%s made " + TRIS + "!!",
               "next_turn" : "It's %s's turn now!",
               "final_win" : "%s scored 3 wins and won the " + TRIS + " game!!",
               "endgame" : CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER"
                           + CONTROL_NORMAL + ". Start a new match if you wanna play again.",
               "game_started" : "A new game of " + TRIS + " is started!",
               "adstop" : CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER"
                           + CONTROL_NORMAL + ". The game was stopped by an Admin.",
               "not_started" : "The match hasn't started yet. Find another player to start.",
               "no_square" : "Please put a slot after the command. e.g. 'A2'",
               "quit_stop" : CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER"
                           + CONTROL_NORMAL + ":a player left the match.",
               "draw_" : "The match is a DRAW!",
               "missing" : "A parameter is missing...try to write all together? :) "
               }

class tttgame:
    def __init__(self , trigger):
        self.strings = strings_eng  # default strings are in english
        #self.string_help = string_help_eng
        #self.rules = rules_eng
        self.starter = trigger.nick
        self.channel = trigger.sender
        self.players = {}  # Player's dict
        self.playerOrder = []  # List of players per order
        self.currentPlayer = 0
        self.startTime = None
        self.dealt = False
        self.griglia =  {"A1" : "/" , "A2" : "/" , "A3" : "/",   # game grid
                         "B1" : "/"  ,"B2" : "/" , "B3" : "/" ,
                         "C1" : "/" , "C2" : "/" , "C3" : "/"}
        self.jcount = 0
        self.counter = 0

    def join(self, bot, trigger):
        with lock:
            if trigger.nick not in self.players:  # if the player is not in the game
                if len(self.players) == max_player:
                    bot.say(self.strings["impos_unirsi"] % trigger.nick)  # match full
                    return
                if self.dealt:
                    bot.say(self.strings["cant_play"])
                    return
                if self.jcount == 0:
                    self.players[trigger.nick]= {"squares" : [] , "sign" : X , "score" : 0}
                else:
                    self.players[trigger.nick]= {"squares" : [] , "sign" : O , "score" : 0}  # add player to players dict
                self.jcount += 1
                self.playerOrder.append(trigger.nick)  # add player to players order list
                if len(self.players) == 2:
                    self.dealt = True
                    bot.say(self.strings["start"])
                    self.print_grid(bot)
                    bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
            else:
                bot.say(self.strings["gia_dentro"] % trigger.nick)  # player already in

    def play(self, bot, trigger):
        player = trigger.nick
        if not self.dealt:
            bot.say(self.strings["not_started"])
            return
        if player not in self.players:
            bot.notice(self.strings['cant_play'], player)
            return
        if player != self.playerOrder[self.currentPlayer]:
            bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
            return
        if not trigger.group(3):
            bot.say(self.strings["no_square"])
            return
        

        cmd = trigger.group(3).upper()
        #print(cmd)

        if cmd[0] not in "ABC":
            try:
                bot.say(self.strings["noletter"] % cmd[0])
            except:
                bot.say(self.strings["missing"])
            return

        try: int(cmd[1])
        except:
            try:
                bot.say(self.strings["nonumber"] % cmd[1])
            except:
                bot.say(self.strings["missing"])
            return

        if cmd not in gridlist:
            bot.say(self.strings["nogrid"] % cmd)
            return

        cp = self.check_possible(player , cmd)
        if cp == 0:
            bot.say(self.strings["yours"])
            return
        elif cp == 2:
            bot.say(self.strings["altro"])
            return

        bot.say(self.strings["ok"] % (self.players[player]["sign"] , cmd , player))

        self.players[player]["squares"].append(cmd)
        self.griglia[cmd] = self.players[player]["sign"]
        self.print_grid(bot)
        self.counter += 1
        print(self.counter)
        if self.checkwin(player):
            bot.say(self.strings["win"] % player)
            self.players[player]["score"] += 1
            self.reboot(bot , trigger  ,place = trigger.sender)
        else:
            self.currentPlayer += 1
            if self.currentPlayer == len(self.playerOrder):
               self.currentPlayer = 0
            if self.counter == 9:
                bot.say(self.strings["draw_"])                
                self.currentPlayer += 1
                if self.currentPlayer == len(self.playerOrder):
                    self.currentPlayer = 0
                self.reboot(bot , trigger , place = trigger.sender)
                return
            bot.say(self.strings["next_turn"] % self.playerOrder[self.currentPlayer])

    def reboot(self , bot , trigger, place):
        for player in self.players:
            if self.players[player]["score"] == 3:
                bot.say(self.strings["final_win"] % (player))
                self.endgame(bot , trigger ,player_win = player , place = place)
                return
            self.players[player]["squares"].clear()

            if self.players[player]["sign"] == X:
                self.players[player]["sign"] = O
            else:
                self.players[player]["sign"] = X

        self.currentPlayer += 1
        if self.currentPlayer == len(self.playerOrder):
           self.currentPlayer = 0

        self.griglia = {"A1" : "/" , "A2" : "/" , "A3" : "/",
                         "B1" : "/"  ,"B2" : "/" , "B3" : "/" ,
                         "C1" : "/" , "C2" : "/" , "C3" : "/"}

        self.print_grid(bot)
        bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
        self.counter = 0
        self.jcount = 0

    def endgame(self , bot, trigger, player_win , place):
        bot.say(self.strings["endgame"])
        forced = False
        tttbot.endgame( bot , trigger ,player_win,  place , forced )

    def checkwin(self , player):
        squ =  self.players[player]["squares"]
        check_dic = {"A" : 0 , "B" : 0 , "C" : 0 , "1" : 0 , "2" : 0 , "3" : 0}

        for combination in squ:
            check_dic[combination[0]] += 1
            check_dic[str(combination[1])] += 1

        if max(check_dic.values()) == 3:
            return True
        elif "A1" in squ and "B2" in squ and "C3" in squ:
            return True
        elif "A3" in squ and "B2" in squ and "C1" in squ:
            return True
        else:
            return False

    def check_possible(self , player , cmd):
        if self.griglia[cmd] == self.players[player]["sign"]:
            return 0
        else:
            if self.griglia[cmd] == "/":
                return 1
            else:
                return 2

    def print_grid(self , bot):
        dicgrid = self.griglia
        bot.say(dicgrid["A1"] + "   |   " + dicgrid["A2"] + "   |   " + dicgrid["A3"])
        bot.say("-------------")
        bot.say(dicgrid["B1"] + "   |   " + dicgrid["B2"] + "   |   " + dicgrid["B3"])
        bot.say("-------------")
        bot.say(dicgrid["C1"] + "   |   " + dicgrid["C2"] + "   |   " + dicgrid["C3"])


class tttbot:
    def __init__(self):
        self.games = {}
        self.strings = strings_eng

    def start(self, bot, trigger):

        if trigger.sender in self.games:
            self.join(bot, trigger)
        else:
            bot.say(self.strings['game_started'])
            bot.say("[" + TRIS + "] : partita INIZIATA in " + trigger.sender + " da: " + trigger.nick , log_chan)
            self.games[trigger.sender] = tttgame(trigger)
            self.join(bot, trigger)


    def endgame(self, bot , trigger , player_win, place, forced = False , partquit=False):
        if trigger.sender not in self.games:
               return
        if forced:
            
            bot.say("[" + TRIS + "] : partita BLOCCATA in " + trigger.sender + " da: " + trigger.nick , log_chan)
            bot.say(self.strings["adstop"])
        elif partquit:
            bot.say(self.strings["quit_stop"])
        else:
            bot.say("[" + TRIS + "] : partita finita in " + place + ". Vincitore: " + player_win , log_chan)
        del self.games[place]

    def play(self , bot , trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].play(bot , trigger)
        else:
            bot.say(self.strings["not_started"])

    def join(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].join(bot, trigger)
        else:
            bot.say(self.strings['not_started'])

    def print_grid(self , bot , trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].print_grid(bot)
        else:
            bot.say(self.strings["not_started"])



ttt = tttbot()

@plugin.commands("grid" , "gr")
def grid(bot , trigger):
    if trigger.sender in game_chan:
        ttt.print_grid(bot , trigger)

@plugin.commands("ttt" , "TicTacToe" , "tictactoe")
def ttt_start(bot , trigger):
    if trigger.sender in game_chan:
        
        ttt.start(bot , trigger)

@plugin.commands("join" , "jo")
def ttt_join(bot , trigger):
    if trigger.sender in game_chan:
        ttt.join(bot , trigger)

@plugin.commands("adstop")
def adstop(bot , trigger):
    if trigger.sender in game_chan and trigger.group(3) == "ttt":      
        
        ttt.endgame(bot ,trigger , forced = True ,place = trigger.sender ,partquit=False, player_win = None )

@plugin.commands("play" , "pl")
def play(bot , trigger):
    if trigger.sender in game_chan:
        ttt.play(bot , trigger)
        
@plugin.commands("quit" , "qu")
def quit(bot, trigger):
    if trigger.sender in game_chan:
        ttt.endgame(bot, trigger , forced=False,place = trigger.sender, partquit=True, player_win = None)


@plugin.event("PART")
def part(bot, trigger):
    if trigger.sender in game_chan:
        ttt.endgame(bot, trigger ,forced=False,place = trigger.sender, partquit=True, player_win = None)


@plugin.event("QUIT")
def quit_(bot, trigger):
    if trigger.sender in game_chan:
        ttt.endgame(bot, trigger ,forced=False,place = trigger.sender, partquit=True, player_win = None)