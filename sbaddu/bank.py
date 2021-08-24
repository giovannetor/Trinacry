from sopel.plugin import  commands, require_privmsg , example

@commands("bank" , "ba")
def bank(bot , trigger):
    if not trigger.group(3):
        money = bot.db.get_nick_value(trigger.nick , "denari")
        if not money:
            bot.db.set_nick_value(trigger.nick , "denari" , 100)
            bot.reply(" you have 0 denari in your Bank.")
        else:
            bot.reply(" you have " + str(money) + "denari in your Bank.")
    else:
        gender = bot.db.get_nick_value(trigger.group(3) , "pronouns")
        if not gender:
            gender_def = "their"
        else:
            gender_def = gender.split("/")[2]

        money = bot.db.get_nick_value(trigger.group(3) , "denari")

        if not money:
            bot.db.set_nick_value(trigger.nick , "denari" , 100)
            bot.reply(trigger.group(3) + " has 0 denari in " + gender_def + " Bank.")
        else:
            bot.reply(trigger.group(3)+ "  has " + str(money) + "denari in " + gender_def + " Bank.")

