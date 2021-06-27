from random import randint

from sopel import formatting
from sopel.module import (event, commands, example, priority, OP, HALFOP, require_privilege, require_chanmsg , require_privmsg)
from sopel.tools import Identifier
logs = "#trinacry-logs"

@commands("giohelp")
@example("=giohelp i can't understand anything, please contact me XD")
def giohelp(bot, trigger):
    bot.say("Don't worry " + trigger.nick + ", you'll be contacted ASAP.")
    bot.say("SUPERTEST :" + trigger.nick + " ha richiesto il tuo aiuto in " + trigger.sender+ ": " + trigger.group(2) , logs)

@commands("boop")
@require_privmsg()
def boop(bot , trigger):
    if not trigger.group(3) or not trigger.group(4):
        bot.reply("Correct syntax: .boop <chan> <user>")
        return
    if trigger.group(3) == "pm" :
        bot.reply(trigger.group(4) + " will be boooooped in PM :P")
        bot.action("boops " + trigger.group(4) +" with a pillow. Wonder who asked this...", trigger.group(4))
        return
    if trigger.group(3) not in bot.channels:
        bot.reply("I'm NOT in the chan " + trigger.group(3) + ". Correct syntax: .boop <chan|pm> <user> ..." )
        return
    bot.reply(trigger.group(4) + " will be boooooped :P")
    bot.action("boops " + trigger.group(4) +" with a pillow. Wonder who asked this...", trigger.group(3))

#@event("JOIN")
#def join(bot, trigger):
#    if trigger.nick != "Trinacry":
#        bot.say("Welcome " + trigger.nick + "! :D")


#@event("PART")
#def part(bot, trigger):
#    bot.say("Goodbye " + trigger.nick + "! :C")


@commands("randnum")
def randnum(bot, trigger):
    numero = randint(0, 1000)
    bot.say("You got the number " + str(numero))


@commands("randsentence")
def randsentence(bot, trigger):
    sentences = ["hi", "hi 2", "not hi", "surely not hi"]
    bot.say(sentences[randint(0, 3)])

@commands("hug")
def hug(bot , trigger):
    try:
        bot.action("hugs " + trigger.group(2) + " veeeery tight. Love you :)")
    except:
        bot.action("hugs " + trigger.nick + " veeeery tight. Love you :) ")


@commands("dontlike")
@example(".dontlike giovannetor")
def dontlike(bot, trigger):
    if trigger.group(2) == "Trinacry":
        if trigger.admin:
            bot.say("Mh, only cuz it's you gio...")
            bot.action("hugs gio")
        else:
           bot.say("What have i done to you T.T")
           bot.action("goes to hide under the sofa crying")
    elif trigger.group(2) == "giovannetor":
        bot.say("HOW DARE YOU!")
        bot.action("slaps " + trigger.nick)
    else:
       bot.reply("Duuude, i don't like " + trigger.group(2) + " either")
       bot.action("hides in the bush")

@commands("adtest")
def adtest(bot , trigger):
    if trigger.admin:
        bot.reply("YOU'RE MY ADMIN, TAKE A COOKIE OMG!!!")
    else:
        bot.reply("you are not my admin...you suck...")



@commands("giokick")
def giokick(bot, trigger):
    text = trigger.group().split()
    reason = ' '.join(text[2:])
    if trigger.admin:
        bot.kick(trigger.group(2), trigger.sender, reason)
    else:
        bot.say("You are not an admin, go away!")


@commands("sendcard", "sc")
def sendcard(bot, trigger):
    semi = ("♠", "♥", "♦", "♣")
    numeri = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
    carte = []
    carte_mischiate = []
    for i in semi:
        for k in numeri:
            carta = str(k) + i
            carte.append(carta)
    bot.say("Hai trovato un " + carte[randint(0 , len(carte))])


@commands("splittest")
def splittest(bot, trigger):
    stringa = trigger
    str1, str2 = stringa.split(" ")
    bot.say("Ho trovato la stringa " + str1 + " + " + str2)


@commands("grouptest")
def grouptest(bot, trigger):
    stringa00 = trigger.group(0)
    stringa0 = trigger.group(1)
    stringa1 = trigger.group(2)
    stringa2 = trigger.group(3)
    stringa3 = trigger.group(4)
    stringa4 = trigger.group(5)
    bot.say(
        "Ho trovato la stringa " + stringa00 + "+" + stringa0 + "+" + stringa1 + "+" + stringa2 + "++" + stringa3 + "+++" + stringa4)
    stringa = trigger.group(2).split()
    bot.say(trigger)
