import sopel.plugin as module
import sopel.tools as tools     #import the 2 sopel modules required


strings = {
    "limite" : "Mi spiace, ma hai raggiunto il limite massimo di uova ottenibili! / I'm sorry, but you can't claim any more eggs!",
    "egg" : "Ecco il tuo UOVO / Here's you EGG %s  https://usercontent.twoopy.nl/6b4f281c5a446791/image.png .",
    "left" : "Ti sono rimasti %s tentativi / You've got %s attempts left.",
    "adminegg" : "Hai ricevuto un uovo da %s. / You received an egg from %s . https://usercontent.twoopy.nl/6b4f281c5a446791/image.png",
    "admineggself" : "Ti sei dato un uovo da solo %s (monello!)"
}   # The bot is designed to stay in #italiano, but we expect people from everywhere to come to find the egg. The strings
    # are both in Italian and English.

class easteregg:    # everything is inside a single little class.
    
    def __init__(self):
        self.user = {}   # this dict will store the user's nick of whoever uses the .easteregg command. Being a dict
                         # inside the code and not in a db, the datas will vanish if the bot will reload.

    def egg(self , bot , trigger):     # main function of the bot. triggered by .easteregg , insert the trigger in
        if trigger.nick not in self.user:  # self.user and starts the counter.
            self.user[trigger.nick] = 0
        if self.user[trigger.nick] >= 3:
            bot.notice(strings["limite"] , trigger.nick)  # the limit of 3 eggs is to prevent flood in channel. anyway,
            return                                        # the image will be provided via notice.
        self.user[trigger.nick] += 1
        bot.notice(strings["egg"] % (trigger.nick) , trigger.nick)
        bot.notice(strings["left"] % ( str(3 - self.user[trigger.nick]) , str(3 - self.user[trigger.nick])) , trigger.nick)

    def adminegg(self , bot , trigger): # for admins only. in case of need, an admin can manually give an egg to a user.
        try:
           bot.notice(strings["adminegg"] % (trigger.nick , trigger.nick) , trigger.group(3))
        except:
           bot.notice(strings["admineggself"] % (trigger.nick) , trigger.nick)  # using .giveegg without argument will result
        bot.notice("Uovo consegnato correttamente :P" , trigger.nick)          # in a self given egg.


eggita = easteregg()


@module.commands("uovodipasqua")    # this command might change it's syntax in the future (maybe a code to find trough some
@module.example(".uovodipasqua")    # activity)
@module.require_chanmsg
def eegg(bot , trigger):
    eggita.egg(bot , trigger)    # all the commands require chan message (we don't like private chats)

@module.commands("giveegg")
@module.example(".giveegg giovannetor , .giveegg")  # the command for admins. If the user is not admin, the bot replies
@module.require_chanmsg                             # with a smily face :)
def giveegg(bot , trigger):
    if trigger.admin:
        eggita.adminegg(bot , trigger)
    else:
        bot.say("You can't give eggs :) ")
        
