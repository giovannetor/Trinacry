"""
various imports. Depends on Sopel. in the future, would like to add a DB for
fiches and stats like the BRISCOLa one
(might need to ask yorick or bruand for this eheh, i'd love a SQlite db)
"""
import random
import threading
import time
from datetime import datetime

import sopel.plugin as module
import sopel.tools as tools
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL, CONTROL_HEX_COLOR

lock = threading.RLock()  # initialise lock

max_player = 10
game_chan = ["#poker" , "#games"]
log_chan = "#trinacry-logs"
poker = CONTROL_BOLD + CONTROL_COLOR + colors.BLACK + "," + colors.WHITE + " P" + CONTROL_COLOR + colors.RED + "," + colors.WHITE + "O" + CONTROL_COLOR + colors.BLACK + "," + colors.WHITE + "K" + CONTROL_COLOR + colors.RED + "," + colors.WHITE + "E" + CONTROL_COLOR + colors.BLACK + "," + colors.WHITE + "R" + CONTROL_COLOR + colors.RED + "," + colors.WHITE + "! " + CONTROL_NORMAL
"""
Here are defined all the strings used in the game.
We have: RULES , GAME STRINGS and HELP.
They'll always be provided in ITALIAN and ENGLISH and translated according to the last .lan command given .
"""

strings_ita = {"nuovo_player": " %s si è unito alla partita di " + poker + " come giocatore: *%s* .",
               "impos_unirsi": "Mi spiace %s , il numero massimo di giocatori è 10. Aspetta fino alla prossima partita :)",
               "gia_dentro": " %s sei già dentro il match di " + poker + " :P ",
               "pronti": "Siamo abbastanza per partire, siete proooonti? XD (.deal per iniziare!)",
               "player_quit": " %s ha abbandonato la partita di " + poker ,
               "cant_stay": "%s non puoi stare ora!",
               "not_change": "%s devi cambiare prima di scommettere!",
               "empty": "%s devi specificare un numero di fiches da scommettere",
               "no_fiches": "%s Non hai abbastanza fiches per scommettere quell'ammontare. Hai solo [%s].",
               "need_more": "%s devi scommettere [%s] fiches in più!",
               "non_abbastanza": "Non puoi giocare da solo, aspetta qualcun altro...",
               "relaunched": "%s ha rilanciato a [%s] !! Raggiungi il nuovo ammontare, o lascia.",
               "iniziato": "La partita è già iniziata.",
               "cant_play": "Non sei dentro la partita, aspetta la prossima per favore :p ",
               "turno": CONTROL_BOLD + " E' il turno di %s.",
               "non_hai": "%s non hai questa carta: {%s}",
               "tue_carte": "Le tue carte: %s",
               "prossimo": CONTROL_BOLD + "Turno di:  ",
               "game_started": poker + " iniziato. Usa .join per unirti.",
               "not_started": "La partita non è ancora iniziata.",
               "game_stopped": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER.",
               "admin_stop": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "UN ADMIN HA TERMINATO LA PARTITA DI " + poker + " DA REMOTO.",
               "on_table": "E' il turno di %s per CAMBIARE.",
               'SB_PLAYER': "%s (%d %s)",
               "cant_move": "Solo un Admin può spostare un match di " + poker + " . ",
               'NEED_CHANNEL': "Dimmi dove spostarmi.",
               'NOT_IN_CHANNEL': "Non sono in %s, quindi non posso spostare la partita di " + poker + " lì.",
               'CHANNEL_IN_USE': "Il canale %s ha già una partita di " + poker + " in corso.",
               'MOVED_FROM': "Note: %s ha spostato una partita di " + poker + " qui da %s.",
               'GAME_MOVED': "%s partita di " + poker + " spostata in %s.",
               "lan_done": CONTROL_COLOR + colors.LIME + "Lingua cambiata in %s .",
               "not_admin": "Solo un admin può cambiare questa impostazione.",
               "wrong_seed": "I semi possono essere Picche(s) , Fiori(c) , Cuori(h) or Quadri(d), non %s .",
               "wrong_value": "I valori vanno da A a J. %s non esiste.",
               "quit_ok": "Il giocatore %s ha lasciato la partita di " + poker + " . La partita deve essere iniziata di nuovo.",
               "fiches": "%s hai [%s] fiches.",
               "bet_done": "Non puoi farlo adesso %s...",
               "bets_done": "Fine delle scommesse. Banco:  ( %s )!!",
               "stay": "%s ha scelto di stare!",
               "winner": CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_BLUE + "%s vince la mano con un fantastico" + CONTROL_COLOR + colors.LIME + " %s !",
               "send_value": "%s ecco cos'hai: <%s>",
               "extra_fiches": "%s ha 0 fiches rimaste. Gli saranno date 100 fiches per continuare a giocare (solo una volta!)",
               "careful": "Attento. Se lasci ora, perderai cosa hai scommesso. Usa .leave per confermare.",
               "leave": "%s ha deciso di lasciare il turno.",
               "bet_time": CONTROL_BOLD + CONTROL_HEX_COLOR + "D9DF01" + "ORA DI SCOMMETTERE!",
               "change_time": CONTROL_BOLD + CONTROL_HEX_COLOR + "1EF004" + "ORA DI CAMBIARE LE CARTE!",
               "game_ended": "Nessun giocatore rimasto! Fine della partita.",
               "new_turn": CONTROL_BOLD + "Sta iniziando un nuovo turno!!",
               "fiches_table": "Ci sono [%s] fiches sul tavolo.",
               "sus_1": "Fine del turno. Il vincitore è...",
               "sus_2": "...un po' di suspense...",
               "left": "%s hai lasciato, aspetta l'inizio del prossimo turno."}

