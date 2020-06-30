# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# You can find misc modules, which dont fit in anything xD
""" Userbot module for other small commands. """

from random import randint
from asyncio import sleep
from os import execl
import sys
import os
import io
import sys
import json
from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot, UPSTREAM_REPO_URL
from userbot.events import register


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    message = time.text
    if " " not in time.pattern_match.group(1):
        await time.reply("Syntax: `.sleep [seconds]`")
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit("Sto aspettando il tempo stabilito`")
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Hai messo il bot in pausa per " + str(counter) + " secondi",
            )
        await sleep(counter)
        await time.edit("`OK, sono sveglio ora.`")


@register(outgoing=True, pattern="^.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Arrivederci, *suono di windows xp*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot spento")
    await bot.disconnect()


@register(outgoing=True, pattern="^.restart$")
async def killdabot(event):
    await event.edit("`Riaccendo...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot Riavviato")
    await bot.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        f"Clicca [qui]({UPSTREAM_REPO_URL}) per installare l'userbot di @xfl4me.")


@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with io.BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Check the userbot log for the decoded message data !!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Here's the decoded message data !!`")


CMD_HELP.update({
    'random':
    '.random <item1> <item2> ... <itemN>\
\nUtilizzo: Sceglie qualcosa di casuale da una lista di elementi.'
})

CMD_HELP.update({
    'sleep':
    '.sleep <seconds>\
\nUtilizzo: Anche il bot si addormenta, fallo dormire per qualche istante.'
})

CMD_HELP.update({
    "shutdown":
    ".shutdown\
\nUtilizzo: Alcune volte devi spegnere il bot. Alcune volte speri semplicemente di\
sentire il suono di spegnimento di Windows XP... ma non succederà."
})

CMD_HELP.update({
    'repo':
    '.repo\
\nUtilizzo: Se vuoi dare istruzioni agli altri per installare il bot.'
})

CMD_HELP.update({
    "readme":
    ".readme\
\nUtilizzo: Invia link per installare l'userbot e caricare i moduli (in inglese)."
})

CMD_HELP.update({
    "repeat":
    ".repeat <no.> <text>\
\nUtilizzo: Ripete il testo per un numero di volte. Non confondere questo con spam."
})

CMD_HELP.update({"restart": ".restart\
\nUtilizzo: Riavvia il bot !!"})

CMD_HELP.update({
    "raw":
    ".raw\
\nUtilizzo: Esporta dati dettagliati sul messaggio in risposta su un file .json."
})
