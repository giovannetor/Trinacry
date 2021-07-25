import os
import random
import threading
import time
from datetime import datetime
from enum import Enum
from io import StringIO
from pathlib import Path

import sopel.plugin as plugin
import sopel.tools as tools
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL

X = CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_CYAN + CONTROL_NORMAL
O = CONTROL_BOLD + CONTROL_COLOR + colors.RED + CONTROL_NORMAL
gridlist = ["A1" , "A2"  , "A3" , "B1"   ,"B2"  , "B3" , "C1" , "C2", "C3"]

log_chan = "#trinacry-logs"
game_chan = ["#TicTacToe"]
lock = threading.RLock()
max_player = 2

class tttgame:
    def __init__(self , trigger):
        self.strings = strings_eng
        self.string_help = string_help_eng
        self.rules = rules_eng
        self.starter = trigger.nick
        self.channel = trigger.sender
        self.players = {self.starter: {"squares" : [] , "sign" : X}}  # player's dict. each player will have a card list
        self.playerOrder = [self.starter]  # player order. it will mostly be used paired with self.currentPlayer
        self.currentPlayer = 0
        self.startTime = None
        self.dealt = False
        self.dicgrid =  {"A1" : "/" , "A2" : "/" , "A3" : "/",
                         "B1" : "/"  ,"B2" : "/" , "B3" : "/" ,
                         "C1" : "/" , "C2" : "/" , "C3" : "/"}

    def join(self, bot, trigger):
        with lock:
            if trigger.nick not in self.players:  # if the player is not in the game
                if len(self.players) == max_player:
                    bot.say(self.strings["impos_unirsi"] % trigger.nick)  # match full
                    return
                if self.dealt:
                    bot.say(self.strings["cant_play"])
                    return
                self.players[trigger.nick]= {"squares" : [] , "sign" : O}  # add player to players dict
                self.playerOrder.append(trigger.nick)  # add player to players order list
                bot.say(self.strings['inizio'])  # at least 2 players, ready to deal
                self.dealt = True
            else:
                bot.say(self.strings["gia_dentro"] % trigger.nick)  # player already in

    def play(self, bot, trigger):
        player = trigger.nick
        if player not in self.players:
            bot.notice(self.strings['cant_play'], player)
            return
        if player != self.playerOrder[self.currentPlayer]:
            bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
            return

        cmd = trigger.group(3).upper

        if cmd[0] not in "ABC":
            bot.say(self.strings["noletter"] % cmd)
            return

        try: int(cmd[1])
        except:  bot.say(self.strings["nonumber"] % cmd[1])

        if cmd not in gridlist:
            bot.say(self.strings["nogrid"] % cmd)
            return

        cp = self.check_possible(player , cmd)
        if cp == 0:
            bot.say(self.strings["già_tuo"])
            return
        elif cp == 2:
            bot.say(self.strings["altro"])
            return

        bot.say(self.strings["ok"])

        self.players[player]["squares"].append(cmd)

        self.print_grid(bot)

        if self.checkwin(player):
            bot.say(self.strings["win"] % player)
        else:
            self.currentPlayer += 1
            if self.currentPlayer > 1:
               self.currentPlayer = 0
            bot.say(self.strings["next_turn"])


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
        if gridlist[cmd] == self.players[player]["sign"]:
            return 0
        else:
            if gridlist[cmd] == "/":
                return 1
            else:
                return 2

    def print_grid(self , bot):
        dicgrid = self.dicgrid
        bot.say(dicgrid["A1"]+ "   |   " + dicgrid["A2"] + "   |   " + dicgrid["A3"])
        bot.say("------------------------------")
        bot.say(dicgrid["B1"]+ "   |   " + dicgrid["B2"] + "   |   " + dicgrid["B3"])
        bot.say("------------------------------")
        bot.say(dicgrid["C1"]+ "   |   " + dicgrid["C2"] + "   |   " + dicgrid["C3"])

@plugin.commands("grid")
def grid(bot):
    tttgame.print_grid(bot)