strings_eng = {"nuovo_player": " %s has joined the match of " + poker + " as player: *%s* .",
               "impos_unirsi": "I'm sorry %s , the max number of players is 10. Wait until next match :)",
               "gia_dentro": " %s you are already inside the match of " + poker + " :P ",
               "pronti": "Enough players, are you reeeady to plaaay? XD (.deal to start!)",
               "player_quit": " %s abandoned the match of " + poker + " (wasn't good enough :P) ",
               "cant_stay": "%s you cannot stay now!",
               "not_change": "%s you have to change before betting!",
               "empty": "%s you need to specify a number of fiches to bet :p",
               "no_fiches": "%s you don't have enough fiches to bed that amount! You only have [%s].",
               "need_more": "%s you'll need to bet [%s] fiches more!",
               "non_abbastanza": "Can't play alone, wait for someone else...",
               "relaunched": "%s has relaunched to [%s] !! Reach the new amount, or leave.",
               "iniziato": "Match already started.",
               "cant_play": "You are not inside the match, wait for next one :p ",
               "turno": CONTROL_BOLD + " %s 's turn.",
               "non_hai": "%s you don't have this card: {%s}",
               "tue_carte": "Your cards: %s",
               "prossimo": CONTROL_BOLD + "ON TURN:  ",
               "game_started": poker + " started. use .join to join .",
               "not_started": "Match not started yet.",
               "game_stopped": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "GAME OVER.",
               "admin_stop": CONTROL_BOLD + CONTROL_COLOR + colors.RED + "AN ADMIN TERMINATED THE " + poker + " MATCH FROM REMOTE.",
               "on_table": "%s 's turn to CHANGE.",
               'SB_PLAYER': "%s (%d %s)",
               "cant_move": "Only an admin can move the match of " + poker + " . ",
               'NEED_CHANNEL': "I need a channel name to move to.",
               'NOT_IN_CHANNEL': "I'm not in %s, so I can't move the " + poker + " game there.",
               'CHANNEL_IN_USE': "Channel %s already has a " + poker + " game in progress.",
               'MOVED_FROM': "Note: %s moved an " + poker + " game here from %s.",
               'GAME_MOVED': "%s POKER game moved to %s.",
               "lan_done": CONTROL_COLOR + colors.LIME + "Succesfully changed language to %s .",
               "not_admin": "Only an admin can change this setting.",
               "wrong_seed": "Suits can be Spades(s) , Clubs(c) , Hearts(h) or Diamonds(d), not %s .",
               "wrong_value": "values go from A to J (+ some random numbers :p). %s is not ok.",
               "quit_ok": "The player %s left the " + poker + " match. Match has to be started again.",
               "fiches": "%s you have [%s] fiches.",
               "bet_done": "You can't do this now %s...",
               "bets_done": "Bets ended. On table:  ( %s )!!",
               "stay": "%s chose to stay!",
               "winner": CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_BLUE + "The winner is %s with a wonderful" + CONTROL_COLOR + colors.LIME + " %s !",
               "send_value": "%s here's what you have: <%s>",
               "extra_fiches": "%s has 0 fiches left. He'll be given 10 fiches to continue playing :p",
               "careful": "Careful. If you quit now, you'll lose what you bet before. Use .leave to confirm.",
               "leave": "%s decided to leave this turn.",
               "bet_time": CONTROL_BOLD + CONTROL_HEX_COLOR + "D9DF01" + "IT'S BET TIME!",
               "change_time": CONTROL_BOLD + CONTROL_HEX_COLOR + "1EF004" + "IT'S CHANGE TIME!",
               "game_ended": "No players left! Match is ended.",
               "new_turn": CONTROL_BOLD + "A new turn is starting!!",
               "fiches_table": "Currently there are [%s] fiches on table.",
               "sus_1": "Turn done. The winner is...",
               "sus_2": "...a bit of suspense...",
               "left": "%s you left, wait until next turn."

               }  # STRINGS IN ENGLISH
string_help_ita = "https://webchat.duckie.chat/uploads/d7a1a9f67b032751/paste.txt"
string_help_eng = "https://webchat.duckie.chat/uploads/3150af865aeda59d/paste.txt"

"""
Here i defined all the value given to cards and combinations. Also added a value for seeds, i think it'll be 
useful in order to decide who wins in case of draws.

"""

suits_value = {"S": 0, "C": 1, "D": 2, "H": 3}
suits_render = {"S": " ♤ ", "C": " ♧ ", "D": " ♦ ", "H": " ♥ "}
hand_value = {"High Card": [0, 100], "Pair": [100, 200], "Two Pair": [200, 300], "Three of a kind": [300, 400],
              "Straight": [400, 500],
              "Flush": [500, 600], "Full house": [600, 700], "Poker": [700, 800], "Straight flush": [800, 900],
              "Royal flush": [900, 1000]
              }

values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

card_values = {"A": 14, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
               "9": 9, "10": 10, "J": 11, "Q": 12, "K": 13}

suits = ["S", "H", "C", "D"]


