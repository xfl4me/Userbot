# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
""" Userbot module containing commands for keeping global notes. """

from userbot.events import register
from userbot import CMD_HELP, BOTLOG_CHATID


@register(outgoing=True,
          pattern=r"\$\w*",
          ignore_unsafe=True,
          disable_errors=True)
async def on_snip(event):
    """ Snips logic. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    message_id_to_reply = event.message.reply_to_msg_id
    if not message_id_to_reply:
        message_id_to_reply = None
    if snip and snip.f_mesg_id:
        msg_o = await event.client.get_messages(entity=BOTLOG_CHATID,
                                                ids=int(snip.f_mesg_id))
        await event.client.send_message(event.chat_id,
                                        msg_o.message,
                                        reply_to=message_id_to_reply,
                                        file=msg_o.media)
        await event.delete()
    elif snip and snip.reply:
        await event.client.send_message(event.chat_id,
                                        snip.reply,
                                        reply_to=message_id_to_reply)
        await event.delete()


@register(outgoing=True, pattern="^.snip (\w*)")
async def on_snip_save(event):
    """ For .snip command, saves snips for future use. """
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG_CHATID:
            await event.client.send_message(
                BOTLOG_CHATID, f"#SNIP\
            \nKEYWORD: {keyword}\
            \n\nThe following message is saved as the data for the snip, please do NOT delete it !!"
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True)
            msg_id = msg_o.id
        else:
            await event.edit(
                "`Saving snips with media requires the BOTLOG_CHATID to be set.`"
            )
            return
    elif event.reply_to_msg_id and not string:
        rep_msg = await event.get_reply_message()
        string = rep_msg.text
    success = "`Snip {} correttamente. Usa` **${}** `ovunque per averlo`"
    if add_snip(keyword, string, msg_id) is False:
        await event.edit(success.format('aggiornato', keyword))
    else:
        await event.edit(success.format('salvato', keyword))


@register(outgoing=True, pattern="^.snips$")
async def on_snip_list(event):
    """ For .snips command, lists snips saved by you. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return

    message = "`Nessun snip disponibile adesso.`"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "`Nessun snip disponibile adesso.`":
            message = "Snips disponibili:\n"
            message += f"`${a_snip.snip}`\n"
        else:
            message += f"`${a_snip.snip}`\n"

    await event.edit(message)


@register(outgoing=True, pattern="^.remsnip (\w*)")
async def on_snip_delete(event):
    """ For .remsnip command, deletes a snip. """
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"`Snip eliminato correttamente:` **{name}**")
    else:
        await event.edit(f"`Impossibile trovare snip:` **{name}**")


CMD_HELP.update({
    "snips":
    "\
$<snip_name>\
\nUtilizzo: Prende lo snip specificato, ovunque.\
\n\n.snip <name> <data> o risponi ad un messaggio con .snip <name>\
\nUtilizzo: Salva il messaggio come snip (nota globale) con il nome. (Funziona anche con gli allegati!)\
\n\n.snips\
\nUtilizzo: Prende la lista di snip.\
\n\n.remsnip <snip_name>\
\nUtilizzo: Elimina lo snip specificato.\
"
})
