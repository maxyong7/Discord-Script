import discord
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter
from discord import Embed
import asyncio
import os
import psycopg2.extras
import time
import aiohttp

cmd_input = os.environ["cmd_input"]
cmd_logs = os.environ["cmd_logs"]
cmd_post = os.environ["cmd_post"]
empty_list = []
# Giveaways
giveaway_words_not_to_join = ["entrants", "congratulations"]
giveaway_exclude_words = ["nothing", "fake", "bots", "bot", "test", "dont", "don't"]
rumble_words = ["click the emoji below to join"]
GiveawayBot_id = 294882584201003009
Giveaway_Boat_id = 530082442967646230
Rumble_Royale = 693167035068317736
# Keywords from tables
words = "w"
guild_id = "g"
channel_id = "c"
leave_id = "l"
# Name of tables (Need to change)
exclude_words = os.environ["exclude_word"]
exclude_guild_id = os.environ["exclude_guild_id"]
exclude_channel_id = os.environ["exclude_channel_id"]
leave_guild_id = os.environ["leave_guild_id"]
# Identifier (Need to change)
identify_list = [os.environ["identify_letters"], "*"]
identify_letters = os.environ["identify_letters"]
all_input = "*"
# Identifier for discord_acc table
discord_acc_table = "discord_acc"
acc_discord_id = "discord_id"
acc_letters = "letters"
# Webhook
join_webhook_name = os.environ["join_webhook_name"]
won_webhook_name = os.environ["won_webhook_name"]
join_webhook_url = os.environ["webhook_url"]
won_webhook_url = os.environ["won_webhook_url"]
# Channels
won_channel = os.environ["won_giveaway_channel_id"]


conn = psycopg2.connect(
    os.environ["DATABASE_URL"],
    sslmode="require",
    keepalives=1,
    keepalives_idle=30,
    keepalives_interval=10,
    keepalives_count=5,
)
c = conn.cursor()
client = discord.Client()


async def leave(user, guild_id):
    await guild_id.leave()


async def create_table():
    with conn:
        try:
            c.execute(
                f"""
            CREATE TABLE {exclude_guild_id}(g BIGINT)
            CREATE TABLE {exclude_words}(w VARCHAR)
            CREATE TABLE {leave_guild_id}(l BIGINT)
            CREATE TABLE {exclude_channel_id}(c BIGINT);
            """
            )
            return [exclude_guild_id, exclude_words, leave_guild_id, exclude_channel_id]
        except:
            return False


async def remove(msg, what):
    msg = str(msg)
    if what == words:
        with conn:
            if msg == all_input:
                c.execute(f"DELETE FROM {exclude_words}")
                return

            else:
                c.execute(f"SELECT * FROM {exclude_words} WHERE {words} = '{msg}'")
                fetchall = c.fetchall()

                if bool(fetchall) == True:  # True if fetchall has a value
                    c.execute(f"DELETE FROM {exclude_words} WHERE {words} = '{msg}';")
                    return True
                else:
                    return False

    if what == guild_id:
        with conn:
            if msg == all_input:
                c.execute(f"DELETE FROM {exclude_guild_id}")
                return
            else:
                c.execute(
                    f"SELECT * FROM {exclude_guild_id} WHERE {guild_id} = '{msg}'"
                )
                fetchall = c.fetchall()

                if bool(fetchall) == True:  # True if fetchall has a value
                    c.execute(
                        f"DELETE FROM {exclude_guild_id} WHERE {guild_id} = '{msg}';"
                    )
                    return True
                else:
                    return False

    if what == channel_id:
        with conn:
            if msg == all_input:
                c.execute(f"DELETE FROM {exclude_channel_id}")
                return
            else:
                c.execute(
                    f"SELECT * FROM {exclude_channel_id} WHERE {channel_id} = '{msg}'"
                )
                fetchall = c.fetchall()

                if bool(fetchall) == True:  # True if fetchall has a value
                    c.execute(
                        f"DELETE FROM {exclude_channel_id} WHERE {channel_id} = '{msg}';"
                    )
                    return True
                else:
                    return False

    if what == leave_id:
        with conn:
            if msg == all_input:
                c.execute(f"DELETE FROM {leave_guild_id}")
                return
            else:
                if bool(fetchall) == True:  # True if fetchall has a value
                    c.execute(
                        f"DELETE FROM {leave_guild_id} WHERE {leave_id} = '{msg}';"
                    )
                    return True
                else:
                    return False


