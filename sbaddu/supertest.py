from random import randint
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL, CONTROL_ITALIC
from sopel.plugin import  commands, require_privmsg , example
logs = "#trinacry-logs"

@commands("contact" , "giohelp")
def contact(bot, trigger):
    bot.say("Don't worry " + trigger.nick + ", you'll be contacted ASAP.")
    bot.say(CONTROL_BOLD + CONTROL_COLOR +  colors.YELLOW + "CONTACT: " +CONTROL_NORMAL+
            trigger.nick + " ha scritto in " + trigger.sender+ ": "+ CONTROL_ITALIC + trigger.group(2) , logs)

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


#@commands("dontlike")
#@example(".dontlike giovannetor")
#def dontlike(bot, trigger):
#    if trigger.group(2) == "Trinacry":
#        if trigger.admin:
#            bot.say("Mh, only cuz it's you gio...")
#            bot.action("hugs gio")
#        else:
#           bot.say("What have i done to you T.T")
#           bot.action("goes to hide under the sofa crying")
#    elif trigger.group(2) == "giovannetor":
#        bot.say("HOW DARE YOU!")
#        bot.action("slaps " + trigger.nick)
#    else:
#       bot.reply("Duuude, i don't like " + trigger.group(2) + " either")
#       bot.action("hides in the bush")

@commands("uptest")
def uptest(bot , trigger):
    if trigger.admin:
        bot.reply("Ehy, the code was updated. 2")

@commands("adtest")
def adtest(bot , trigger):
    if trigger.admin:
        bot.reply("YOU'RE MY ADMIN, TAKE A COOKIE OMG!!!")
    else:
        bot.reply("you are not my admin...you suck...")




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

@commands("dbtest")
@example(".dbtest add gio test")
def dbtest(bot , trigger):
    if trigger.group(3) == "add":
        bot.db.set_nick_value(trigger.group(4) ,"test", trigger.group(5))
        bot.reply(" value assigned.")

    elif trigger.group(3) == "get":
        test = bot.db.get_nick_value(trigger.group(4) , "test")
        if test:
            bot.reply(" your test value is " + test)
        else:
            bot.reply(" no value for " + trigger.group(4))
            return
    elif trigger.group(3) == "del":
        try:
            bot.reply( " value" + bot.db.get_nick_value(trigger.group(4) , "test") +" deleted with success.")
            bot.db.delete_nick_value(trigger.group(4) , "test")

        except:
            bot.reply(" there's no value to delete for " + trigger.group(4))

    else:
        bot.reply(" use add/get/del ")

@commands("prtest")
@example(".prtest gio")
def prtest(bot , trigger):
    print("DOING")
    gender = bot.db.get_nick_value(trigger.group(3) , "pronouns")
    if not trigger.group(3):
        bot.reply(" who do you want to test?")
        return
    if not gender:
        bot.reply(trigger.group(3) + " hasn't already set his gender.")
        return
    gender_test = gender.split("/")[1]
    bot.act("hands " + trigger.group(3) + " " + gender_test + " Ice-Cream.")
    print("GOT " + gender_test + " and " + gender)