class PokerGame:
    def __init__(self, trigger):
        self.strings = strings_eng
        self.string_help = string_help_eng  
     
        self.starter = trigger.nick
        self.channel = trigger.sender
        self.deck = []
        self.players = {
            self.starter: {"cards": [], "hasdone": False, "change": False, "bet": False, "fiches": 1000, "allin": False,
                           "left": False}}
        self.playerOrder = [self.starter]
        self.currentPlayer = 0
        self.previousPlayer = None
        self.way = 1
        self.startTime = None
        self.dealt = False
        self.turncounter = 0
        self.startcont = 0
        self.changecounter = 0
        self.betcounter = 0
        self.maxbet = 0
        self.betsdone = {self.starter: 0}
        self.ontable = 0
        self.idkcounter = 0
        self.secondcounter = 0
        self.listout = {}
        self.contatore = 0
        self.removecard = []
        self.bohcounter = 0

    def send_ontable(self, bot, trigger):
        bot.say(self.strings["fiches_table"] % str(self.ontable))

    def join(self, bot, trigger):  # joins to the match
        if self.startcont == 0:
            bot.write(['MODE', trigger.sender, '+v', self.starter])  # to let the starter join too
            self.startcont += 1
        with lock:
            if trigger.nick not in self.players:  # if the player is not in the game
                if len(self.players) == max_player:
                    bot.say(self.strings["impos_unirsi"] % trigger.nick)  # match full
                    return
                if self.dealt:
                    bot.notice(self.strings["cant_play"], trigger.nick)
                    print("problema in JOIN")  # if game already dealt, cannot join
                    return
                bot.write(['MODE', trigger.sender, '+v', trigger.nick])  # playing players will be voiced
                self.players[trigger.nick] = {"cards": [], "hasdone": False, "change": False, "bet": False,
                                              "fiches": 1000, "allin": False,
                                              "left": False}  # initiates the dict, same for each player ("hasdone" is useless iirc)
                self.betsdone[trigger.nick] = 0  # add player to bets dict
                self.playerOrder.append(trigger.nick)  # add player to players order list (maybe to remove?)

                bot.say(self.strings['nuovo_player'] % (trigger.nick, str(self.playerOrder.index(trigger.nick) + 1)))
                if len(self.players) > 1 and len(self.players) < 3:
                    bot.say(self.strings['pronti'])  # at least 2 players, ready to deal

                self.startcont += 1
            else:
                bot.say(self.strings["gia_dentro"] % trigger.nick)  # player already in

    def leave(self, bot, trigger):
        with lock:  # this function will allow a player to leave but still being in game TO DOOOOO!!!!
            player = trigger.nick
            if player not in self.players:
                return
            if self.players[player]["left"] == True:
                bot.say(self.strings["left"] % player)
                return

            bot.say(self.strings["leave"] % player)
            self.players[player]["left"] = True

            if self.players[trigger.nick]["change"] == True:  # stay during CHANGE
                self.players[trigger.nick]["change"] = False
                self.inc_player()

                if trigger.nick != self.playerOrder[-1]:  # increase the player.
                    self.show_on_turn(bot)  # shows who's the turn now
                self.idkcounter += 1
                print("il idkcounter è stato aggiornato a " + str(self.idkcounter))
                if self.idkcounter >= len(self.players):
                    self.secondcounter += 1
                    bot.say(self.strings["bet_time"])
                    for i in self.players:
                        if self.players[i]["left"] != True:
                            self.players[i]["bet"] = False

            if self.players[trigger.nick]["bet"] == False:  # stay during BETS
                self.players[trigger.nick]["bet"] = True
                for i in self.players:  # when this for will return true, self.betsdone can have place.
                    if self.players[i]["bet"] == False:
                        self.bohcounter += 1
                if self.bohcounter == 0:
                    self.betdone(bot, trigger)  # check the function

        self.bohcounter = 0
        self.temp_remove_player(bot, trigger)

    def temp_remove_player(self, bot, trigger):
        player = trigger.nick
        with lock:
            player1, value = player, self.players[player]
            self.listout[player1] = value
            self.currentPlayer -= 1
            self.players.pop(player)
            self.playerOrder.remove(player)

    def quit(self, bot, trigger,
             partquit=False):  # remove the player from the match. If there's only one player left, the match is ended.
        player = trigger.nick
        if player not in self.players:
            return
        if not partquit:
            if self.contatore == 0:
                bot.say(self.strings["careful"])
                self.contatore += 1
                return
            self.contatore = 0

        with lock:
            bot.say(self.strings['player_quit'] % player)
            self.remove_player(bot, player)
            if len(self.players) == 1:
                if not self.dealt:
                    bot.say(self.strings["game_ended"])
                    pokerbot.game_ended(bot, trigger)
                else:
                    if len(self.players) <= 1:
                        self.decidewin(bot, trigger,
                                       forced=True)  # if a player leaves during a match, and there's only one player left,
                        # the points are given to the only one left. then the game ends.

    def remove_player(self, bot, player):  # guess by the name :p
        with lock:
            self.players.pop(player)
            self.playerOrder.remove(player)

    def deal(self, bot, trigger):  # deal the game. everyone in the game can do it, owner not required.
        if trigger.nick not in self.players:
            bot.notice(self.strings["cant_play"], trigger.nick)
            print("problema in DEAL")
            return
        if len(self.players) < 2:
            bot.say(self.strings['non_abbastanza'])
            return
        if len(self.deck):
            bot.say(self.strings['iniziato'])  # means the match is already going on, return
            return

        with lock:
            self.startTime = datetime.now()  # starts the time counter
            self.deck = self.create_deck()  # create the deck (check self.create_deck )
            for player in self.players:
                while len(self.players[player]["cards"]) < 5:
                    self.players[player]["cards"].append(self.get_card(bot))  # gives each player 5 cards.
            self.dealt = True
            self.currentPlayer = 0  # 1st player is chosen randomly
            # self.show_on_turn(bot)   # shows who's on turn (NEEDS CORRECTIONS!)
            for player in self.players:
                self.send_cards(bot, player)  # shows to each player the cards at the beginning of the match.
            bot.say(self.strings["bet_time"])

    def stay(self, bot, trigger):  # decides if to stay during a bet or a change phase
        canstay = True
        giocatore = trigger.nick
        if trigger.nick not in self.players:
            bot.say(self.strings["cant_play"])
            return
        if self.players[giocatore]["left"] == True:
            bot.say(self.strings["left"] % giocatore)
            return

        if self.players[trigger.nick]["change"] == True:  # stay during CHANGE
            self.players[trigger.nick]["change"] = False
            self.inc_player()

            if trigger.nick != self.playerOrder[-1]:  # increase the player.
                self.show_on_turn(bot)  # shows who's the turn now
            self.idkcounter += 1
            print("il idkcounter è stato aggiornato a " + str(self.idkcounter))
            if self.idkcounter >= len(self.players):
                self.secondcounter += 1
                bot.say(self.strings["bet_time"])
                for i in self.players:
                    if self.players[i]["left"] != True:
                        self.players[i]["bet"] = False

        elif self.players[trigger.nick]["bet"] == False:  # stay during BETS
            if self.betsdone[giocatore] < self.maxbet:  # if another player already betted, you cannot stay.
                canstay = False

            if canstay:
                self.players[giocatore]["bet"] = True
                bot.say(self.strings["stay"] % trigger.nick)
            else:
                bot.say(self.strings["cant_stay"] % trigger.nick)
                return
            for i in self.players:  # when this for will return true, self.betsdone can have place.
                if self.players[i]["bet"] == False:
                    return False
            self.betdone(bot, trigger)  # check the function
        else:
            bot.say(self.strings["cant_stay"] % trigger.nick)
            return

    def bet(self, bot, trigger):  # allows the player to bet
        if trigger.nick not in self.players:  # If the player is NOT part of the game
            bot.notice(self.strings['cant_play'], trigger.nick)
            print("problema in BET")
            return
        if self.players[trigger.nick]["left"] == True:
            bot.say(self.strings["left"] % trigger.nick)
            return
        if self.players[trigger.nick]["change"] and self.betcounter < 1:  # if it's change time, you cannot bet.
            bot.say(self.strings["not_change"] % trigger.nick)
            return
        if self.players[trigger.nick]["bet"] == True:  # if you've already betted, you cannot bet anymore.
            bot.say(self.strings["bet_done"] % trigger.nick)
            return
        # if not self.players[trigger.nick]["hasdone"]:
        #    bot.say(self.strings["not_done"] % trigger.nick)
        #    return
        if not self.betsdone:
            self.maxbet = int(trigger.group(3))  # If there's no bet done, the 1st one becomes the MAX.
        try:
            bet = int(trigger.group(3))
        except:  # if args is empty, return
            bot.say(self.strings["empty"] % trigger.nick)
            return

        if bet > self.players[trigger.nick]["fiches"]:  # if you don't have enough fiches, return.
            """
            THIS WILL BE CHANGED TO ALLOW THE "ALL IN" FUNCTION.
            """
            bot.say(self.strings["no_fiches"] % (trigger.nick, str(self.players[trigger.nick]["fiches"])))
            return

        if (bet + self.betsdone[trigger.nick]) < self.maxbet:  # If player did not bet more than previous player
            bot.say(self.strings["need_more"] % (
            trigger.nick, str(self.maxbet - bet)))  # tells you how many fiches more you need
            self.players[trigger.nick]["bets"] = False
            return

        self.players[trigger.nick]["fiches"] -= bet  # remove the fiches from the player's and adds them to the table.
        self.betsdone[trigger.nick] += bet
        self.ontable += bet

        if bet > self.maxbet:  # If player bet more than previous player, a new Max bet is set and every player has to
            # either reach it or leave the game. "ALL IN" players will just stay in game
            self.maxbet = bet
            bot.say(self.strings["relaunched"] % (trigger.nick, str(bet)))
            for player in self.players:
                self.players[player]["bet"] = False
            self.players[trigger.nick]["bet"] = True
        else:
            self.players[trigger.nick]["bet"] = True
        for i in self.players:
            if self.players[i]["bet"] == False:  # will return false until everyone has left, or betted a fair amount
                return False
        self.betdone(bot, trigger)
        return True

    def betdone(self, bot,
                trigger):  # sets the maxbet to 0 again. starts the change phase IF the 1st bet took place (not the 2nd)
        self.maxbet = 0
        bot.say(self.strings["bets_done"] % str(self.ontable))
        if self.secondcounter == 0:
            bot.say(self.strings["change_time"])
            for player in self.players:
                if self.players[player]["left"] != True:
                    self.players[player]["change"] = True
            self.show_on_turn(bot)
        else:  # if this functin gets called after the 2nd bet, the winner is decided
            self.decidewin(bot, trigger)  # see the function below

    def decidewin(self, bot, trigger, forced=False):
        punteggio = 0
        if not forced:
            nomewin, punteggio = self.playerOrder[0], self.hand_value_def(bot, self.playerOrder[0])
            for player in self.players:
                if self.hand_value_def(bot, player) > punteggio and self.players[player][
                    "left"] == False:  # checks who has the most valuable hand.
                    nomewin, punteggio = player, self.hand_value_def(bot, player)
                else:
                    print("cicciole")

                # elif self.hand_value_def(bot , trigger) == punteggio:
                #    nomewin , punteggio = self.decide_draw(bot , nomewin , player)
                """
                decide_draw will have to decide who wins the draw, and return the result as a tuple (name , score)
                """

        else:  # the forced occours when there's only one player left in game. triggered by quit.
            for i in self.players:
                nomewin, punteggio = i, self.hand_value_def(bot, i)  # used a "for" cuz i'm lazy :p

        bot.say(self.strings["sus_1"])
        time.sleep(3)
        bot.say(self.strings["sus_2"])
        time.sleep(3)
        for val in hand_value:
            if punteggio in range(hand_value[val][0], hand_value[val][1]):
                punteggio = val
        bot.say(self.strings["winner"] % (nomewin, str(punteggio)))
        time.sleep(1)
        self.players[nomewin]["fiches"] += self.ontable
        self.reboot(bot, trigger)

    def reboot(self, bot, trigger):
        with lock:
            for player in self.listout:
                self.players[player] = self.listout[player]
                self.playerOrder.insert(0, player)
        if len(self.players) >= 2:
            self.create_deck()  # a new deck is created each time
            self.maxbet = 0
            bot.say(self.strings["new_turn"])
            for i in self.players:
                self.players[i]["left"] = False
                self.players[i]["bet"] = False
                self.players[i]["change"] = False
                self.players[i]["hasdone"] = False
                if self.players[i]["fiches"] == 0:  # if a player has no fiches left, 10 are kindly given to continue :p
                    self.players[i]["fiches"] = 100
                    bot.say(self.strings["extra_fiches"] % i)
                self.players[i]["cards"] = []
                while len(self.players[i]["cards"]) < 5:
                    self.players[i]["cards"].append(self.get_card(bot))

            self.ontable = 0
            self.idkcounter = 0
            self.secondcounter = 0
            self.changecounter = 0
            self.betcounter = 0
            self.listout = {}
            bot.say(self.strings["bet_time"])

            for player in self.players:
                self.send_cards(bot, player)

            return False

        else:
            pokerbot.game_ended(bot, trigger)  # if the players left are <2, ends the game.
            return True

    def change(self, bot, trigger):
        # makes a player change a N number of cards
        if trigger.nick not in self.players:
            bot.notice(self.strings['cant_play'], trigger.nick)
            print("problema in CHANGE")
            return
        if self.players[trigger.nick]["left"] == True:
            bot.say(self.strings["left"] % trigger.nick)
            return
        if trigger.nick != self.playerOrder[self.currentPlayer]:
            bot.say(self.strings['turno'] % self.playerOrder[self.currentPlayer])
            return
        if not self.players[trigger.nick]["change"]:
            bot.say(self.strings["not_change"] % trigger.nick)
            return

        try:
            for card in trigger.group(2).split():  # all the cards must go in a line, separated by a space.
                seed, number = card[-1].upper(), card[
                                                 :-1].upper()  # here, he takes commands like .change 4c and creates the card "4C"
                if seed not in suits:
                    seed, number = card[:-1].upper(), card[-1].upper()
                elif number not in values:  # allows both .change 4c and .change c4
                    seed, number = card[:-1].upper(), card[-1].upper()
                if seed in suits and number in values:
                    searchcard = number + seed  # important!! the output card must always have number + seed. The card in the format e.g. "4C" is called searchcard

                else:
                    if seed not in suits:
                        bot.notice(self.strings["wrong_seed"] % seed, trigger.nick)

                    elif number not in values:  # if something is not working, explains what
                        bot.notice(self.strings["wrong_value"] % number, trigger.nick)

                    return  # card not existing

                with lock:
                    if searchcard not in self.players[trigger.nick]["cards"]:
                        bot.notice(self.strings['non_hai'] % (trigger.nick, searchcard), trigger.nick)
                        return
                    if searchcard not in self.removecard and searchcard in self.players[trigger.nick]["cards"]:
                        self.removecard.append(searchcard)
                    # self.players[trigger.nick]["cards"].remove(searchcard)  # removes from the player's card list the card in the "4C" forma

        except (AttributeError):
            return
        for card in self.removecard:
            try:
                self.players[trigger.nick]["cards"].remove(card)
            except:
                print("L'errore è la carta " + card)

        while len(self.players[trigger.nick]["cards"]) < 5:
            self.players[trigger.nick]["cards"].append(self.get_card(bot))

        self.send_cards(bot, trigger)
        self.removecard = []
        self.players[trigger.nick]["change"] = False
        self.inc_player()
        if trigger.nick != self.playerOrder[-1]:  # increase the player.
            self.show_on_turn(bot)  # shows who's the turn now
        self.idkcounter += 1
        print("il idkcounter è stato aggiornato a " + str(self.idkcounter))
        if self.idkcounter >= len(self.players):
            self.secondcounter += 1
            bot.say(self.strings["bet_time"])
            for i in self.players:
                if self.players[i]["left"] != True:
                    self.players[i]["bet"] = False

    def fiches(self, bot, trigger):
        if trigger.nick in self.players:
            bot.notice(self.strings["fiches"] % (trigger.nick, str(self.players[trigger.nick]["fiches"])), trigger.nick)

    def send_value(self, bot, trigger):
        if trigger.nick in self.players:
            bot.notice(self.strings["send_value"] % (trigger.nick, str(self.hand_value_def(bot, trigger))),
                       trigger.nick)

    def hand_value_def(self, bot, trigger):
        try:
            giocatore = trigger.nick
        except:
            giocatore = trigger
        mazzo = []
        for card in self.players[giocatore]["cards"]:
            mazzo.append(card)
        mazzo.sort(key=lambda numero: int(card_values[numero[:-1]]))
        valori_possibili = [
            self.is_scala(mazzo), self.is_colore(mazzo), self.is_doublecouple(mazzo),
            self.is_full(mazzo), self.is_poker_tris_couple(mazzo)
        ]
        valore_top = max(valori_possibili)
        #    for val in hand_value:
        #        if valore_top in range(hand_value[val][0] , hand_value[val][1]):
        return valore_top

    """
    Main functions return a number.
    sub functions return a True False.
    The winner will be the one having the max hand value.    
    """

    def is_scala(self, mazzo):

        ok_scala = 0
        for carta in range(1, 5):
            if int(card_values[mazzo[carta][:-1]]) == int(card_values[mazzo[carta - 1][:-1]]) + 1:
                ok_scala += 1
        if ok_scala == 4:
            if self.is_scala_colore(mazzo):
                if self.is_scala_reale(mazzo):
                    return 900
                return 800
            return 400
        else:
            return 0

    def is_scala_colore(self, mazzo):
        ok_colore = 0
        for carta in range(1, 5):
            if mazzo[carta][-1] == mazzo[carta - 1][-1]:
                ok_colore += 1
        if ok_colore == 4:
            return True
        else:
            return False

    def is_scala_reale(self, mazzo):
        if mazzo[-1][0] == "A":
            return True
        else:
            return False

    def is_colore(self, mazzo):
        ok_coloronly = 0
        for carta in range(1, 5):
            if mazzo[carta][-1] == mazzo[carta - 1][-1]:
                ok_coloronly += 1
        if ok_coloronly == 4:
            return 500
        else:
            return 0

    def is_doublecouple(self, mazzo):
        if mazzo[0][:-1] == mazzo[1][:-1] and mazzo[2][:-1] == mazzo[3][:-1] != mazzo[4][:-1]:
            return 200
        elif mazzo[0][:-1] == mazzo[1][:-1] and mazzo[2][:-1] != mazzo[3][:-1] == mazzo[4][:-1]:
            return 200
        elif mazzo[0][:-1] != mazzo[1][:-1] == mazzo[2][:-1] and mazzo[3][:-1] == mazzo[4][:-1]:
            return 200
        else:
            return 0

    def is_poker_tris_couple(self, mazzo):
        ok_ = {}
        for carta in mazzo:
            if carta[:-1] in ok_:
                ok_[carta[:-1]] += 1
            else:
                ok_[carta[:-1]] = 1
        massimo = max(ok_.values())
        if massimo == 4:
            return 700
        elif massimo == 3:
            return 300
        elif massimo == 2:
            return 100
        else:
            return 0

    def is_full(self, mazzo):
        if mazzo[0][:-1] == mazzo[1][:-1] == mazzo[2][:-1] and mazzo[3][:-1] == mazzo[4][:-1]:
            return 600
        elif mazzo[0][:-1] == mazzo[1][:-1] and mazzo[2][:-1] == mazzo[3][:-1] == mazzo[4][:-1]:
            return 600
        else:
            return 0

    def inc_player(self):
        self.previousPlayer = self.currentPlayer  # if not all the players have played a card, the turn goes on as normal.
        self.currentPlayer += 1
        if self.currentPlayer >= len(self.players):
            self.currentPlayer = 0

    def show_on_turn(self, bot):  # shows the cards atm on the table.
        with lock:
            giocatore = self.playerOrder[self.currentPlayer]
            if self.players[giocatore]["left"]:
                self.inc_player()
                giocatore = self.playerOrder[self.currentPlayer]
            bot.say(self.strings['on_table'] % (giocatore))
            self.send_cards(bot, self.playerOrder[self.currentPlayer])

    def send_cards(self, bot, trigger):  # shows the cards in your hand, and the match's briscola card
        with lock:
            if not self.startTime:
                bot.notice(self.strings['not_started'], trigger.nick)
                return
            try:
                if trigger.nick not in self.players:
                    bot.notice(self.strings['cant_play'], trigger.nick)
                    print("problema in SEND CARDS 1")
                    return
            except:
                if trigger not in self.players:
                    bot.notice(self.strings['cant_play'], trigger.nick)
                    print("problema in SEND CARDS 2")
                    return

            cards = []
            try:
                for i in self.players[trigger]["cards"]:
                    cards.append(i)
            except:
                for i in self.players[trigger.nick]["cards"]:
                    cards.append(i)
                # trova le carte nel dizionario, renderizzate sotto V
            try:
                bot.notice("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", trigger)
                bot.notice(
                    self.strings['tue_carte'] % (str(self._render_colored_cards(self.players[trigger]["cards"]))),
                    trigger)
                bot.notice("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", trigger)
            except:
                bot.notice("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", trigger.nick)
                bot.notice(
                    self.strings['tue_carte'] % (str(self._render_colored_cards(self.players[trigger.nick]["cards"]))),
                    trigger.nick)
                bot.notice("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=", trigger.nick)

    def create_deck(self):
        new_deck = []
        for seed in suits:
            for valores in values:
                if card_values[valores] >= 11 - len(self.players):
                    new_deck.append(valores + seed)
        random.shuffle(new_deck)
        random.shuffle(new_deck)
        random.shuffle(new_deck)
        return new_deck

    def get_card(self, bot):
        with lock:
            if not self.deck:
                self.deck = self.create_deck()
            ret = self.deck.pop(0)
        return ret

    @staticmethod
    def _render_colored_cards(cards):  # renderizza colori carte
        black_code = colors.BLACK
        red_code = colors.RED
        white_code = colors.WHITE
        with lock:
            ret = []
            cards.sort(key=lambda numero: int(card_values[numero[:-1]]))
            for card in cards:
                if card[-1] == "D":
                    ret.append(
                        CONTROL_COLOR + black_code + "," + red_code + "[" +
                        CONTROL_COLOR + black_code + "," + red_code + card[:-1]
                        + CONTROL_COLOR + black_code + "," + red_code + suits_render[card[-1]] +
                        CONTROL_COLOR + black_code + "," + red_code + "]" +
                        CONTROL_NORMAL + "   "
                    )

                if card[-1] == "C":  # colora le altre carte, abbastanza ez
                    ret.append(
                        CONTROL_COLOR + white_code + "," + black_code + "[" +
                        CONTROL_COLOR + white_code + "," + black_code + card[:-1]
                        + CONTROL_COLOR + white_code + "," + black_code + suits_render[card[-1]] +
                        CONTROL_COLOR + white_code + "," + black_code + "]" +
                        CONTROL_NORMAL + "   "
                    )

                if card[-1] == "S":
                    ret.append(
                        CONTROL_COLOR + white_code + "," + black_code + "[" +
                        CONTROL_COLOR + white_code + "," + black_code + card[:-1]
                        + CONTROL_COLOR + white_code + "," + black_code + suits_render[card[-1]] +
                        CONTROL_COLOR + white_code + "," + black_code + "]" +
                        CONTROL_NORMAL + "   "
                    )

                if card[-1] == "H":
                    ret.append(
                        CONTROL_COLOR + black_code + "," + red_code + "[" +
                        CONTROL_COLOR + black_code + "," + red_code + card[:-1]
                        + CONTROL_COLOR + black_code + "," + red_code + suits_render[card[-1]] +
                        CONTROL_COLOR + black_code + "," + red_code + "]" +
                        CONTROL_NORMAL + "   "
                    )

        return ''.join(ret) + CONTROL_NORMAL


