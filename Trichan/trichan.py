from sopel.plugin import rule , require_admin , commands , OP , require_owner , event , require_privmsg, nickname_commands
from random import randint , shuffle
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL


LOG_CHAN = "#trinacry-logs"
@commands("privacy")
def privacy(bot , trigger):
    bot.notice("Here's the Privacy Policy: https://www.termsfeed.com/live/c0b6de93-39dc-484b-a460-b946ecb9428e " , trigger.nick)

@rule(".*BANG.*")
def bang(bot , trigger):
    if trigger.sender == "#general":
        return
    if trigger.admin:
        lista = []
        for i in bot.channels[trigger.sender].users:
            lista.append(i)
        shuffle(lista)
        shuffle(lista)
        player = lista[randint(0 , len(lista)-1)]
        bot.kick(player , message="BANG!")
        bot.say("One is out. Just " + str(len(lista)-1) + " left >:) ")
        lista = []
    else:
        bot.kick(trigger.nick , message="Only admins can bang.  BANG!!!")

@rule(".*POWAH.*")
@require_admin()
def powah(bot , trigger):
    bot.say(CONTROL_COLOR + colors.RED + "HERE'S THE POWAH!")
    bot.write(['MODE', trigger.sender, '+h', trigger.nick])



@rule(".*mask.*")
@require_admin()
def mask(bot , trigger):
    bot.write(['MODE', trigger.sender, '-h', trigger.nick])



@commands("destroy")
@require_owner()
def destroy(bot , trigger):
    if not trigger.group(2):
        return
    try:
        bot.write(['MODE', trigger.sender, '+b', trigger.group(2)])
        bot.kick(trigger.group(2))
    except:
        bot.say("No person with that nick.")

@rule(".*")
@require_privmsg()
def echo(bot , trigger):
    if not trigger.owner:
        bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_BLUE +"[PM] " + CONTROL_NORMAL + trigger.nick + ": " + trigger, LOG_CHAN)

@commands("resurrect")
@require_admin()
def resurrect(bot , trigger):
    if not trigger.group(2):
        return
    bot.write(['MODE', trigger.sender, '-b', trigger.group(2)])
    bot.write(["invite" , trigger.group(2)])
    bot.say(trigger.group(2) + " has succesfully been resurrected.")

@event("JOIN")
def autop(bot , trigger):
    listauser_V = ["yorick","Marco_Polo","Alie-Pie","Kimmie"]
    listachan = ["#general","#test" ]
    if trigger.account in listauser_V and trigger.sender in listachan:
        bot.write(["MODE", trigger.sender , "+V " , trigger.nick] )

@nickname_commands("hv" , "hvoice" , "halfvoice")
def manop(bot , trigger):
    if trigger.group(3) != "please":
        bot.say("Say please...")
        return
    listauser_V = ["yorick","Marco_Polo","Alie-Pie","Kimmie","giovannetor"]
    listachan = ["#general","#test" ]
    if trigger.account in listauser_V and trigger.sender in listachan:
        bot.write(["MODE", trigger.sender , "+V " , trigger.nick] )
        bot.say("Here's your hat darling :)")
    else:
        bot.say("Something didn't work...")

@commands("hvoice")
@require_admin("You're not an admin")
def hvoice(bot , trigger):
    if not trigger.group(3):
        bot.write(["MODE" , trigger.sender , "+V" , trigger.nick])
    else:
        bot.write(["MODE" , trigger.sender , "+V" , trigger.group(3)])

@commands("do")
@require_admin("You're not an admin")
def do(bot , trigger):
    cmd_list = ""
    contatore = 0
    for word in trigger.split():
        if contatore != 0:
            cmd_list += (str(word))
            cmd_list += " "
        contatore += 1
    print("Ho eseguito: " + str(cmd_list))
    bot.write(cmd_list) 
    

@commands("giokick")
def giokick(bot, trigger):
    text = trigger.group().split()
    reason = ' '.join(text[2:])
    if trigger.admin:
        bot.kick(trigger.group(2), trigger.sender, reason)
    else:
        bot.say("You are not an admin, go away!")