async def add(msg, what):
    msg = str(msg)
    if what == words:
        with conn:
            c.execute(f"SELECT * FROM {exclude_words} WHERE {words} = '{msg}'")
            fetchall = c.fetchall()

            if bool(fetchall) == False:  # Insert if fetchall has no value equals to msg
                c.execute(f"INSERT INTO {exclude_words} ({words}) VALUES ('{msg}');")
                return False
            else:  # Else return nothing
                return True

    if what == guild_id:
        with conn:
            c.execute(f"SELECT * FROM {exclude_guild_id} WHERE {guild_id} = '{msg}'")
            fetchall = c.fetchall()

            if bool(fetchall) == False:  # Insert if fetchall has no value equals to msg
                c.execute(
                    f"INSERT INTO {exclude_guild_id} ({guild_id}) VALUES ({msg});"
                )
                return False
            else:  # Else return nothing
                return True

    if what == channel_id:
        with conn:
            c.execute(
                f"SELECT * FROM {exclude_channel_id} WHERE {channel_id} = '{msg}'"
            )
            fetchall = c.fetchall()
            if bool(fetchall) == False:  # Insert if fetchall has no value equals to msg
                c.execute(
                    f"INSERT INTO {exclude_channel_id} ({channel_id}) VALUES ({msg});"
                )
                return False
            else:  # Else return nothing
                return True

    if what == leave_id:
        with conn:
            c.execute(f"SELECT * FROM {leave_guild_id} WHERE {leave_id} = '{msg}'")
            fetchall = c.fetchall()
            if bool(fetchall) == False:  # Insert if fetchall has no value equals to msg
                c.execute(f"INSERT INTO {leave_guild_id} ({leave_id}) VALUES ({msg});")
                return False
            else:  # Else return nothing
                return True


async def fetch(letters, what):
    # fetchall type is list
    if what == words:
        with conn:
            if letters.lower() in identify_list:
                c.execute(f"SELECT * FROM {exclude_words}")
                fetchall = [f"{x[0]}" for x in c.fetchall()]
                return fetchall

    if what == guild_id:
        with conn:
            if letters.lower() in identify_list:
                c.execute(f"SELECT * FROM {exclude_guild_id}")
                fetchall = [f"{x[0]}" for x in c.fetchall()]
                return fetchall

    if what == channel_id:
        with conn:
            if letters.lower() in identify_list:
                c.execute(f"SELECT * FROM {exclude_channel_id}")
                fetchall = [f"{x[0]}" for x in c.fetchall()]
                return fetchall

    if what == leave_id:
        with conn:
            if letters.lower() in identify_list:
                c.execute(f"SELECT * FROM {leave_guild_id}")
                fetchall = [f"{x[0]}" for x in c.fetchall()]
                return fetchall

    if what == acc_discord_id:
        with conn:
            if letters.lower() in identify_list:
                c.execute(
                    f"SELECT {acc_discord_id} FROM {discord_acc_table} WHERE {acc_letters} = '{letters}'"
                )
                fetchall = [f"{x[0]}" for x in c.fetchall()]
                return fetchall


