from sopel.module import rule , require_admin , commands , OP , require_owner , event , require_privmsg
from sopel.tools.target import Channel
from random import randint , shuffle
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL

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
    bot.write(['MODE', trigger.sender, '+o', trigger.nick])



@rule(".*mask.*")
@require_admin()
def mask(bot , trigger):
    bot.write(['MODE', trigger.sender, '-o', trigger.nick])



@commands("destroy")
@require_owner()
def execute(bot , trigger):
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
        bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.LIGHT_BLUE +"[PM] "+ CONTROL_NORMAL + trigger.nick + ": "+ trigger , "#trinacry-logs")

@commands("resurrect")
@require_admin()
def resurrect(bot , trigger):
    if not trigger.group(2):
        return
    bot.write(['MODE', trigger.sender, '-b', trigger.group(2)])
    bot.write(["invite" , trigger.nick(2)])
    bot.say(trigger.group(2) + " has succesfully been resurrected.")

@event("JOIN")
def autop(bot , trigger):
    listauser_V = ["yorick","Marco_Polo","Alie-Pie","Kimmie"]
    listachan = ["#general","#test" ]
    if trigger.account in listauser_V and trigger.sender in listachan:
        bot.write(["MODE", trigger.sender , "+V " , trigger.nick] )

@commands("hvoice")
@require_admin("You're not an admin")
def hvoice(bot , trigger):
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
    