class PokerBot:
    def __init__(self):
        self.games = {}
        self.strings = strings_eng
        self.contatore = 0

    def ontable(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.send_ontable(bot, trigger)

    def language(self, bot, trigger):
        try:
            self.games[trigger.sender]
        except:
            #bot.say("Need to start the game first.")
            return
        game = self.games[trigger.sender]

        if game.dealt:
            bot.say("Can't change now.")
            return
        else:
            if trigger.group(3) == "italiano":
                game.strings = strings_ita

                game.string_help = string_help_ita
                bot.say(self.strings["lan_done"] % trigger.group(3))
                self.strings = strings_eng
            elif trigger.group(3) == "english":
                game.strings = strings_eng

                game.string_help = string_help_eng
                bot.say(self.strings["lan_done"] % trigger.group(3))
                self.strings = strings_ita

    def start(self, bot, trigger):
        if trigger.sender in self.games:
            self.join(bot, trigger)
        else:
            self.games[trigger.sender] = PokerGame(trigger)
            bot.say(self.strings['game_started'])

    def leave(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].leave(bot, trigger)

    def stay(self, bot, trigger):
        self.contatore = 0
        if trigger.sender in self.games:
            self.games[trigger.sender].stay(bot, trigger)

    def send_value(self, bot, trigger):
        self.contatore = 0
        if trigger.sender in self.games:
            self.games[trigger.sender].send_value(bot, trigger)

    def join(self, bot, trigger):
        if trigger.sender in self.games:
            self.games[trigger.sender].join(bot, trigger)
        #else:
        #    bot.say(self.strings['not_started'] )

    def deal(self, bot, trigger):
        if trigger.sender not in self.games:
            #bot.say(self.strings['not_started'] )
            return
        self.games[trigger.sender].deal(bot, trigger)

    def stop(self, bot, trigger, forced=False):
        chan = trigger.sender  # tools.Identifier(trigger.sender)
        if chan not in self.games:
            # bot.notice(self.strings['not_started'] +  "STOP", trigger.nick)
            return
        game = self.games[chan]
        if trigger.admin or forced:
            if not forced:
                bot.say(self.strings['game_stopped'])
                bot.say("[" + poker + "] : Admin ha fermato una partita in " + trigger.sender, log_chan)
                if trigger.sender != chan:
                    bot.say(self.strings['admin_stop'], chan)
                else:
                    bot.say("Game stopped by admin.", chan)

            else:
                if not game.dealt:
                    bot.say(self.strings["quit_ok"] % (trigger.nick))
                    for player in game.players:
                        bot.write(['MODE', trigger.sender, '-v', player])
                    del self.games[trigger.sender]
                    return

            for player in game.players:
                bot.write(['MODE', trigger.sender, '-v', player])
            self.game_ended(bot, trigger)
            # del self.games[chan]
        else:
            bot.say("Can't be stopped.")

    def quit(self, bot, trigger, partquit=False):
        try:
            gioco = self.games[trigger.sender]
        except:
            print("canale non in lista")
            return
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.quit(bot, trigger, partquit)
        bot.write(['MODE', trigger.sender, '-v', trigger.nick])

        if len(gioco.players) < 2:
            self.stop(bot, trigger, forced=True)

    def change(self, bot, trigger):
        self.contatore = 0
        game = self.games[trigger.sender]
        if trigger.sender not in self.games:
            return
        game.change(bot, trigger)

    def bet(self, bot, trigger):
        self.contatore = 0
        game = self.games[trigger.sender]
        if trigger.sender not in self.games:
            return
        game.bet(bot, trigger)

    def fiches(self, bot, trigger):
        self.contatore = 0
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.fiches(bot, trigger)

    def send_cards(self, bot, trigger):
        self.contatore = 0
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.send_cards(bot, trigger.nick)

    def send_counts(self, bot, trigger):
        if trigger.sender not in self.games:
            return
        game = self.games[trigger.sender]
        game.send_counts(bot)

    def game_ended(self, bot, trigger):

        with lock:
            game = self.games[trigger.sender]
            try:
                for player in game.players:
                    bot.write(['MODE', trigger.sender, '-v', player])
            except:
                print("Provato a cancellare player inesistente.")
            del self.games[trigger.sender]

    def move_game(self, bot, trigger):
        who = trigger.nick
        oldchan = trigger.sender
        newchan = tools.Identifier(trigger.group(3))
        if newchan[0] != '#':
            newchan = tools.Identifier('#' + newchan)
        if oldchan not in self.games:
            bot.reply(self.strings['not_started'] + "MOVEGAME")
            return

        if not trigger.admin:
            bot.reply(self.strings['cant_move'])
            return
        if not newchan:
            bot.reply(self.strings['NEED_CHANNEL'])
            return
        if newchan == oldchan:
            return
        if newchan.lower() not in bot.privileges:
            bot.reply(self.strings['NOT_IN_CHANNEL'] % newchan)
            return
        if newchan in self.games:
            bot.reply(self.strings['CHANNEL_IN_USE'] % newchan)
            return
        game = self.games.pop(oldchan)
        self.games[newchan] = game
        game.game_moved(bot, who, oldchan, newchan)


pokerbot = PokerBot()


@module.commands("poker" , "pk")
def poker1(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.start(bot, trigger)
        string = "[" + poker + "] : START iniziata in " + trigger.sender
        bot.say(string, log_chan)


@module.commands("change" , "chg")
@module.example(".change 4a 5s 7w")
def change(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.change(bot, trigger)


@module.commands("cards" , "ca")
def cards(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.send_cards(bot, trigger)


@module.commands("deal" , "de")
@module.example(".deal")
def deal(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.deal(bot, trigger)
        bot.say("[" + poker + "] : DEAL in " + trigger.sender, log_chan)


@module.commands("bet")
@module.example(".bet 50")
def bet(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.bet(bot, trigger)


@module.commands("join" , "jo")
@module.example(".join")
def join(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.join(bot, trigger)


@module.commands("quit" , "qu")
@module.example(".leave")
def quit(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.quit(bot, trigger)


@module.commands("leave" , "le")
def leave(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.leave(bot, trigger)


@module.commands("stay" , "st")
def stay(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.stay(bot, trigger)


@module.commands('adstop')
@module.example(".adstop")
@module.priority('high')
def pokerstop(bot, trigger):
    if trigger.sender in game_chan and trigger.group(3) == "poker":
        pokerbot.stop(bot, trigger)
        


@module.commands("fiches")
def fiches(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.fiches(bot, trigger)


@module.commands("value" , "vl")
def value(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.send_value(bot, trigger)


@module.commands('pokergames', "pkgame")
@module.priority('high')
@module.require_admin
def brisgames(bot, trigger):
    chans = []
    active = 0
    pending = 0
    with lock:
        for chan, game in pokerbot.games.items():
            if game.startTime:
                chans.append(chan)
                active += 1
            else:
                chans.append(chan + " (pending)")
                pending += 1
    if not len(chans):
        bot.say('No ' + poker + ' games in progress, %s.' % trigger.nick)
        return
    g_active = "channel" if active == 1 else "channels"
    g_pending = "channel" if pending == 1 else "channels"
    chanlist = ", ".join(chans[:-2] + [" and ".join(chans[-2:])])
    bot.reply(
        poker + " is pending deal in %d %s and in progress in %d %s: %s."
        % (pending, g_pending, active, g_active, chanlist))


@module.commands("language", "lan")
@module.example(".language italiano", ".lan english")
def language(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.language(bot, trigger)


@module.commands("help")
@module.example(".pokerhelp italiano", "pokerhelp english")
def pokerhelp(bot, trigger):
    if trigger.sender in game_chan and trigger.group(3).lower == "poker":
        if trigger.group(4).lower == "italiano" or trigger.group(4).lower == "it":
            bot.notice("GUIDA: " + string_help_ita, trigger.nick)
        else:
            bot.notice("GUIDE: " + string_help_eng, trigger.nick)


@module.commands("ontable" , "ot")
def ontable(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.ontable(bot, trigger)


@module.event("PART")
def part(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.quit(bot, trigger, partquit=True)


@module.event("QUIT")
def quit_(bot, trigger):
    if trigger.sender in game_chan:
        pokerbot.quit(bot, trigger, partquit=True)