async def giveaway_react(
    channel, embed, message, user, guild_name, bot_id, msg_channel, msg_channel_name
):
    msg = message.content
    # change to string cause all item[data] is a list
    msg_channel = str(msg_channel)
    if guild_name != None:
        react_guild_id = str(guild_name.id)
        guild_name = str(guild_name)
    msg_channel_name = str(msg_channel_name)

    user = str(user)

    if len(embed) > 0:
        word_list = await fetch(identify_letters, words)
        guild_list = await fetch(identify_letters, guild_id)
        channel_list = await fetch(identify_letters, channel_id)
        # Check exception_guild_id and exclude_guild_id from json before joining
        if (react_guild_id not in guild_list) and (msg_channel not in channel_list):
            # Check word_list in json before joining
            if not any(word in embed.lower() for word in word_list):
                if not any(
                    word in msg.lower() for word in giveaway_words_not_to_join
                ):
                    time_checker = time.time() + 2.5
                    asyncio.sleep(1)
                    if bot_id == Giveaway_Boat_id:
                        split = {embed.split("'")[0]}
                        await_msg = await channel.send(
                            f"> Joined giveaway **{split}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                        )
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(
                                join_webhook_url,
                                adapter=AsyncWebhookAdapter(session),
                            )
                            await webhook.send(
                                f"> Joined giveaway **{split}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}",
                                username=join_webhook_name,
                            )
                        giveaway_kw = embed.split("'")[0]
                        pass
                    elif bot_id == GiveawayBot_id:
                        split = embed.split("'")[1]
                        await_msg = await channel.send(
                            f"> Joined giveaway **{split}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                        )
                        giveaway_kw = embed.split("'")[1]
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(
                                join_webhook_url,
                                adapter=AsyncWebhookAdapter(session),
                            )
                            await webhook.send(
                                f"> Joined giveaway **{split}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}",
                                username=join_webhook_name,
                            )
                        pass

                    await await_msg.add_reaction("✅")

                    check1 = (
                        lambda r, u: r.message.id == await_msg.id
                        and u == await_msg.author
                        and str(r.emoji) in "✅"
                    )
                    check2 = (
                        lambda m: m.channel == await_msg.channel
                        and m.content.lower() == "yes"
                    )  # working
                    check3 = lambda c: c.channel == message.channel and any(
                        word in c.content.lower() for word in word_list
                    )
                    check4 = (
                        lambda r, u: r.message.id == await_msg.id
                        and u != await_msg.author
                        and str(r.emoji) in "✅"
                    )

                    while (time_checker + 0.5) > time.time():
                        if time.time() >= time_checker:
                            reaction = await message.add_reaction(
                                "\N{PARTY POPPER}"
                            )
                            break

                    while True:
                        if time.time() > time_checker:
                            await asyncio.sleep(2.5)
                            reaction = await message.add_reaction(
                                "\N{PARTY POPPER}"
                            )
                        tasks = [
                            asyncio.create_task(
                                client.wait_for(
                                    "reaction_remove", check=check1, timeout=60
                                ),
                                name="check_reaction_remove",
                            ),
                            asyncio.create_task(
                                client.wait_for(
                                    "message", check=check2, timeout=60
                                ),
                                name="check_msg",
                            ),
                            asyncio.create_task(
                                client.wait_for(
                                    "message", check=check3, timeout=60
                                ),
                                name="msg_scanner",
                            ),
                            asyncio.create_task(
                                client.wait_for(
                                    "reaction_add", check=check4, timeout=60
                                ),
                                name="check_reaction_add",
                            ),
                        ]

                        done, pending = await asyncio.wait(
                            tasks,
                            return_when=(
                                asyncio.FIRST_COMPLETED or asyncio.FIRST_EXCEPTION
                            ),
                        )

                        finished: asyncio.Task = list(done)[0]

                        for task in tasks:
                            try:
                                task.cancel()
                            except asyncio.TimeoutError:
                                await await_msg.edit(
                                    content=f" Giveaway unreact timed out. **{giveaway_kw}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                                )
                                return
                            except:
                                return

                        try:
                            action = finished.get_name()
                            result = finished.result()
                        except asyncio.TimeoutError:
                            await await_msg.edit(
                                content=f"> Giveaway unreact timed out. **{giveaway_kw}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                            )
                            return
                        except:
                            return

                        if action == "check_msg":
                            await await_msg.edit(
                                content=f"> Unreacted via 'yes'. **{giveaway_kw}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                            )
                            await message.remove_reaction(
                                "\N{PARTY POPPER}", client.user
                            )
                            break

                        elif action == "check_reaction_remove":
                            await await_msg.edit(
                                content=f"> Unreacted via removing emoji. **{giveaway_kw}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                            )
                            await message.remove_reaction(
                                "\N{PARTY POPPER}", client.user
                            )
                            break

                        elif action == "msg_scanner":
                            await asyncio.sleep(0.5)
                            await channel.send(
                                f"> Potential fake giveaway **{giveaway_kw}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url} <@&961002892897185862>"
                            )

                        elif action == "check_reaction_add":
                            await await_msg.edit(
                                content=f"> Unreacted via add emoji. **{giveaway_kw}** - {guild_name} ({msg_channel_name}) :\n> {message.jump_url}"
                            )
                            await message.remove_reaction(
                                "\N{PARTY POPPER}", client.user
                            )
                            break

            else:
                pass

    if client.user.mentioned_in(message):
        target_channel = client.get_channel(int(won_channel))
        await target_channel.send(
            f"> You won giveaway from **{guild_name}**({msg_channel_name}) \n> {message.jump_url}"
        )
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(
                won_webhook_url, adapter=AsyncWebhookAdapter(session)
            )
            await webhook.send(
                f"> You won giveaway from **{guild_name}**({msg_channel_name}) \n> {message.jump_url}",
                username=won_webhook_name,
            )


async def repeat(message, target_channel, author_checker):
    Author = str(message.author.mention)
    Content = str(message.content)

    if len(message.attachments) > 0:
        for x in range(len(message.attachments)):
            attachment = message.attachments[x]
            if (
                attachment.filename.endswith(".jpg")
                or attachment.filename.endswith(".jpeg")
                or attachment.filename.endswith(".png")
                or attachment.filename.endswith(".webp")
                or attachment.filename.endswith(".gif")
            ):
                image = attachment.url
                if x == 0:
                    await target_channel.send(Author + " : \n" + Content + "\n" + image)
                if x > 0:
                    await target_channel.send(image)
            elif (
                "https://images-ext-1.discordapp.net" in message.content
                or "https://tenor.com/view/" in message.content
            ):
                image = message.content
                if x == 0:
                    await target_channel.send(Author + " : \n" + Content + "\n" + image)
                if x > 0:
                    await target_channel.send(image)

    elif len(message.attachments) <= 0:
        if message.content:
            if author_checker == True:
                await target_channel.send(Content)
            else:
                await target_channel.send(Author + " : \n" + Content)

    else:
        pass


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    target_channel = client.get_channel(int(cmd_logs))
    await target_channel.send("> We have logged in as {0.user}".format(client))
    await client.change_presence(status=discord.Status.idle, afk=True)


@client.event
async def on_message(message):

    msg = message.content
    embeds = message.embeds

    # For commands
    dictionary = []
    false_dictionary = []
    name_list = []
    print_list = []
    left_guild = []
    guild_set_list = []
    empty_string = ""
    remove_symbols = ["[", "(", ",", ")", "]"]
    i = 2

    # Auto-react if its GiveawayBot (Working well)
    for embed in embeds:
        if message.author.id == GiveawayBot_id:
            target_channel = client.get_channel(int(cmd_post))
            msg_channel = message.channel.id
            author = str(embed.author)
            guild_name = message.guild
            channel_name = message.channel
            await giveaway_react(
                target_channel,
                author,
                message,
                client.user.id,
                guild_name,
                message.author.id,
                msg_channel,
                channel_name,
            )

    # Auto-react if its GiveawayBoat (Working perfectly)
    for embed in embeds:
        if message.author.id == Giveaway_Boat_id:
            target_channel = client.get_channel(int(cmd_post))
            msg_channel = message.channel.id
            title = embed.title
            guild_name = message.guild
            channel_name = message.channel
            await giveaway_react(
                target_channel,
                title,
                message,
                client.user.id,
                guild_name,
                message.author.id,
                msg_channel,
                channel_name,
            )

    # Mention user if won Rumble (Working)
    if message.author.id == Rumble_Royale:
        if client.user.mentioned_in(message):
            target_channel = client.get_channel(int(cmd_post))
            await target_channel.send(
                f"> You won Rumble from {guild_name} ({channel_name}):\n{message.jump_url}"
            )
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    won_webhook_url, adapter=AsyncWebhookAdapter(session)
                )
                await webhook.send(
                    f"> You won Rumble from {guild_name} ({channel_name}):\n{message.jump_url}",
                    username=won_webhook_name,
                )

    if message.channel.id == int(cmd_input) and msg.startswith("+"):
        split_msg = msg.split()
        what = msg[1]
        id_letters = msg.split()[1]

        if what.lower() == words:
            if (id_letters.lower() in identify_list):
                while i < len(
                    split_msg
                ):  # While loop (Add everything after the 3rd word to a list)
                    returned_msg = await add(split_msg[i], what)
                    if returned_msg == False:
                        dictionary.append(split_msg[i])
                    else:
                        false_dictionary.append(split_msg[i])
                    i += 1
                # target_channel = client.get_channel(int(cmd_input))
                # await target_channel.send(f"> Added {dictionary} to {exclude_words}")

        if what.lower() == guild_id:
            if (id_letters.lower() in identify_list):
                while i < len(
                    split_msg
                ):  # While loop (Add everything after the 3rd word to a list)
                    returned_msg = await add(split_msg[i], what)
                    guild_name = client.get_guild(int(split_msg[i]))
                    if guild_name != None and returned_msg == False:
                        dictionary.append(f"{split_msg[i]} **{guild_name}**")
                    else:
                        false_dictionary.append(f"{split_msg[i]} **{guild_name}**")
                    i += 1
                # target_channel = client.get_channel(int(cmd_input))
                # await target_channel.send(f"> Added {dictionary} to {exclude_guild_id}")

        if what.lower() == channel_id:
            if (id_letters.lower() in identify_list):
                while i < len(
                    split_msg
                ):  # While loop (Add everything after the 3rd word to a list)
                    returned_msg = await add(split_msg[i], what)
                    channel_name = client.get_channel(int(split_msg[i]))
                    if channel_name != None and returned_msg == False:
                        dictionary.append(f"{split_msg[i]} **({channel_name})**")
                    else:
                        false_dictionary.append(f"{split_msg[i]} **{channel_name}**")
                    i += 1
                # target_channel = client.get_channel(int(cmd_input))
                # await target_channel.send(f"> Added {dictionary} to {exclude_channel_id}")

        if what.lower() == leave_id:
            if (id_letters.lower() in identify_list):
                while i < len(
                    split_msg
                ):  # While loop (Add everything after the 3rd word to a list)
                    returned_msg = await add(split_msg[i], what)
                    guild_name = client.get_guild(int(split_msg[i]))
                    if guild_name != None and returned_msg == False:
                        dictionary.append(f"{split_msg[i]} **{guild_name}**")
                    else:
                        false_dictionary.append(f"{split_msg[i]} **{guild_name}**")
                    i += 1
                # target_channel = client.get_channel(int(cmd_input))
                # await target_channel.send(f"> Added {dictionary} to {leave_guild_id}")

        target_channel = client.get_channel(int(cmd_input))
        if (id_letters.lower() in identify_list):
            if bool(false_dictionary) == False:
                await target_channel.send(f"> Added {dictionary}")
            elif bool(dictionary) == True and bool(false_dictionary) == True:
                await target_channel.send(
                    f"> Added {dictionary} \n> Already existed or Invalid {false_dictionary}"
                )
            elif (bool(dictionary) == False) and (bool(false_dictionary) == True):
                await target_channel.send(
                    f"> Already existed or Invalid {false_dictionary}"
                )

        else:
            pass

    if message.channel.id == int(cmd_input) and msg.startswith("-"):
        split_msg = msg.split()
        what = msg[1]
        id_letters = msg.split()[1]
        all_checker = msg.split()[2]

        if what.lower() == words:
            if (id_letters.lower() in identify_list):
                if all_checker == all_input:
                    dictionary = await fetch(id_letters, what)
                    await remove(all_input, what)

                else:
                    while i < len(
                        split_msg
                    ):  # While loop (Add everything after the 3rd word to a list)
                        returned_msg = await remove(split_msg[i], what)
                        if returned_msg == True:
                            dictionary.append(split_msg[i])
                        else:
                            false_dictionary.append(split_msg[i])
                        i += 1

        if what.lower() == guild_id:
            if (id_letters.lower() in identify_list):
                if all_checker == all_input:
                    all_list = await fetch(id_letters, what)
                    for i in all_list:
                        guild_name = client.get_guild(int(i))
                        dictionary.append(f"{i} **{guild_name}**")
                    await remove(all_input, what)

                else:
                    while i < len(
                        split_msg
                    ):  # While loop (Add everything after the 3rd word to a list)
                        returned_msg = await remove(split_msg[i], what)
                        if returned_msg == True:
                            guild_name = client.get_guild(int(split_msg[i]))
                            dictionary.append(f"{split_msg[i]} **({guild_name})**")
                        else:
                            false_dictionary.append(split_msg[i])
                        i += 1

        if what.lower() == channel_id:
            if (id_letters.lower() in identify_list):
                if all_checker == all_input:
                    all_list = await fetch(id_letters, what)
                    for i in all_list:
                        channel_name = client.get_guild(int(i))
                        dictionary.append(f"{i} **{channel_name}**")
                    await remove(all_input, what)

                else:
                    while i < len(
                        split_msg
                    ):  # While loop (Add everything after the 3rd word to a list)
                        returned_msg = await remove(split_msg[i], what)
                        if returned_msg == True:
                            channel_name = client.get_channel(int(split_msg[i]))
                            dictionary.append(f"{split_msg[i]} **({channel_name})**")
                        else:
                            false_dictionary.append(split_msg[i])
                        i += 1

        if what.lower() == leave_id:
            if (id_letters.lower() in identify_list):
                if all_checker == all_input:
                    all_list = await fetch(id_letters, what)
                    for i in all_list:
                        guild_name = client.get_guild(int(i))
                        dictionary.append(f"{i} **{guild_name}**")
                    await remove(all_input, what)

                else:
                    while i < len(
                        split_msg
                    ):  # While loop (Add everything after the 3rd word to a list)
                        returned_msg = await remove(split_msg[i], what)
                        if returned_msg == True:
                            guild_name = client.get_guild(int(split_msg[i]))
                            dictionary.append(f"{split_msg[i]} **({guild_name})**")
                        else:
                            false_dictionary.append(split_msg[i])
                        i += 1

        target_channel = client.get_channel(int(cmd_input))
        if (id_letters.lower() in identify_list):
            if bool(false_dictionary) == False:
                await target_channel.send(f"> Removed {dictionary}")
            elif bool(dictionary) == True and bool(false_dictionary) == True:
                await target_channel.send(
                    f"> Removed {dictionary} \n> Doesnt exists {false_dictionary}"
                )
            elif (bool(dictionary) == False) and (bool(false_dictionary) == True):
                await target_channel.send(f"> Doesnt exists {false_dictionary}")

        else:
            pass

    if message.channel.id == int(cmd_input) and msg.startswith("!fetch"):
        split_msg = msg.split()
        what = msg.split()[1]
        id_letters = msg.split()[2]
        result = await fetch(id_letters, what)

        if what.lower() == words and result != None:
            for i in result:
                clean_word = "".join(
                    (filter(lambda i: i not in remove_symbols, str(i)))
                )  # Remove anything that's in remove_symbol
                if i == result[-1]:  # If second last word
                    empty_string += clean_word
                else:
                    empty_string += f"{clean_word}, "

            target_channel = client.get_channel(int(cmd_input))
            await target_channel.send(f"> {empty_string}")

        if what.lower() == guild_id and result != None:
            for i in result:
                clean_word = "".join(
                    (filter(lambda i: i not in remove_symbols, str(i)))
                )  # Remove anything that's in remove_symbol
                guild_name = client.get_guild(int(clean_word))
                dictionary.append(f"{clean_word} **{guild_name}**")
                empty_string += f"{clean_word} "

            target_channel = client.get_channel(int(cmd_input))
            await target_channel.send(f"> {dictionary}")
            await target_channel.send(f"> {empty_string}")

        if what.lower() == channel_id and result != None:
            for i in result:
                clean_word = "".join(
                    (filter(lambda i: i not in remove_symbols, str(i)))
                )  # Remove anything that's in remove_symbol
                channel_name = client.get_channel(int(clean_word))
                dictionary.append(f"{clean_word} **{channel_name}**")
                empty_string += f"{clean_word} "

            target_channel = client.get_channel(int(cmd_input))
            await target_channel.send(f"> {dictionary}")
            await target_channel.send(f"> {empty_string}")

        if what.lower() == leave_id and result != None:
            for i in result:
                clean_word = "".join(
                    (filter(lambda i: i not in remove_symbols, str(i)))
                )  # Remove anything that's in remove_symbol
                guild_name = client.get_guild(int(clean_word))
                dictionary.append(f"{clean_word} **{guild_name}**")
                empty_string += f"{clean_word} "

            target_channel = client.get_channel(int(cmd_input))
            await target_channel.send(f"> {dictionary}")
            await target_channel.send(f"> {empty_string}")

        else:
            pass

    if message.channel.id == int(cmd_input) and msg.startswith("!leave"):
        guild_list = await fetch(identify_letters, leave_id)

        for guild in guild_list:
            clean_word = "".join(
                (filter(lambda guild: guild not in remove_symbols, str(guild)))
            )  # Remove anything that's in remove_symbol
            guild_client = client.get_guild(int(clean_word))
            guild_name = str(guild_client)
            dictionary = dictionary + [f"{clean_word} **{guild_name}**"]
            empty_string += f"{clean_word} "
            await guild_client.leave()
            await remove(clean_word, leave_id)
            await remove(clean_word, guild_id)

        target_channel = client.get_channel(int(cmd_input))
        await target_channel.send(f"> Left {dictionary}")
        await target_channel.send(f"> {empty_string}")

    if message.channel.id == int(cmd_input) and msg.startswith("!table"):
        table_check = await create_table()
        if table_check:
            target_channel = client.get_channel(int(cmd_input))
            await target_channel.send(f"Created Table: {table_check}")
        else:
            target_channel = client.get_channel(int(cmd_input))
            await target_channel.send(
                f"Failed to create table (Probably table ady existed"
            )


@client.event
# Rumble Royale Auto React (Working)
async def on_reaction_add(reaction, user):
    messages = reaction.message
    reaction_guild_id = str(messages.guild.id)
    guild_name = str(messages.guild)
    channel_name = str(messages.channel)
    reaction_channel_id = str(messages.channel.id)

    if user.id == Rumble_Royale:
        word_list = await fetch(identify_letters, words)
        guild_list = await fetch(identify_letters, guild_id)
        channel_list = await fetch(identify_letters, channel_id)
        
        # Check exception_guild_id and exclude_guild_id from json before joining
        if (
            reaction_guild_id not in guild_list
            and reaction_channel_id not in channel_list
        ):
            await asyncio.sleep(20)
            rumble_emoji = reaction.emoji
            if asyncio.sleep:
                try:
                    await messages.add_reaction(reaction.emoji)
                    if messages.add_reaction:
                        asyncio.sleep(1)
                        target_channel = client.get_channel(int(cmd_post))
                        rumble_msg = await target_channel.send(
                            f"> You joined Rumble from {guild_name} ({channel_name}):\n{messages.jump_url}"
                        )
                        async with aiohttp.ClientSession() as session:
                            webhook = Webhook.from_url(
                                join_webhook_url,
                                adapter=AsyncWebhookAdapter(session),
                            )
                            await webhook.send(
                                f"> You joined Rumble from {guild_name} ({channel_name}):\n{messages.jump_url}",
                                username=join_webhook_name,
                            )
                        await rumble_msg.add_reaction("✅")
                        check = (
                            lambda r, u: r.message.id == rumble_msg.id
                            and u == rumble_msg.author
                            and str(r.emoji) in "✅"
                        )
                        check2 = (
                            lambda m: m.channel == rumble_msg.channel
                            and m.content.lower() == "yes"
                        )  # working
                        check3 = lambda c: c.channel == messages.channel and any(
                            word in c.content.lower() for word in word_list
                        )
                        check4 = (
                            lambda r, u: r.message.id == rumble_msg.id
                            and u != rumble_msg.author
                            and str(r.emoji) in "✅"
                        )

                        while True:
                            tasks = [
                                asyncio.create_task(
                                    client.wait_for(
                                        "reaction_remove", check=check, timeout=60
                                    ),
                                    name="check_reaction_remove",
                                ),
                                asyncio.create_task(
                                    client.wait_for(
                                        "message", check=check2, timeout=60
                                    ),
                                    name="check_msg",
                                ),
                                asyncio.create_task(
                                    client.wait_for(
                                        "message", check=check3, timeout=60
                                    ),
                                    name="msg_scanner",
                                ),
                                asyncio.create_task(
                                    client.wait_for(
                                        "reaction_add", check=check4, timeout=60
                                    ),
                                    name="check_reaction_add",
                                ),
                            ]

                            done, pending = await asyncio.wait(
                                tasks,
                                return_when=(
                                    asyncio.FIRST_COMPLETED
                                    or asyncio.FIRST_EXCEPTION
                                ),
                            )

                            finished: asyncio.Task = list(done)[0]

                            for task in tasks:
                                try:
                                    task.cancel()
                                except asyncio.TimeoutError:
                                    await rumble_msg.edit(
                                        content=f"> You joined Rumble from {guild_name} ({channel_name}):\n> {messages.jump_url} (too late to unreact)"
                                    )
                                    return
                                except:
                                    return

                            try:
                                action = finished.get_name()
                                result = finished.result()
                            except asyncio.TimeoutError:
                                await rumble_msg.edit(
                                    content=f"> You joined Rumble from {guild_name} ({channel_name}):\n> {messages.jump_url} (too late to unreact)"
                                )
                                return
                            except:
                                return

                            if action == "check_msg":
                                await rumble_msg.edit(
                                    content=f"> Unreacted rumble via 'yes' from {guild_name} ({channel_name}):\n> {messages.jump_url}"
                                )
                                await reaction.remove(client.user)
                                break

                            elif action == "check_reaction_remove":
                                await rumble_msg.edit(
                                    content=f"> Unreacted rumble via emoji from {guild_name} ({channel_name}):\n> {messages.jump_url}"
                                )
                                await reaction.remove(client.user)
                                break

                            elif action == "msg_scanner":
                                await target_channel.send(
                                    f"> Potential fake rumble on {guild_name} ({channel_name}):\n> {messages.jump_url} <@&961002892897185862>"
                                )

                            elif action == "check_reaction_add":
                                await rumble_msg.edit(
                                    content=f"> Unreacted rumble via emoji from {guild_name} ({channel_name}):\n> {messages.jump_url}"
                                )
                                await reaction.remove(client.user)
                                break

                except:
                    pass


@client.event
async def on_member_ban(guild, user):
    if user.id == client.user.id:
        target_channel = client.get_channel(int(cmd_post))
        await target_channel.send(f"> You've been banned from {str(guild)}")


client.run(os.environ["token_user"])
