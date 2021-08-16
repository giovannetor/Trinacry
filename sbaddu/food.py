from sopel.plugin import rule , commands , event
from random import randint
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL


@commands("drink")
def drink(bot , trigger):
   # if trigger.nick == "Ash":
   #     bot.say("No drinks for kiddos!!")
   #     return
    lista_drink = ["Water" , "Coca Cola" , "Pepsi" , "Vodka",
                   "Tequila", "Beer", "Absinth", "Rum" , "Red Wine" , "White Wine" , "Fanta" , "Chardonnay" ,
                   "Beer",  "Tea", "Hot Chocolate", "soda" , "Icetea" ,
                   "Captain Morgan", "Whiskey", "Cognac", "Gin", "Martini", "Liqueur",
                   "Cider", "Sake", "Brandy", "Schnapps", "Jenever" , "Irish Coffee",
                  " Bloody Mary", "Mojito", "Piña Colada", "Sex on the Beach" , "Acquarium", "Quattro Bianchi",
                  " Gin Fizz", "Mai Tai", "Margarita", "Cosmopolitan", "Jack Daniel",
                   "Eggnog", "Gluhwein", "Jägermeister", "Sherry", "Prosecco", "Port"," Gin Tonic", "Amaretto",
                  " Bailey's", "Bourbon",  "Cognac" , "Champagne" ]

    lista_cups = ["shot glass", "cup", "glass", "pint", "wine glass", "mug", "bottle" , "barrel" , "bowl", "can" , "jar"] 
    if not trigger.group(2):
         
        bot.action("gives a " + lista_cups[randint(0 , len(lista_cups) -1)] + " of "  + CONTROL_BOLD + CONTROL_COLOR + colors.FUCHSIA +
            lista_drink[randint(0 , len(lista_drink) -1)] + CONTROL_NORMAL+ " to " + trigger.nick)
    else:
        bot.action("gives a " + lista_cups[randint(0 , len(lista_cups) -1)] + " of "  + CONTROL_BOLD + CONTROL_COLOR + colors.FUCHSIA +
            trigger.group(2) + CONTROL_NORMAL+ " to " + trigger.nick)

@rule(".*pineapple.*" )
def pineapple(bot , trigger):
    if not trigger.owner:
        if "pizza" in trigger.lower():
            bot.kick(trigger.nick , message= "PINEAPPLE SUCKS!")


@commands("pizza")  #condividi pizza con persone. distingue self da other
def pizza(bot , trigger):
    listapizze = ["Margherita" , "Capricciosa" , "PataPizza" ,
                  "Quattro Formaggi" , "Hawaiana (really??)" , "Frutti di mare" ,
                  "Biancaneve" , "Boscaiola" , "Regina" , "Chil Pizza"
                  ]
    lista_act = ["hands a slice of " , "throws a piece of " , "hurls a " , "gently gives a piece of "  ]
    #if len((trigger.group(2)) >= 1 :
    try:
        bot.action(lista_act[randint(0 , len(lista_act)-1)] + listapizze[randint(0 , len(listapizze)-1)] + " to " + trigger.group(2))
    #else:
    except:
        bot.action(lista_act[randint(0 , len(lista_act)-1)] + listapizze[randint(0 , len(listapizze)-1)] +  " to you.")



