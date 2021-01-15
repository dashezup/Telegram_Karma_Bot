import json
from os import path
from pyrogram import Client, filters
from config import bot_token

app = Client(":memory:",bot_token=bot_token,
        api_id=6,
        api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")


@app.on_message(filters.command(['start']))
async def start(_, message):
    await message.reply_text("Hey, I'm A Karma Bot, You Can Upvote Or Downvote Someone Using Me, Join @TheHamkerChat For Support!")

@app.on_message(filters.command(['help']))
async def help(_, message):
    await message.reply_text('''+ To Upvote A Message.
- To Downvote A Message.
/karma To Check Karma Points Of This Group.''')

@app.on_message(filters.regex("\+"))
async def upvote(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Upvote.")
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply_text("dafuq bruh.")
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not path.exists(filename):
        sample_bot = {"1527962675" : 1} 
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] += 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(f'Incremented Karma of {user_mention} By 1 \nTotal Points: {members[f"{user_id}"]}')

@app.on_message(filters.regex("\-"))
async def downvote(_, message):
    if not message.reply_to_message:
        await message.reply_text("Reply To A Message To Downvote.")
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    filename = f"{chat_id}.json"

    if not path.exists(filename):
        sample_bot = {"1527962675" : 1} 
        with open(filename, "w") as f:
            f.write(json.dumps(sample_bot))
    with open(filename) as f2:
        members = json.load(f2)
    if not f"{user_id}" in members:
        members[f"{user_id}"] = 1
    else:
        members[f"{user_id}"] -= 1
    with open(filename, "w") as f3:
        f3.write(json.dumps(members))
    await message.reply_text(f'Decremented Karma Of {user_mention} By 1 \nTotal Points: {members[f"{user_id}"]}')


@app.on_message(filters.command(['karma']))
async def karma(_, message):
    if not message.reply_to_message:
        chat_id = message.chat.id
        filename = f"{chat_id}.json"
        with open(filename) as f2:
            members = json.load(f2)
        output = ""
        for i in range(len(members)):
            output += f"{(await app.get_users(list(members.keys())[i])).username}: {list(members.values())[i]}\n"    
        await message.reply_text(output)

app.run()
