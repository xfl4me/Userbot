# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

try:
    from userbot.modules.sql_helper.globals import gvarstatus, addgvar, delgvar
    afk_db = True
except AttributeError:
    afk_db = False

# ========================= CONSTANTS ============================
AFKSTR = [
    "Adesso sono occupato. Per favore, parla in una borsa e quando torno puoi darmi la borsa!",
    "Sono via adesso. Se hai bisogno di qualcosa, lascia un messaggio dopo il segnale acustico:\n`beeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeep`!",
    "Ti sono mancato, la prossima volta mirare meglio.",
    "Torno tra qualche minuto e se non lo sono...,\naspetta di più.",
    "Non sono qui in questo momento, quindi probabilmente sono altrove.",
    "Roses are red,\nViolets are blue,\nLeave me a message,\nAnd I'll get back to you.",
    "A volte vale la pena aspettare le cose migliori della vita ...\nTorno subito.",
    "Torno subito,\nMa se non tornerò subito,\nTornerò più tardi.",
    "Se non l'hai già capito,\nNon sono qui.",
    "Ciao, benvenuto nel mio messaggio, come posso ignorarti oggi?",
    "Sono via oltre,\n7 mari e 7 continenti,\n7 montange e 7 colline,\n7 pianure e 7 tumuli,\n7 piscine e 7 laghi,\n7 sorgenti e 7 prati,\n7 città e 7 quartieri,\n7 blocchi e 7 case...\n\nDove neanche i tuoi messaggi possono raggiungermi!",
    "Al momento sono lontano dalla tastiera, ma se urlerai abbastanza forte sul tuo schermo, potrei semplicemente sentirti.",
    "Sono andato da questa parte\n---->",
    "Sono andato da questa parte\n<----",
    "Per favore, lascia un messaggio e fammi sentire ancora più importante di quanto lo sia già.",
    "Non sono qui, quindi smettila di scrivermi,\naltrimenti ti ritroverai con uno schermo pieno dei tuoi messaggi.",
    "Se ero qui,\nTi avrei detto dov'ero.\n\nMa se non sono qui,\nnon chiedere quando ritornerò.",
    "Sono via!\nNon so quando ritornerò!\nSpero tra pochi minuti da adesso!",
    "Al momento non sono disponibile, quindi per favore lascia il tuo nome, numero e indirizzo e ti seguirò più tardi.",
    "Mi dispiace, non sono qui adesso.\nSentiti libero di parlare con il mio userbot per tutto il tempo che desideri.\nTi richiamo più tardi.",
    "Scommetto che ti aspettavi un messaggio!",
    "La vita è così breve, ci sono così tante cose da fare ...\nSono via facendo una di queste",
    "Non sono qui adesso...\nma se fossi...\n\nnon sarebbe fantastico?",
]
# =================================================================


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFFKREASON
    ISAFK_SQL = False
    AFKREASON_SQL = None
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    EXCUSE = AFKREASON_SQL if afk_db else AFKREASON
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK or ISAFK_SQL:
            if mention.sender_id not in USERS:
                if EXCUSE:
                    await mention.reply(f"Sono offline adesso.\
                    \nMotivo: `{EXCUSE}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if EXCUSE:
                        await mention.reply(
                            f"Nel caso non l'avessi notato, sono ancora AFK.\
                        \nMotivo: `{EXCUSE}`")
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global AFFKREASON
    ISAFK_SQL = False
    AFKREASON_SQL = None
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    global USERS
    global COUNT_MSG
    EXCUSE = AFKREASON_SQL if afk_db else AFKREASON
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and (ISAFK or ISAFK_SQL):
            if sender.sender_id not in USERS:
                if EXCUSE:
                    await sender.reply(f"Sono offline adesso\
                    \nMotivo: `{EXCUSE}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if EXCUSE:
                        await sender.reply(
                            f"Nel caso non l'avessi notato, sono ancora AFK\
                        \nMotivo: `{EXCUSE}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFFKREASON
    ISAFK_SQL = False
    AFKREASON_SQL = None
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    if string:
        if afk_db:
            addgvar("AFK_REASON", string)
        AFKREASON = string
        await afk_e.edit(f"Going AFK!\
        \nReason: `{string}`")
    else:
        await afk_e.edit("`D'ora in poi sarò offline!`")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nYou went AFK!")
    if afk_db:
        addgvar("AFK_STATUS", True)
    ISAFK = True
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global COUNT_MSG
    global USERS
    global ISAFK
    global AFFKREASON
    AFKREASON_SQL = None
    ISAFK_SQL = False
    if afk_db:
        ISAFK_SQL = gvarstatus("AFK_STATUS")
        AFKREASON_SQL = gvarstatus("AFK_REASON")
    if ISAFK or ISAFK_SQL:
        if afk_db:
            delgvar("AFK_STATUS")
            delgvar("AFK_REASON")
        ISAFK = False
        AFKREASON = None
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Hai ricevuto " + str(COUNT_MSG) + " messaggi da " +
                str(len(USERS)) + " chat quando eri offline",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " sent you " + "`" + str(USERS[i]) + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}


CMD_HELP.update({
    "afk":
    ".afk [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
