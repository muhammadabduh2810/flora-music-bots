from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from config import BANNED_USERS
from WinxMusic import YouTube, app
from WinxMusic.utils.channelplay import get_channeplayCB
from WinxMusic.utils.decorators.language import languageCB
from WinxMusic.utils.stream.stream import stream


@app.on_callback_query(filters.regex("LiveStream") & ~BANNED_USERS)
@languageCB
async def play_live_stream(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, callback_query)
    except:
        return
    video = True if mode == "v" else None
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    try:
        await callback_query.answer()
    except:
        pass
    mystic = await callback_query.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text(_["play_3"])
    ffplay = True if fplay == "f" else None
    if not details["duration_min"]:
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                callback_query.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            return await mystic.edit_text(err)
    else:
        return await mystic.edit_text("Not a live stream")
    await mystic.delete()
