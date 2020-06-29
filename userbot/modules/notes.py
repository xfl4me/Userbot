# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping notes. """

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import register
from asyncio import sleep


@register(outgoing=True, pattern="^.notes$")
async def notes_active(svd):
    """ For .notes command, list all of the notes saved in a chat. """
    try:
        from userbot.modules.sql_helper.notes_sql import get_notes
    except AttributeError:
        await svd.edit("`Running on Non-SQL mode!`")
        return
    message = "`Non ci sono note salvate qui!`"
    notes = get_notes(svd.chat_id)
    for note in notes:
        if message == "`Non ci sono note salvate qui!`":
            message = "Note salvate qui:\n"
            message += "`#{}`\n".format(note.keyword)
        else:
            message += "`#{}`\n".format(note.keyword)
    await svd.edit(message)


@register(outgoing=True, pattern=r"^.clear (\w*)")
async def remove_notes(clr):
    """ For .clear command, clear note with the given name."""
    try:
        from userbot.modules.sql_helper.notes_sql import rm_note
    except AttributeError:
        await clr.edit("`Running on Non-SQL mode!`")
        return
    notename = clr.pattern_match.group(1)
    if rm_note(clr.chat_id, notename) is False:
        return await clr.edit("`Impossibile trovare la nota:` **{}**".format(notename))
    else:
        return await clr.edit(
            "`Nota eliminata correttamente:` **{}**".format(notename))


@register(outgoing=True, pattern=r"^.save (\w*)")
async def add_note(fltr):
    """ For .save command, saves notes in a chat. """
    try:
        from userbot.modules.sql_helper.notes_sql import add_note
    except AttributeError:
        await fltr.edit("`Running on Non-SQL mode!`")
        return
    keyword = fltr.pattern_match.group(1)
    string = fltr.text.partition(keyword)[2]
    msg = await fltr.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await fltr.client.send_message(
                BOTLOG_CHATID, f"#NOTE\
            \nCHAT ID: {fltr.chat_id}\
            \nKEYWORD: {keyword}\
            \n\nThe following message is saved as the note's reply data for the chat, please do NOT delete it !!"
            )
            msg_o = await fltr.client.forward_messages(entity=BOTLOG_CHATID,
                                                       messages=msg,
                                                       from_peer=fltr.chat_id,
                                                       silent=True)
            msg_id = msg_o.id
        else:
            await fltr.edit(
                "`Saving media as data for the note requires the BOTLOG_CHATID to be set.`"
            )
            return
    elif fltr.reply_to_msg_id and not string:
        rep_msg = await fltr.get_reply_message()
        string = rep_msg.text
    success = "`Nota {} correttamente. Usa` #{} `per averla`"
    if add_note(str(fltr.chat_id), keyword, string, msg_id) is False:
        return await fltr.edit(success.format('updated', keyword))
    else:
        return await fltr.edit(success.format('added', keyword))


@register(pattern=r"#\w*",
          disable_edited=True,
          disable_errors=True,
          ignore_unsafe=True)
async def incom_note(getnt):
    """ Notes logic. """
    try:
        if not (await getnt.get_sender()).bot:
            try:
                from userbot.modules.sql_helper.notes_sql import get_note
            except AttributeError:
                return
            notename = getnt.text[1:]
            note = get_note(getnt.chat_id, notename)
            message_id_to_reply = getnt.message.reply_to_msg_id
            if not message_id_to_reply:
                message_id_to_reply = None
            if note and note.f_mesg_id:
                msg_o = await getnt.client.get_messages(entity=BOTLOG_CHATID,
                                                        ids=int(
                                                            note.f_mesg_id))
                await getnt.delete()
                await getnt.client.send_message(getnt.chat_id,
                                                msg_o.mesage,
                                                reply_to=message_id_to_reply,
                                                file=msg_o.media)
            elif note and note.reply:
                await getnt.delete()
                await getnt.client.send_message(getnt.chat_id,
                                                note.reply,
                                                reply_to=message_id_to_reply)

    except AttributeError:
        pass


@register(outgoing=True, pattern="^.rmbotnotes (.*)")
async def kick_marie_notes(kick):
    """ For .rmbotnotes command, allows you to kick all \
        Marie(or her clones) notes from a chat. """
    bot_type = kick.pattern_match.group(1).lower()
    if bot_type not in ["marie", "rose"]:
        await kick.edit("`Questo bot non è ancora supportato!`")
        return
    await kick.edit("```Distruggerà tutte le note!```")
    await sleep(3)
    resp = await kick.get_reply_message()
    filters = resp.text.split("-")[1:]
    for i in filters:
        if bot_type == "marie":
            await kick.reply("/clear %s" % (i.strip()))
        if bot_type == "rose":
            i = i.replace('`', '')
            await kick.reply("/clear %s" % (i.strip()))
        await sleep(0.3)
    await kick.respond(
        "```Bot tolti correttamente!```\n Dammi dei biscotti!")
    if BOTLOG:
        await kick.client.send_message(
            BOTLOG_CHATID, "Ho pulito tutte le note a " + str(kick.chat_id))


CMD_HELP.update({
    "notes":
    "\
#<notename>\
\nUtilizzo: Invia la nota corrispondente.\
\n\n.save <nome> <valore> o rispondi ad un messaggio con .save <nome>\
\nUtiizzo: Salva il messaggio risposto nelle note. (Funziona con foto, sticker e file!)\
\n\n.notes\
\nUtilizzo: Invia la lista delle note salvate in una chat.\
\n\n.clear <nome>\
\nUtilizzo: Cancella la nota selezionata.\
\n\n.rmbotnotes <marie/rose>\
\nUtilizzo: Rimuove tutte le note dei bot admin (Supportati: Marie, Rose e i loro cloni.) nella chat."
})
