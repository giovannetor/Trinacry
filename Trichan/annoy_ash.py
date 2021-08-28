from sopel import plugin , tools
from random import  randint


@plugin.interval(900)
def annoy_ash(bot):
    sentences = ["Hi kiddo","Hello dude, this is an annoying module just for you! :D", "Pssssst, you're short.", "MUAHAHAH",
                 "How're you kiddo?", "Want to /ignore me? You sure? I manage half of the network :P" ,
                 "Ehy", "If you say sorry to gio I might stop :P"
                 "Boooooop", "PSSSSSSSSSSSSSSSSSSSST",
                 "PINGGGG", "01010101010101 <--- turn it into letters" ,
                 "Pew Pew, take these!",  ".-../---/.-..",
                 "Flying pizza coming for youuuu",
                 "Uhmmmm, you're short.",
                 "Am I annoying you? I'm so sorry..."]

    nick = bot.db.get_nick_value("Ash" , "annoy_ash_nick" )
    frase = sentences[randint(0 , len(sentences) -1)]
    bot.say(frase , nick)
    bot.say("Told to Ash: " + frase , "gio")

@plugin.event("NICK")
@plugin.rule(".*")
@plugin.priority("high")
def nick_change(bot, trigger):
        old_ash = bot.db.get_nick_value("Ash" , "annoy_ash_nick" )
        old_new = trigger.nick
        new = tools.Identifier(trigger)
        if old_ash != old_new:
            return
        old_ash = new
        bot.db.set_nick_value("Ash" , "annoy_ash_nick" , old_ash)
        bot.say("Where do you think you're going? You can't run :P" , old_ash)

@plugin.commands("add_ash")
def add_ash(bot , trigger):
    bot.db.set_nick_value("Ash" , "annoy_ash_nick" , trigger.group(3))
    bot.reply("Eheh done, "+ trigger.group(3) + " has no chances against us!!!")
