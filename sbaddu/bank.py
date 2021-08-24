from sopel.plugin import  commands, require_privmsg , example


def money_getter(bot , nick):
    money = bot.db.get_nick_value(nick , "denari")
    if not money:
        bot.db.set_nick_value(nick , "denari" , 0)
        return 0
    else:
        return money


@commands("bank" , "ba")
@example(".bank" , ".bank gio")
def bank(bot , trigger):
    if not trigger.group(3):
        money = money_getter(bot , trigger.nick)
        bot.reply(" you have " + str(money) + "denari in your Bank.")
    else:
        if trigger.group(3) == "Trinacry" or trigger.group(3) == "trinacry":
            bot.reply("Darling, I'm the Bank. I own EVERYTHING!!!")
            return

        gender = bot.db.get_nick_value(trigger.group(3) , "pronouns")

        if not gender:
            gender_def = "their"
        else:
            gender_def = gender.split("/")[2]

        money = money_getter(bot , trigger.group(3))
        bot.reply(trigger.group(3) + "  has " + str(money) + "denari in " + gender_def + " Bank.")

@commands("pay")
@example(".pay gio 50")
def pay(bot , trigger):
    money_1 = money_getter(bot , trigger.nick)
    money_2 = money_getter(bot , trigger.group(3))

    to_give = int(trigger.group(4))

    if to_give > money_1:
        bot.reply(" you don't have enough money to pay.")
        return

    money_1 -= to_give
    money_2 += to_give

    bot.db.set_nick_value(trigger.nick , "money" , money_1)
    bot.db.set_nick_value(trigger.group(3) , "money" , money_2)

