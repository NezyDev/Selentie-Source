from dis import disco
from email.mime import base
import pstats
from re import L
import time
from turtle import title
from xml.dom.expatbuilder import parseFragmentString
from colorama import Cursor
import requests
import discord
import asyncio
import sqlite3
from discord.ext import commands
import random


data_base = sqlite3.connect("selentie.db")
curs = data_base.cursor()


PREFIX = "$"

selentie = commands.Bot( command_prefix=PREFIX )
selentie.remove_command('help')


@selentie.event
async def on_ready():
    print('[+] selentie-bot launched...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, languageid)".format('localization'))
    data_base.commit()
    print('[+] localization service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, messagecout)".format('messages'))
    data_base.commit()
    print('[+] message service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, commandcout)".format('commands'))
    data_base.commit()
    print('[+] commands service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, user, warns)".format('warnings'))
    data_base.commit()
    print('[+] warnings service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, userid, msgs, lvl)".format('level'))
    data_base.commit()
    print('[+] level service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(userid, hooby, about)".format('bio'))
    data_base.commit()
    print('[+] biography service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, working)".format('chatfilter'))
    data_base.commit()
    print('[+] chat filter service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, channel_id)".format('reports'))
    data_base.commit()
    print('[+] reports service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, user_role_id)".format('user_role'))
    data_base.commit()
    print('[+] verification service initialized...')
    data_base.execute("CREATE TABLE IF NOT EXISTS {}(servername, userid, status)".format('tickets'))
    data_base.commit()
    print('[+] ticket service initialized...')

    await selentie.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name='$help'))



@selentie.event
async def on_command_error(ctx, error):
    pass



@selentie.event
async def on_message( message ):
    await selentie.process_commands( message )

    author_id = message.author.id
    server_name = message.guild.name
    user_message = message.content.lower()


    server_localization = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()


    if server_localization == None:
        curs.execute('INSERT INTO localization VALUES(?, ?)', (f'{server_name}', f"0"))
        data_base.commit()
    else:
        pass
   

    ms_cout = curs.execute('SELECT messagecout FROM messages WHERE servername == ?', (f'{server_name}',)).fetchone()

    if ms_cout == None:
        curs.execute('INSERT INTO messages VALUES(?, ?)', (f'{server_name}', f"2"))
        data_base.commit()
    else:
        pass

    cmd_ct = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{server_name}',)).fetchone()

    if cmd_ct == None:
        curs.execute('INSERT INTO commands VALUES(?, ?)', (f'{server_name}', f"0"))
        data_base.commit()


    ct_fl = curs.execute('SELECT working FROM chatfilter WHERE servername == ?', (f'{server_name}',)).fetchone()

    if ct_fl == None:
        curs.execute('INSERT INTO chatfilter VALUES(?, ?)', (f'{server_name}', False))
        data_base.commit()
    else:
        pass


    reports = curs.execute('SELECT channel_id FROM reports WHERE servername == ?', (f'{server_name}',)).fetchone()

    if reports == None:
        curs.execute('INSERT INTO reports VALUES(?, ?)', (f'{server_name}', f'0'))
        data_base.commit()
    else:
        pass


    user_role_id = curs.execute('SELECT user_role_id FROM user_role WHERE servername == ?', (f'{server_name}',)).fetchone()

    if user_role_id == None:
        curs.execute('INSERT INTO user_role VALUES(?, ?)', (f'{server_name}', f'0'))
        data_base.commit()
    else:
        pass



    server_messages = curs.execute('SELECT messagecout FROM messages WHERE servername == ?', (f'{message.guild.name}',)).fetchone()
    

    cout_messsage = int(server_messages[0])
    cout_messsage += 1

    curs.execute('UPDATE messages SET messagecout == ? WHERE servername == ?', (f'{cout_messsage}', f'{message.guild.name}'))
    data_base.commit()


    is_filter_enabled = curs.execute('SELECT working FROM chatfilter WHERE servername == ?', (f'{server_name}',)).fetchone()


    if is_filter_enabled[0] == True:
        if 'fuck' in user_message or 'пизда' in user_message or 'сука' in user_message or 'пидор' in user_message or 'хуй' in user_message or 'очко' in user_message or 'евреи' in user_message or 'блять' in user_message or 'гандон' in user_message or 'пиздец' in user_message or 'pidor' in user_message or 'gay' in user_message or 'nigger' in user_message or 'вагина' in user_message or 'gandon' in user_message or 'конча' in user_message or 'шалава' in user_message or 'хуйня' in user_message:
            await message.channel.purge(limit = 1)

            await message.channel.send(f'{message.author.mention} ‹⛔› *filter detected bad word*. ‹⛔›')
        else:
            pass



    about_person = curs.execute('SELECT about FROM bio WHERE userid == ?', (f'{message.author.id}',)).fetchone()

    if about_person == None:
        curs.execute('INSERT INTO bio VALUES(?, ?, ?)', (f'{message.author.id}', 'not stated', 'not stated'))
        data_base.commit()
    else:
        pass


    user_messages = curs.execute('SELECT msgs FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()

    if user_messages == None:
        curs.execute('INSERT INTO level VALUES(?, ?, ?, ?)', (f'{server_name}', f'{author_id}', 1, 0))
        data_base.commit()
    else:
        got_message = int(user_messages[0]) + 1
        curs.execute('UPDATE level SET msgs == ? WHERE servername == ? AND userid == ?', (f'{got_message}', f'{server_name}', f'{author_id}'))
        data_base.commit()
        
        if got_message == 40:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 0:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (1, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='1')

                await message.channel.send(embed = emb)
            else:
                pass
        elif got_message == 100:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 1:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (2, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='2')

                await message.channel.send(embed = emb)
            else:
                pass
        elif got_message == 200:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 2:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (3, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='3')

                await message.channel.send(embed = emb)
            else:
                pass
        elif got_message == 550:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 3:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (4, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='4')

                await message.channel.send(embed = emb)
            else:
                pass
        elif got_message == 1000:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 4:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (5, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='5')

                await message.channel.send(embed = emb)
            else:
                pass
        elif got_message == 1500:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 5:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (6, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='6')

                await message.channel.send(embed = emb)
            else:
                pass
        elif got_message == 2000:
            level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{author_id}')).fetchone()
            if int(level[0]) == 6:
                curs.execute('UPDATE level SET lvl == ? WHERE servername == ? AND userid == ?', (7, f'{server_name}', f'{author_id}'))
                data_base.commit()

                emb = discord.Embed( title= message.author.name, colour = discord.Color.green())

                emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

                emb.add_field( name= message.author.name + '‹🎉› New Level:', value='7')

                await message.channel.send(embed = emb)
            else:
                pass




#set localization
@selentie.command(aliases = ['поставитьязык', 'setlanguage', 'поставить_локализацию', 'язык_сервера', 'set_language'])
@commands.has_permissions( administrator = True )
async def set_localization(ctx, language):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name
    localization_id = 0

    if language == "russian":
        localization_id = 100
    elif language == "espanol":
        localization_id = 200
    elif language == "english":
        localization_id = 0
    else:
        await ctx.send(f"{ctx.author.mention} ‹🚩› *incorrect language name. you can call* ``$language_list`` *to get information*.")
        return

    curs.execute('UPDATE localization SET languageid == ? WHERE servername == ?', (f'{localization_id}', f'{server_name}'))
    data_base.commit()
    await ctx.send(f"{ctx.author.mention} *successfully changed localization for this server*.")



@selentie.command()
@commands.has_permissions( administrator = True )
async def language_list(ctx):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    localization_id_str = str(localization_id)
    localization_id_cleared = localization_id_str.replace("('", "")
    localization_id_cleared2 = localization_id_cleared.replace("',)", "")

    if int(localization_id_cleared2) == 0:
        emb = discord.Embed( title= "Languages:", colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='‹🔷› english', value="```language have id 0.```")
        emb.add_field( name='‹🔷› russian', value="```language have id 100.```")
        emb.add_field( name='‹🔷› espanol', value="```language have id 200.```")

        await ctx.send(embed = emb)
    elif int(localization_id_cleared2) == 100:
        emb = discord.Embed( title= "Языки:", colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='‹🔷› english', value="```у языка айди 0.```")
        emb.add_field( name='‹🔷› russian', value="```у языка айди 100.```")
        emb.add_field( name='‹🔷› espanol', value="```у языка айди 200.```")

        await ctx.send(embed = emb)
    elif int(localization_id_cleared2) == 200:
        emb = discord.Embed( title= "lengua:", colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='‹🔷› english', value="```la lengua de Aidi 0.```")
        emb.add_field( name='‹🔷› russian', value="```la lengua de Aidi 100.```")
        emb.add_field( name='‹🔷› espanol', value="```la lengua de Aidi 200.```")

        await ctx.send(embed = emb)





@selentie.command()
@commands.has_permissions( administrator = True )
async def settings(ctx):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    localization_id_str = str(localization_id)
    localization_id_cleared = localization_id_str.replace("('", "")
    localization_id_cleared2 = localization_id_cleared.replace("',)", "")

    if int(localization_id_cleared2) == 0:
        emb = discord.Embed( title= "‹🔰› Settings:", colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='{}set_localization <language>'.format( PREFIX ), value="```sets localization of bot on current server.```")
        emb.add_field( name='{}set_report_channel <channel_id>'.format( PREFIX ), value="```sets a channel where reports will be send.```")
        emb.add_field( name='{}chatfilter <Enbale/Disable>'.format( PREFIX ), value="```sets chat filter enbabled or disabled on current server.```")
        emb.add_field( name='{}set_user_role <role_id>'.format( PREFIX ), value="```sets a user role to verify in current server.```")

        await ctx.send(embed = emb)
    elif int(localization_id_cleared2) == 100:
        emb = discord.Embed( title= "‹🔰› Настройки:", colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='{}set_localization <language>'.format( PREFIX ), value="```выставляет локализацию бота на этом сервере.```")
        emb.add_field( name='{}set_report_channel <channel_id>'.format( PREFIX ), value="```выставить канал куда репорты будут присылаться.```")
        emb.add_field( name='{}chatfilter <Enbale/Disable>'.format( PREFIX ), value="```включает или выключает фильтрацию чата на сервере.```")
        emb.add_field( name='{}set_user_role <role_id>'.format( PREFIX ), value="```выставить роль юзера для верификаций на этом сервере.```")

        await ctx.send(embed = emb)
    elif int(localization_id_cleared2) == 200:
        emb = discord.Embed( title= "‹🔰› Ajustes:", colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='{}set_localization <language>'.format( PREFIX ), value="```expone la localización del bot en este servidor.```")
        emb.add_field( name='{}set_report_channel <channel_id>'.format( PREFIX ), value="```poner un canal donde los reporteros serán enviados.```")
        emb.add_field( name='{}chatfilter <Enbale/Disable>'.format( PREFIX ), value="```activa o desactiva el filtrado de chat en el servidor.```")
        emb.add_field( name='{}set_user_role <role_id>'.format( PREFIX ), value="```establecer el rol de usuario para las verificaciones en este servidor.```")

        await ctx.send(embed = emb)



@selentie.command(aliases = ['server', 'statistic', 'сервер', 'статистика', 'stats'])
async def server_stats(ctx):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    commands_cout = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{server_name}',)).fetchone()
    total_cmd_cout = int(commands_cout[0])

    messages_cout = curs.execute('SELECT messagecout FROM messages WHERE servername == ?', (f'{server_name}',)).fetchone()
    messages_ct = int(messages_cout[0])

    is_filter_enabled = curs.execute('SELECT working FROM chatfilter WHERE servername == ?', (f'{server_name}',)).fetchone()

    total_filter = 'False'
    if is_filter_enabled[0] == False:
        total_filter = 'False'
    else:
        total_filter = 'True'

    server_icon = ctx.guild.icon_url

    if lang_id == 0:
        emb = discord.Embed( title= '***' + server_name + '***', colour = discord.Color.green())

        emb.set_thumbnail(url=server_icon)

        emb.add_field( name='‹📧› Messages:', value= '```' + str(messages_ct) + '```')
        emb.add_field( name='‹🔰› Chat Filter:', value= '```' + total_filter + '```')
        emb.add_field( name='‹👥› Members:', value='```' +  str(ctx.guild.member_count) + '```')
        emb.add_field( name='‹💬› Language:', value= '```' + "English" + '```')
        emb.add_field( name='‹💻› Selentie commands called:', value='```' + str(total_cmd_cout) +  '```')

        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed( title= '***' + server_name + '***', colour = discord.Color.green())

        emb.set_thumbnail(url=server_icon)

        emb.add_field( name='‹📧› Сообщения:', value= '```' + str(messages_ct) + '```')
        emb.add_field( name='‹🔰› Фильтрация Чата:', value= '```' + total_filter + '```')
        emb.add_field( name='‹👥› Участники:', value='```' +  str(ctx.guild.member_count) + '```')
        emb.add_field( name='‹💬› Язык:', value= '```' + "Русский" + '```')
        emb.add_field( name='‹💻› Всего комманд Selentie:', value='```' + str(total_cmd_cout) +  '```')

        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed( title= '***' + server_name + '***', colour = discord.Color.green())

        emb.set_thumbnail(url=server_icon)

        emb.add_field( name='‹📧› Mensajes:', value= '```' + str(messages_ct) + '```')
        emb.add_field( name='‹🔰› Filtrado De Chat:', value= '```' + total_filter + '```')
        emb.add_field( name='‹👥› Agentes:', value='```' +  str(ctx.guild.member_count) + '```')
        emb.add_field( name='‹💬› Idioma:', value= '```' + "Espanol" + '```')
        emb.add_field( name='‹💻› Total de comandos:', value='```' + str(total_cmd_cout) +  '```')

        await ctx.send(embed = emb)




@selentie.command()
async def help(ctx):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        emb = discord.Embed(title='‹📚› My Commands:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '{}clear <amount>'.format(PREFIX), value='```clearing messages in chat.```')
        emb.add_field(name= '{}verify'.format(PREFIX), value='```makes you verify on current server.```')
        emb.add_field(name= '{}ticket'.format(PREFIX), value='```creates a ticket.```')
        emb.add_field(name= '{}bio_commands'.format(PREFIX), value='```gives you biography commands.```')
        emb.add_field(name= '{}report <username> <reason>'.format(PREFIX), value='```reports a user for reason to special channel.```')
        emb.add_field(name= '{}joke'.format(PREFIX), value='```telling random joke.```')
        emb.add_field(name= '{}kick <username> <reason>'.format(PREFIX), value='```kicks user from current server.```')
        emb.add_field(name= '{}ban <username> <reason>'.format(PREFIX), value='```bans people from server for reason.```')
        emb.add_field(name= '{}unban <user_id>'.format(PREFIX), value='```unbans if user banned on server.```')
        emb.add_field(name= '{}warn <username> <reason>'.format(PREFIX), value='```gives warn to user, if you got 3 you will be banned.```')
        emb.add_field(name= '{}translate <text>'.format(PREFIX), value='```translates text into your localization.```')
        emb.add_field(name= '{}clearwarns <username>'.format(PREFIX), value='```removes warns from user.```')
        emb.add_field(name= '{}decode <text>'.format(PREFIX), value='```decodes encrypted text and pushes result.```')
        emb.add_field(name= '{}settings'.format(PREFIX), value='```sends list of settings.```')
        emb.add_field(name= '{}server_stats'.format(PREFIX), value='```shows list of server stats.```')
        emb.add_field(name= '{}servers'.format(PREFIX), value='```shows a cout of the server where are bot invited.```')
        emb.add_field(name= '{}language_list'.format(PREFIX), value='```shows list of languages.```')
        emb.add_field(name= '{}wink'.format(PREFIX), value='```returns a random anime winking gif.```')
        emb.add_field(name= '{}minecraft <nickname>'.format(PREFIX), value='```returns information about minecraft player.```')
        emb.add_field(name= '{}binary_encode <text>'.format(PREFIX), value='```returns encoded binary code.```')
        emb.add_field(name= '{}binary_decode <binary>'.format(PREFIX), value='```returns decoded text.```')
        emb.add_field(name= '{}ipinfo <ip>'.format(PREFIX), value='```return information about ip address.```')
        emb.add_field(name= '{}pat'.format(PREFIX), value='```returns a random anime patting gif.```')
        emb.add_field(name= '{}hug'.format(PREFIX), value='```returns a random anime hugging gif.```')
        emb.add_field(name= '{}set_localization <language>'.format(PREFIX), value='```sets a language localization to this server.```')

        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹📚› Мои Комманды:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '{}clear <amount>'.format(PREFIX), value='```очищает сообщения в чате.```')
        emb.add_field(name= '{}verify'.format(PREFIX), value='```верифицироваться на этом сервере.```')
        emb.add_field(name= '{}ticket'.format(PREFIX), value='```создаёться тикет.```')
        emb.add_field(name= '{}bio_commands'.format(PREFIX), value='```выдаёт комманды взаимодействия со своей биографией.```')
        emb.add_field(name= '{}report <username> <reason>'.format(PREFIX), value='```кинуть жалобу на пользователя по причине.```')
        emb.add_field(name= '{}joke'.format(PREFIX), value='```рассказывает случайную шутку.```')
        emb.add_field(name= '{}kick <username> <reason>'.format(PREFIX), value='```выгоняет участника с сервера.```')
        emb.add_field(name= '{}ban <username> <reason>'.format(PREFIX), value='```выдаёт бан пользователю по причине.```')
        emb.add_field(name= '{}unban <user_id>'.format(PREFIX), value='```разбанивает если пользователь забанен.```')
        emb.add_field(name= '{}warn <username> <reason>'.format(PREFIX), value='```выдаёт варн пользователю, если у него 3 варна, то бан.```')
        emb.add_field(name= '{}translate <text>'.format(PREFIX), value='```переводит текст в текст вашей локализации сервера.```')
        emb.add_field(name= '{}clearwarns <username>'.format(PREFIX), value='```удаляет все варны пользователя.```')
        emb.add_field(name= '{}decode <text>'.format(PREFIX), value='```декодирует текст и выдаёт результат.```')
        emb.add_field(name= '{}settings'.format(PREFIX), value='```высалает настройки.```')
        emb.add_field(name= '{}server_stats'.format(PREFIX), value='```показывает лист сервер статуса.```')
        emb.add_field(name= '{}servers'.format(PREFIX), value='```показывает количество серверов на которых находиться бот.```')
        emb.add_field(name= '{}language_list'.format(PREFIX), value='```показывает лист доступных языков к установке.```')
        emb.add_field(name= '{}wink'.format(PREFIX), value='```возращает случайную подмигивающию гифку с тянкой аниме.```')
        emb.add_field(name= '{}minecraft <nickname>'.format(PREFIX), value='```выдаёт информацию о майнкрафт игроке.```')
        emb.add_field(name= '{}binary_encode <text>'.format(PREFIX), value='```выдаёт зашифрованый текст в двочном(бинарном) коде.```')
        emb.add_field(name= '{}binary_decode <binary>'.format(PREFIX), value='```выдаёт расшифрованый текст.```')
        emb.add_field(name= '{}ipinfo <ip>'.format(PREFIX), value='```возращает информацию об айпи.```')
        emb.add_field(name= '{}pat'.format(PREFIX), value='```возращает случайную гифку похлопывание аниме тян.```')
        emb.add_field(name= '{}hug'.format(PREFIX), value='```возращает случайную гифку обнимающейся аниме тян.```')
        emb.add_field(name= '{}set_localization <language>'.format(PREFIX), value='```выставляет локализацию языка на этом сервере.```')

        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹📚› Mis Comandos:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '{}clear <amount>'.format(PREFIX), value='```borra los mensajes de chat.```')
        emb.add_field(name= '{}verify'.format(PREFIX), value='```verifique en este servidor.```')
        emb.add_field(name= '{}ticket'.format(PREFIX), value='```crea ticket.```')
        emb.add_field(name= '{}bio_commands'.format(PREFIX), value='```emite comando de interacción con su biografía.```')
        emb.add_field(name= '{}report <username> <reason>'.format(PREFIX), value='```lanzar una queja contra el usuario por una razón.```')
        emb.add_field(name= '{}joke'.format(PREFIX), value='```cuenta una broma al azar.```')
        emb.add_field(name= '{}kick <username> <reason>'.format(PREFIX), value='```expulsa a un miembro del servidor.```')
        emb.add_field(name= '{}ban <username> <reason>'.format(PREFIX), value='```emite Ban al usuario por una razón.```')
        emb.add_field(name= '{}unban <user_id>'.format(PREFIX), value='```desbarata si el usuario está Prohibido.```')
        emb.add_field(name= '{}warn <username> <reason>'.format(PREFIX), value='```da Varna al usuario, si tiene 3 Varna, entonces Ban.```')
        emb.add_field(name= '{}translate <text>'.format(PREFIX), value='```traduce texto a texto de la localización del servidor.```')
        emb.add_field(name= '{}clearwarns <username>'.format(PREFIX), value='```elimina todos los Varna del usuario.```')
        emb.add_field(name= '{}decode <text>'.format(PREFIX), value='```decodifica el texto y produce el resultado.```')
        emb.add_field(name= '{}settings'.format(PREFIX), value='```sale de la configuración.```')
        emb.add_field(name= '{}server_stats'.format(PREFIX), value='```muestra la hoja de estado del servidor.```')
        emb.add_field(name= '{}servers'.format(PREFIX), value='```muestra el número de servidores en los que se encuentra el bot.```')
        emb.add_field(name= '{}language_list'.format(PREFIX), value='```muestra la hoja de idiomas disponibles para la instalación.```')
        emb.add_field(name= '{}wink'.format(PREFIX), value='```revive un guiño al azar GIF con anime de tirón.```')
        emb.add_field(name= '{}minecraft <nickname>'.format(PREFIX), value='```da información sobre el jugador de Minecraft.```')
        emb.add_field(name= '{}binary_encode <text>'.format(PREFIX), value='```emite texto cifrado en código binario (binario) .```')
        emb.add_field(name= '{}binary_decode <binary>'.format(PREFIX), value='```emite texto descifrado.```')
        emb.add_field(name= '{}ipinfo <ip>'.format(PREFIX), value='```recupera información sobre IPI.```')
        emb.add_field(name= '{}pat'.format(PREFIX), value='```devuelve GIF aleatorio palmaditas anime Chan.```')
        emb.add_field(name= '{}hug'.format(PREFIX), value='```devuelve un GIF al azar abrazando anime Chan.```')
        emb.add_field(name= '{}set_localization <language>'.format(PREFIX), value='```expone la localización del idioma en este servidor.```')

        await ctx.send(embed = emb)



@selentie.command()
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 100):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    await ctx.channel.purge( limit = amount )

    if lang_id == 0:
        emb = discord.Embed( title= '‹📛› Cleared:', colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='📧 Messages:', value='*Deleted* ' + str(amount))

        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed( title= '‹📛› Очищено:', colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='📧 Сообщений:', value='*Удалено* ' + str(amount))

        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed( title= '‹📛› Limpio:', colour = discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field( name='📧 Mensajes:', value='*Remoto* ' + str(amount))

        await ctx.send(embed = emb)



@selentie.command()
@commands.has_permissions(administrator = True)
async def kick(ctx, username : discord.Member, *, kick_reason, ):
    server_name = ctx.message.guild.name
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    await ctx.channel.purge(limit = 1)

    await username.kick(reason=kick_reason)

    if lang_id == 0:
       emb = discord.Embed(title='‹🚩› Kicked:', colour=discord.Color.green())

       emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

       emb.add_field(name= f'{username}', value='Reason: ' + "```" + str(kick_reason) + "```")
        
       await ctx.send(embed = emb)
    elif lang_id == 100:
       emb = discord.Embed(title='‹🚩› Исключён:', colour=discord.Color.green())

       emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

       emb.add_field(name= f'{username}', value='Причина: ' + "```" + str(kick_reason) + "```")
        
       await ctx.send(embed = emb)
    elif lang_id == 200:
       emb = discord.Embed(title='‹🚩› Excluyo:', colour=discord.Color.green())

       emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

       emb.add_field(name= f'{username}', value='Razón: ' + "```" + str(kick_reason) + "```")
        
       await ctx.send(embed = emb)
    



@selentie.command()
@commands.has_permissions(administrator = True)
async def decode(ctx, *, text,):
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    response = requests.post('https://www.artlebedev.ru/tools/decoder/ajax.html', data={ 'msg': text })

    if response.status_code == 200:
        response_jsoned = response.json()
        decoded = response_jsoned['text']

        if lang_id == 0:
            emb = discord.Embed(title='‹🔓› Decoded:', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= 'Decoded String:', value='Total: ' + "```" + str(decoded) + "```")
        
            await ctx.send(embed = emb)
        elif lang_id == 100:
            emb = discord.Embed(title='‹🔓› Расшифровано:', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= 'Декодированая Строчка:', value='Итог: ' + "```" + str(decoded) + "```")
        
            await ctx.send(embed = emb)
        elif lang_id == 200:
            emb = discord.Embed(title='‹🔓› Descifro:', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= 'Costura Decodificada:', value='Resultado: ' + "```" + str(decoded) + "```")
        
            await ctx.send(embed = emb)
    else:
        if lang_id == 0:
            ctx.send(f'{ctx.author.mention} *request didnt got respond*.')
        elif lang_id == 100:
            ctx.send(f'{ctx.author.mention} *запрос не был успешен*.')
        elif lang_id == 200:
            ctx.send(f'{ctx.author.mention} *la solicitud no tuvo éxito*.')






@selentie.command()
@commands.has_permissions(administrator = True)
async def warn(ctx, username: discord.Member, *, warn_reason,):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    warns = curs.execute('SELECT warns FROM warnings WHERE user == ? AND servername == ?', (f'{username}', f'{server_name}')).fetchone()

    await ctx.channel.purge(limit = 1)

    if warns == None:
        curs.execute('INSERT INTO warnings VALUES(?, ?, ?)', (f'{server_name}', f'{username}', f'{1}'))
        data_base.commit()
        if lang_id == 0:
            await ctx.send(f'{username.mention} ‹❗› *You got first warn for* **{warn_reason}**.')
        elif lang_id == 100:
            await ctx.send(f'{username.mention} ‹❗› *Ты получил свой первый варн по причине* **{warn_reason}**.')
        elif lang_id == 200:
            await ctx.send(f'{username.mention} ‹❗› *Tienes tu primer varn por una razón* **{warn_reason}**.')
    if int(warns[0]) == 1:
        curs.execute('UPDATE warnings SET warns == ? WHERE user == ? AND servername == ?', (f'{2}', f'{username}', f'{server_name}'))
        data_base.commit()
        if lang_id == 0:
            await ctx.send(f'{username.mention} ‹❗› *You got second warn for* **{warn_reason}**.')
        elif lang_id == 100:
            await ctx.send(f'{username.mention} ‹❗› *Ты получил свой второй варн по причине* **{warn_reason}**.')
        elif lang_id == 200:
            await ctx.send(f'{username.mention} ‹❗› *Tienes tu segundo varn por una razón* **{warn_reason}**.')
    if int(warns[0]) == 2:
        curs.execute('UPDATE warnings SET warns == ? WHERE user == ? AND servername == ?', (f'{3}', f'{username}', f'{server_name}'))
        data_base.commit()
        if lang_id == 0:
            await username.ban(reason='warns limit reached.')

            emb = discord.Embed(title='‹🚨› Banned:', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= f'{username}', value='Reason: reached warns limit.')
        
            await ctx.send(embed = emb)
        elif lang_id == 100:
             await username.ban(reason='лимит варнов привышен.')

             emb = discord.Embed(title='‹🚨› Забанен:', colour=discord.Color.green())

             emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

             emb.add_field(name= f'{username}', value='Причина: привысил лимит варнов.')
        
             await ctx.send(embed = emb)
        elif lang_id == 200:
             await username.ban(reason='límite de Varna.')

             emb = discord.Embed(title='‹🚨› Prohibido:', colour=discord.Color.green())

             emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

             emb.add_field(name= f'{username}', value='La razón: el límite de varnov.')
        
             await ctx.send(embed = emb)




@selentie.command(aliases = ['убратьварны', 'удалитьварны', 'снятьварны', 'deletewarns', 'removewarns'])
@commands.has_permissions(administrator = True)
async def clearwarns(ctx, username: discord.Member):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    warns = curs.execute('SELECT warns FROM warnings WHERE user == ? AND servername == ?', (f'{username}', f'{server_name}')).fetchone()


    if warns == None:
        if lang_id == 0:
         await ctx.send(f'{username.mention} ‹❌› *You dont have warns!* ‹❌›')
        elif lang_id == 100:
         await ctx.send(f'{username.mention} ‹❌› *У тебя нету варнов!* ‹❌›')
        elif lang_id == 200:
         await ctx.send(f'{username.mention} ‹❌› *¡No tienes Varnas!* ‹❌›')
    else:
        curs.execute('UPDATE warnings SET warns == ? WHERE user == ? AND servername == ?', (f'{0}', f'{username}', f'{server_name}'))
        data_base.commit()
        if lang_id == 0:
          await ctx.send(f'{username.mention} ‹✅› *Your warns got deleted!* ‹✅›')
        elif lang_id == 100:
          await ctx.send(f'{username.mention} ‹✅› *Твои варны были сняты!* ‹✅›')
        elif lang_id == 200:
          await ctx.send(f'{username.mention} ‹✅› *¡Tus Varnas fueron filmadas!* ‹✅›')




@selentie.command()
@commands.has_permissions(administrator = True)
async def ban(ctx, username: discord.Member, *, ban_reason):
    server_name = ctx.message.guild.name

    await ctx.channel.purge(limit= 1)

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    if lang_id == 0:
        await username.ban(reason= ban_reason)

        emb = discord.Embed(title='‹🚨› Banned:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'{username}', value='Reason: ' + str(ban_reason))
        
        await ctx.send(embed = emb)
    elif lang_id == 100:
        await username.ban(reason=ban_reason)

        emb = discord.Embed(title='‹🚨› Забанен:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'{username}', value='Причина: ' + str(ban_reason))
        
        await ctx.send(embed = emb)
    elif lang_id == 200:
        await username.ban(reason=ban_reason)

        emb = discord.Embed(title='‹🚨› Prohibido:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'{username}', value='Razón: ' + str(ban_reason))
        
        await ctx.send(embed = emb)




@selentie.command()
@commands.has_permissions( administrator = True )
async def unban(ctx, id):
    server_name = ctx.message.guild.name

    await ctx.channel.purge( limit = 1 )

    banned_users = await ctx.guild.bans()
    
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

  
    user = await selentie.fetch_user(id)
    await ctx.guild.unban(user)

 
    if lang_id == 0:
            emb = discord.Embed(title= '‹✅› Unban', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= 'Unbaned:', value='User: ' + "```" +  str(user) + "```")
        
            await ctx.send(embed = emb)
    elif lang_id == 100:
            emb = discord.Embed(title= '‹✅› Разбан', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= 'Разбанен:', value='Пользователь: ' + "```" +  str(user) + "```")
        
            await ctx.send(embed = emb)
    elif lang_id == 200:
            emb = discord.Embed(title= '‹✅› Roto', colour=discord.Color.green())

            emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

            emb.add_field(name= 'Roto:', value='Usuario: ' + "```" +  str(user) + "```")
        
            await ctx.send(embed = emb)


        

@selentie.command()
async def translate(ctx, *, text):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        response = requests.get(f"https://t23.translatedict.com/1.php?p1=auto&p2=eng&p3={text}", json={ 'p1': 'auto', 'p2': 'eng', 'p3': text })
        translated = response.text

        emb = discord.Embed(title='‹⚡› Translated:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'Translated Text:', value= f'```{translated}```')
        
        await ctx.send(embed = emb)
    elif lang_id == 100:
        response = requests.get(f"https://t23.translatedict.com/1.php?p1=auto&p2=ru&p3={text}", json={ 'p1': 'auto', 'p2': 'ru', 'p3': text })
        translated = response.text

        emb = discord.Embed(title='‹⚡› Перевод:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'Перевод Текста:', value= f'```{translated}```')
        
        await ctx.send(embed = emb)
    elif lang_id == 200:
        response = requests.get(f"https://t23.translatedict.com/1.php?p1=auto&p2=es&p3={text}", json={ 'p1': 'auto', 'p2': 'es', 'p3': text })
        translated = response.text

        emb = discord.Embed(title='‹⚡› Traducción:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'Traducción De Texto:', value= f'```{translated}```')
        
        await ctx.send(embed = emb)




@selentie.command()
async def joke(ctx):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        response = requests.get('https://some-random-api.ml/joke')

        joke = response.json()['joke']
        await ctx.send(f'{ctx.author.mention} ' + "*" +  str(joke) + "*")
    elif lang_id == 100:
        response = requests.get('https://some-random-api.ml/joke')

        joke = response.json()['joke']

        translate = requests.get(f"https://t23.translatedict.com/1.php?p1=auto&p2=ru&p3={joke}", json={ 'p1': 'auto', 'p2': 'ru', 'p3': joke })
        translated_joke = translate.text
        await ctx.send(f'{ctx.author.mention} ' + "*" +  str(translated_joke) + "*")
    elif lang_id == 200:
        response = requests.get('https://some-random-api.ml/joke')

        joke = response.json()['joke']

        translate = requests.get(f"https://t23.translatedict.com/1.php?p1=auto&p2=es&p3={joke}", json={ 'p1': 'auto', 'p2': 'es', 'p3': joke })
        translated_joke = translate.text
        await ctx.send(f'{ctx.author.mention} ' + "*" +  str(translated_joke) + "*")




@selentie.command()
async def wink(ctx):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name

    response = requests.get('https://some-random-api.ml/animu/wink')
    gif = response.json()['link']
    await ctx.send(f'{ctx.author.mention} ' + str(gif))




@selentie.command()
async def pat(ctx):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name

    response = requests.get('https://some-random-api.ml/animu/pat')
    gif = response.json()['link']
    await ctx.send(f'{ctx.author.mention} ' + str(gif))




@selentie.command()
async def hug(ctx):
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    server_name = ctx.message.guild.name

    response = requests.get('https://some-random-api.ml/animu/hug')
    gif = response.json()['link']
    await ctx.send(f'{ctx.author.mention} ' + str(gif))



@selentie.command()
async def ipinfo(ctx, ip_address):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    response = requests.get(f'http://ip-api.com/json/{ip_address}')

    country = response.json()['country']
    contry_code = response.json()['countryCode']
    city = response.json()['city']
    provider = response.json()['org']
    zip_code = response.json()['zip']
    timezone = response.json()['timezone']
    lat = response.json()['lat']
    lon = response.json()['lon']

    if lang_id == 0:
        emb = discord.Embed(title='IP Information:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'‹🌍› Country:', value=country)
        emb.add_field(name= f'‹📑› Country Code:', value=contry_code)
        emb.add_field(name= f'‹🏠› City:', value=city)
        emb.add_field(name= f'‹🔌› Provider:', value=provider)
        emb.add_field(name= f'‹📬› Zip Code:', value=zip_code)
        emb.add_field(name= f'‹🕥› Timezone:', value=timezone)
        emb.add_field(name= f'‹⚫› lat:', value=lat)
        emb.add_field(name= f'‹⬛› lon:', value=lon)
        
        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='Информация об айпи:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'‹🌍› Регион:', value=country)
        emb.add_field(name= f'‹📑› Код Региона:', value=contry_code)
        emb.add_field(name= f'‹🏠› Город:', value=city)
        emb.add_field(name= f'‹🔌› Провайдер:', value=provider)
        emb.add_field(name= f'‹📬› Почтовый Индекс:', value=zip_code)
        emb.add_field(name= f'‹🕥› Часовой Пояс:', value=timezone)
        emb.add_field(name= f'‹⚫› широта:', value=lat)
        emb.add_field(name= f'‹⬛› долгота:', value=lon)
        
        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='Información sobre IPI:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= f'‹🌍› Región:', value=country)
        emb.add_field(name= f'‹📑› Código De Región:', value=contry_code)
        emb.add_field(name= f'‹🏠› Ciudad:', value=city)
        emb.add_field(name= f'‹🔌› Proveedor:', value=provider)
        emb.add_field(name= f'‹📬› Código Postal:', value=zip_code)
        emb.add_field(name= f'‹🕥› huso horario:', value=timezone)
        emb.add_field(name= f'‹⚫› latitud:', value=lat)
        emb.add_field(name= f'‹⬛› longitud:', value=lon)
        
        await ctx.send(embed = emb)




@selentie.command(aliases = ['я', 'me', 'bio', 'био', 'профиль', 'profile'])
async def me_profile(ctx):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    user_level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{ctx.author.id}')).fetchone()

    user_messages = curs.execute('SELECT msgs FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{ctx.author.id}')).fetchone()

    warns = curs.execute('SELECT warns FROM warnings WHERE user == ? AND servername == ?', (f'{ctx.author}', f'{server_name}')).fetchone()
    
    hooby = curs.execute('SELECT hooby FROM bio WHERE userid == ?', (f'{ctx.author.id}',)).fetchone()

    about = curs.execute('SELECT about FROM bio WHERE userid == ?', (f'{ctx.author.id}',)).fetchone()

    total_warns = 0
    if warns == None:
        total_warns = 0
    else:
        total_warns = warns[0]
    
    if lang_id == 0:
        emb = discord.Embed(title='Profile: ' + str(ctx.author.name), colour=discord.Color.green())

        emb.set_thumbnail(url=ctx.author.avatar_url)

        emb.add_field(name= '‹🔶› ID:', value= '```' + str(ctx.author.id) + '```') 
        emb.add_field(name= '‹✨› Lvl:', value= '```' + str(user_level[0]) + '```')
        emb.add_field(name= '‹📨› Messages:', value= '```' + user_messages[0] + '```')
        emb.add_field(name= '‹❗› Warnings:', value= '```' + str(total_warns) + '```')
        emb.add_field(name= '‹🎨› Hooby:', value= '```' + hooby[0] + '```')
        emb.add_field(name= '‹🎩› About:', value= '```' + about[0] + '```')
        
        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='Профиль: ' + str(ctx.author.name), colour=discord.Color.green())

        emb.set_thumbnail(url=ctx.author.avatar_url)

        emb.add_field(name= '‹🔶› Айди:', value= '```' + str(ctx.author.id) + '```') 
        emb.add_field(name= '‹✨› Уровень:', value= '```' + str(user_level[0]) + '```')
        emb.add_field(name= '‹📨› Сообщения:', value= '```' + user_messages[0] + '```')
        emb.add_field(name= '‹❗› Варны:', value= '```' + str(total_warns) + '```')
        emb.add_field(name= '‹🎨› Хооби:', value= '```' + hooby[0] + '```')
        emb.add_field(name= '‹🎩› Обо мне:', value= '```' + about[0] + '```')
        
        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='Perfil: ' + str(ctx.author.name), colour=discord.Color.green())

        emb.set_thumbnail(url=ctx.author.avatar_url)

        emb.add_field(name= '‹🔶› Aidi:', value= '```' + str(ctx.author.id) + '```') 
        emb.add_field(name= '‹✨› nivel:', value= '```' + str(user_level[0]) + '```')
        emb.add_field(name= '‹📨› mensajes:', value= '```' + user_messages[0] + '```')
        emb.add_field(name= '‹❗› Advertencia:', value= '```' + str(total_warns) + '```')
        emb.add_field(name= '‹🎨› Hooby:', value= '```' + hooby[0] + '```')
        emb.add_field(name= '‹🎩› Sobre:', value= '```' + about[0] + '```')
        
        await ctx.send(embed = emb)




@selentie.command()
async def write_hooby(ctx, *, user_hooby):
    server_name = ctx.message.guild.name

    curs.execute('UPDATE bio SET hooby == ? WHERE userid == ?', (f'{user_hooby}', f'{ctx.author.id}'))
    data_base.commit()

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        await ctx.send(f'{ctx.author.mention} *Updated hooby in your biography!* ‹✅›')
    elif lang_id == 100:
        await ctx.send(f'{ctx.author.mention} *Обновлена графа хооби в вашей биографии!* ‹✅›')
    elif lang_id == 200:
        await ctx.send(f'{ctx.author.mention} *Actualizado el Conde de Hobie en su biografía!* ‹✅›')




@selentie.command()
async def write_about(ctx, *, user_about):
    server_name = ctx.message.guild.name

    curs.execute('UPDATE bio SET about == ? WHERE userid == ?', (f'{user_about}', f'{ctx.author.id}'))
    data_base.commit()

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        await ctx.send(f'{ctx.author.mention} *Updated about me in your biography!* ‹✅›')
    elif lang_id == 100:
        await ctx.send(f'{ctx.author.mention} *Обновлена графа обо мне в вашей биографии!* ‹✅›')
    elif lang_id == 200:
        await ctx.send(f'{ctx.author.mention} *Gráfico actualizado sobre mí en su biografía!* ‹✅›')





@selentie.command(aliases = ['user', 'юзер', 'пользователь', 'view'])
async def view_person(ctx, username: discord.Member):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    user_level = curs.execute('SELECT lvl FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{username.id}')).fetchone()

    user_messages = curs.execute('SELECT msgs FROM level WHERE servername == ? AND userid == ?', (f'{server_name}', f'{username.id}')).fetchone()

    warns = curs.execute('SELECT warns FROM warnings WHERE user == ? AND servername == ?', (f'{username}', f'{server_name}')).fetchone()
    
    hooby = curs.execute('SELECT hooby FROM bio WHERE userid == ?', (f'{username.id}',)).fetchone()

    about = curs.execute('SELECT about FROM bio WHERE userid == ?', (f'{username.id}',)).fetchone()

    total_warns = 0
    if warns == None:
        total_warns = 0
    else:
        total_warns = warns[0]


    if lang_id == 0:
        emb = discord.Embed(title='User Profile: ' + str(username), colour=discord.Color.green())

        emb.set_thumbnail(url=username.avatar_url)

        emb.add_field(name= '‹🔶› ID:', value= '```' + str(ctx.author.id) + '```') 
        emb.add_field(name= '‹✨› Lvl:', value= '```' + str(user_level[0]) + '```')
        emb.add_field(name= '‹📨› Messages:', value= '```' + user_messages[0] + '```')
        emb.add_field(name= '‹❗› Warnings:', value= '```' + str(total_warns) + '```')
        emb.add_field(name= '‹🎨› Hooby:', value= '```' + hooby[0] + '```')
        emb.add_field(name= '‹🎩› About:', value= '```' + about[0] + '```')
        
        await ctx.send(embed = emb)
    if lang_id == 100:
        emb = discord.Embed(title='Профиль Пользователя: ' + str(username), colour=discord.Color.green())

        emb.set_thumbnail(url=username.avatar_url)

        emb.add_field(name= '‹🔶› Айди:', value= '```' + str(ctx.author.id) + '```') 
        emb.add_field(name= '‹✨› Уровень:', value= '```' + str(user_level[0]) + '```')
        emb.add_field(name= '‹📨› Сообщения:', value= '```' + user_messages[0] + '```')
        emb.add_field(name= '‹❗› Варны:', value= '```' + str(total_warns) + '```')
        emb.add_field(name= '‹🎨› Хооби:', value= '```' + hooby[0] + '```')
        emb.add_field(name= '‹🎩› Обо мне:', value= '```' + about[0] + '```')
        
        await ctx.send(embed = emb)
    if lang_id == 200:
        emb = discord.Embed(title='Perfil: ' + str(ctx.author.name), colour=discord.Color.green())

        emb.set_thumbnail(url=ctx.author.avatar_url)

        emb.add_field(name= '‹🔶› Aidi:', value= '```' + str(ctx.author.id) + '```') 
        emb.add_field(name= '‹✨› nivel:', value= '```' + str(user_level[0]) + '```')
        emb.add_field(name= '‹📨› mensajes:', value= '```' + user_messages[0] + '```')
        emb.add_field(name= '‹❗› Advertencia:', value= '```' + str(total_warns) + '```')
        emb.add_field(name= '‹🎨› Hooby:', value= '```' + hooby[0] + '```')
        emb.add_field(name= '‹🎩› Sobre:', value= '```' + about[0] + '```')
        
        await ctx.send(embed = emb)




@selentie.command()
async def bio_commands(ctx):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        emb = discord.Embed(title='‹👀› Bio Commands:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '{}write_hooby <text>'.format(PREFIX), value='```writes hooby into your biography.```')
        emb.add_field(name= '{}write_about <text>'.format(PREFIX), value='```writes about into your biography.```')
        emb.add_field(name= '{}me'.format(PREFIX), value='```check your biography.```')
        emb.add_field(name= '{}user <user_mention>'.format(PREFIX), value='```checks user biography.```')
        
        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹👀› Комманды Биографии:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '{}write_hooby <text>'.format(PREFIX), value='```записывает хооби в вашу биографию.```')
        emb.add_field(name= '{}write_about <text>'.format(PREFIX), value='```записывает информацию в графу обо мне в вашей биографии.```')
        emb.add_field(name= '{}me'.format(PREFIX), value='```показывает вашу биографию.```')
        emb.add_field(name= '{}user <user_mention>'.format(PREFIX), value='```показывает биографию пользователя.```')
        
        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹👀› Comandos Biografías:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '{}write_hooby <text>'.format(PREFIX), value='```escribe Hobie en tu biografía.```')
        emb.add_field(name= '{}write_about <text>'.format(PREFIX), value='```escribe la información en una columna sobre mí en su biografía.```')
        emb.add_field(name= '{}me'.format(PREFIX), value='```muestra tu biografía.```')
        emb.add_field(name= '{}user <user_mention>'.format(PREFIX), value='```muestra la biografía del usuario.```')

        await ctx.send(embed = emb)




@selentie.command()
async def binary_encode(ctx, *, text):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    response = requests.get('https://some-random-api.ml/binary', data={ 'encode': text })

    binary = response.json()['binary']

    if lang_id == 0:
        emb = discord.Embed(title='‹💻› Binary Encoder', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📃› Encoded:', value= '```' + binary + '```')

        await ctx.send(ctx.author.mention, embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹💻› Бинарный Шифровщик', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📃› Зашифровано:', value= '```' + binary + '```')

        await ctx.send(ctx.author.mention, embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹💻› Criptógrafo binario', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📃› De clave:', value= '```' + binary + '```')

        await ctx.send(ctx.author.mention, embed = emb)




@selentie.command()
async def binary_decode(ctx, *, binary_encoded):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    response = requests.get('https://some-random-api.ml/binary', data={ 'decode': binary_encoded })

    decoded = response.json()['text']

    if lang_id == 0:
        emb = discord.Embed(title='‹💻› Binary Decoder', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📃› Decoded:', value= '```' + decoded + '```')

        await ctx.send(ctx.author.mention, embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹💻› Бинарный Дешифровщик', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📃› Расшифровано:', value= '```' + decoded + '```')

        await ctx.send(ctx.author.mention, embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹💻› Descifrador Binario', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📃› Descifro:', value= '```' + decoded + '```')

        await ctx.send(ctx.author.mention, embed = emb)




@selentie.command()
async def minecraft(ctx, *, nickname):
    server_name = ctx.message.guild.name
    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    response = requests.get('https://some-random-api.ml/mc', data={ 'username': nickname })

    if response.status_code == 200:
        player_name = response.json()['username']
        uuid = response.json()['uuid']
        player_skin_thumbnail_url = 'https://crafatar.com/renders/body/' + str(uuid) + '?overlay=true'

        if lang_id == 0:
            emb = discord.Embed(title='Minecraft: ' + str(nickname), colour=discord.Color.green())

            emb.set_thumbnail(url= player_skin_thumbnail_url)

            emb.add_field(name= '‹🎭› Username:', value= '```' + player_name + '```')
            emb.add_field(name= '‹🎮› UUID:', value= '```' + uuid + '```')

            await ctx.send(embed = emb)
        elif lang_id == 100:
            emb = discord.Embed(title='Майнкрафт: ' + str(nickname), colour=discord.Color.green())

            emb.set_thumbnail(url= player_skin_thumbnail_url)

            emb.add_field(name= '‹🎭› Имя Игрока:', value= '```' + player_name + '```')
            emb.add_field(name= '‹🎮› UUID:', value= '```' + uuid + '```')

            await ctx.send(embed = emb)
        elif lang_id == 200:
            emb = discord.Embed(title='Minecraft: ' + str(nickname), colour=discord.Color.green())

            emb.set_thumbnail(url= player_skin_thumbnail_url)

            emb.add_field(name= '‹🎭› Nombre Del Jugador:', value= '```' + player_name + '```')
            emb.add_field(name= '‹🎮› UUID:', value= '```' + uuid + '```')

            await ctx.send(embed = emb)

    else:
        if lang_id == 0:
            await ctx.send(f'{ctx.author.mention} ‹❌› *Request didnt got respond.* ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} ‹❌› *Не удалось выполнить запрос.* ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} ‹❌› *No se pudo ejecutar la consulta.* ‹❌›')
        


@selentie.command()
@commands.has_permissions(administrator = True)
async def dm(ctx, user_id, *, message):
    await ctx.channel.purge(limit = 1)

    user = await selentie.fetch_user(user_id)

    await user.send(f'{message}')




@selentie.command()
@commands.has_permissions(administrator = True)
async def chatfilter(ctx, chat_filter):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])


    if chat_filter == 'Enable':
        curs.execute('UPDATE chatfilter SET working == ? WHERE servername == ?', (True, f'{server_name}'))
        data_base.commit()

        if lang_id == 0:
            await ctx.send(f'{ctx.author.mention} *chat filter enabled!* ‹✅›')
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} *фильтрация чата была включена! ‹✅›*')
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} *el filtrado de chat se ha habilitado!* ‹✅›')
    elif chat_filter == 'Disable':
        curs.execute('UPDATE chatfilter SET working == ? WHERE servername == ?', (False, f'{server_name}'))
        data_base.commit()

        if lang_id == 0:
            await ctx.send(f'{ctx.author.mention} *chat filter disabled!* ‹❎›')
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} *фильтрация чата была отключена!* ‹❎›')
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} *el filtrado de chat se ha desactivado!* ‹❎›')
    else:
        if lang_id == 0:
            await ctx.send(f'{ctx.author.mention} ‹❌› *incorrect argument!* ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} ‹❌› *не верный параметр комманды!* ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} ‹❌› *¡no es un parámetro de comando correcto!* ‹❌›')




@selentie.command(aliases = ['сервера', 'количество_серверов'])
async def servers(ctx):
    servers = len(selentie.guilds)
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if lang_id == 0:
        emb = discord.Embed(title='‹📱› Servers Cout:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹🔎› Checking:', value= '```' + str(servers) + '```')

        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹📱› Количество Серверов:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹🔎› Selentie Смотрит:', value= '```' + str(servers) + '```')

        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹📱› Número De Servidores:', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹🔎› Selentie Mirando:', value= '```' + str(servers) + '```')

        await ctx.send(embed = emb)




@selentie.command(aliases = ['канал_репортов', 'канал_жалоб', 'report_channel'])
@commands.has_permissions(administrator = True)
async def set_report_channel(ctx, channel_id):
    server_name = ctx.message.guild.name

    await ctx.channel.purge(limit = 1)

    channel = selentie.get_channel(channel_id)

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    curs.execute('UPDATE reports SET channel_id == ? WHERE servername == ?', (f'{channel_id}', f'{server_name}'))
    data_base.commit()

    if lang_id == 0:
        emb = discord.Embed(title='‹📒› Report Channel', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📎› Channel ID:', value= '```' + str(channel_id) + '```')

        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹📒› Канал Жалоб', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📎› Айди канала:', value= '```' + str(channel_id) + '```')

        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹📒› Canal De Quejas', colour=discord.Color.green())

        emb.set_thumbnail(url="https://media.discordapp.net/attachments/994739888723349587/994952048216915978/selentie.png?width=473&height=473")

        emb.add_field(name= '‹📎› Aidi canal:', value= '```' + str(channel_id) + '```')

        await ctx.send(embed = emb)




@selentie.command(aliases = ['репорт', 'жалоба'])
async def report(ctx, username: discord.Member, *, report_reason):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    reports_channel_id = curs.execute('SELECT channel_id FROM reports WHERE servername == ?', (f'{server_name}',)).fetchone()

    if int(reports_channel_id[0]) == 0:
        if lang_id == 0:
            await ctx.send(f'{ctx.author.mention} *Sorry, but report channel didnt exists in current server.*')
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} *Извини, но репорт канал не установлен на этом сервере.*')
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} *Lo siento, pero el canal de informes no está instalado en este servidor.*')
    else:
        channel = selentie.get_channel(int(reports_channel_id[0]))

        if lang_id == 0:
            emb = discord.Embed(title='‹📢› Report From: ' + str(ctx.author), colour=discord.Color.green())

            emb.set_thumbnail(url=username.avatar_url)

            emb.add_field(name= '‹📌› Reported User: ' + str(username) , value= 'Reason: ' + '```' + str(report_reason) + '```')

            await channel.send(embed = emb)
        elif lang_id == 100:
            emb = discord.Embed(title='‹📢› Жалоба От: ' + str(ctx.author), colour=discord.Color.green())

            emb.set_thumbnail(url=username.avatar_url)

            emb.add_field(name= '‹📌› Пользователь на которого жалоба: ' + str(username) , value= 'Причина: ' + '```' + str(report_reason) + '```')

            await channel.send(embed = emb)
        elif lang_id == 200:
            emb = discord.Embed(title='‹📢› Denuncia De: ' + str(ctx.author), colour=discord.Color.green())

            emb.set_thumbnail(url=username.avatar_url)

            emb.add_field(name= '‹📌› Usuario contra quien denuncia: ' + str(username) , value= 'Razón: ' + '```' + str(report_reason) + '```')

            await channel.send(embed = emb)




@selentie.command()
async def verify(ctx):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])


    user_role_id = curs.execute('SELECT user_role_id FROM user_role WHERE servername == ?', (f'{server_name}',)).fetchone()

    if int(user_role_id[0]) == 0:
        if lang_id == 0:
            await ctx.send(f'{ctx.author.mention} *User role not exists on*: ' + str(server_name))
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} *Роль пользователя не выставлена на сервере*: ' + str(server_name))
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} *El rol de usuario no está expuesto en el servidor*: ' + str(server_name))


    msg = 0

    if lang_id == 0:
        msg = await ctx.channel.send(f'{ctx.author.mention} *React this message to get verified*.')
        await msg.add_reaction('✅')
    elif lang_id == 100:
        msg = await ctx.channel.send(f'{ctx.author.mention} *Добавь реакцию на это сообщение чтобы быть верефицированым*.')
        await msg.add_reaction('✅')
    elif lang_id == 200:
        msg = await ctx.channel.send(f'{ctx.author.mention} *Agregue una reacción a este mensaje para ser verificado*.')
        await msg.add_reaction('✅')

    user_role = discord.utils.get(ctx.message.guild.roles, id=int(user_role_id[0]))


    def check(reaction, user):
        return user == ctx.author and reaction.message == msg
    # Waiting for the reaction
    reaction, user = await selentie.wait_for("reaction_add", check=check)
    await ctx.channel.purge(limit = 2)
    await ctx.author.add_roles( user_role )




@selentie.command(aliases = ['поставить_роль_пользователя', 'поставить_роль_юзера'])
@commands.has_permissions(administrator = True)
async def set_user_role(ctx, role_id):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    curs.execute('UPDATE user_role SET user_role_id == ? WHERE servername == ?', ( f'{role_id}', f'{server_name}',))
    data_base.commit()

    server_icon = ctx.guild.icon_url

    if lang_id == 0:
        emb = discord.Embed(title='‹🌐› Server: ' + str(server_name), colour=discord.Color.green())

        emb.set_thumbnail(url=server_icon)

        emb.add_field(name= '‹📌› Got user role:', value= '```' + str(role_id) + '```')

        await ctx.send(embed = emb)
    elif lang_id == 100:
        emb = discord.Embed(title='‹🌐› Сервер: ' + str(server_name), colour=discord.Color.green())

        emb.set_thumbnail(url=server_icon)

        emb.add_field(name= '‹📌› Получена Роль:', value= '```' + str(role_id) + '```')

        await ctx.send(embed = emb)
    elif lang_id == 200:
        emb = discord.Embed(title='‹🌐› Servidor: ' + str(server_name), colour=discord.Color.green())

        emb.set_thumbnail(url=server_icon)

        emb.add_field(name= '‹📌› Rol Obtenido:', value= '```' + str(role_id) + '```')

        await ctx.send(embed = emb)




@selentie.command(aliases = ['тикет', 'помощь'])
async def ticket(ctx):
    server_name = ctx.message.guild.name

    commands_called = curs.execute('SELECT commandcout FROM commands WHERE servername == ?', (f'{ctx.message.guild.name}',)).fetchone()
    total_commands = int(commands_called[0])
    total_commands += 1
    curs.execute('UPDATE commands SET commandcout == ? WHERE servername == ?', (f'{total_commands}', f'{ctx.message.guild.name}'))
    data_base.commit()

    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    msg = 0

    if lang_id == 0:
        msg = await ctx.channel.send(f'{ctx.author.mention} *React 📨 to create ticket*.')
        await msg.add_reaction('📨')
    elif lang_id == 100:
        msg = await ctx.channel.send(f'{ctx.author.mention} *Нажми реакцию 📨 чтобы создать тикет*.')
        await msg.add_reaction('📨')
    elif lang_id == 200:
        msg = await ctx.channel.send(f'{ctx.author.mention} *Presiona la reacción 📨 para crear un ticket*.')
        await msg.add_reaction('📨')

    def check(reaction, user):
        return user == ctx.author and reaction.message == msg
    # Waiting for the reaction
    reaction, user = await selentie.wait_for("reaction_add", check=check)
    await msg.delete()

    ticket_status = curs.execute('SELECT status FROM tickets WHERE servername == ? AND userid == ?', (f'{server_name}', f'{ctx.author.id}')).fetchone()

    if ticket_status == None:
        curs.execute('INSERT INTO tickets VALUES(?, ?, ?)', (f'{server_name}', f'{ctx.author.id}', f'0'))
        data_base.commit()
    else:
        pass

    total_ticket_status = curs.execute('SELECT status FROM tickets WHERE servername == ? AND userid == ?', (f'{server_name}', f'{ctx.author.id}')).fetchone()

    if int(total_ticket_status[0]) == 1:
        if lang_id == 0:
           await ctx.send(f'{ctx.author.mention} ‹💢›  *You already have not closed ticket!*. ‹💢› ')
        elif lang_id == 100:
            await ctx.send(f'{ctx.author.mention} ‹💢›  *У тебя уже есть не закрытый тикет!*. ‹💢› ')
        elif lang_id == 200:
            await ctx.send(f'{ctx.author.mention} ‹💢›  *¡Ya tienes un ticket no cerrado!*. ‹💢› ')
    elif int(total_ticket_status[0]) == 0:
        ticket_channel = await ctx.message.guild.create_text_channel(name=f'ticket - {ctx.author}')
        curs.execute('UPDATE tickets SET status == ? WHERE servername == ? AND userid == ?', (f'1', f'{server_name}', f'{ctx.author.id}'))
        data_base.commit()

        close_ticket = 0

        if lang_id == 0:
            close_ticket = await ticket_channel.send(f'{ctx.author.mention} *React ❌ to close ticket*.')
            await close_ticket.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and reaction.message == close_ticket
            # Waiting for the reaction
            reaction, user = await selentie.wait_for("reaction_add", check=check)
            await ticket_channel.delete()
            curs.execute('UPDATE tickets SET status == ? WHERE servername == ? AND userid == ?', (f'0', f'{server_name}', f'{ctx.author.id}'))
            data_base.commit()
        if lang_id == 100:
            close_ticket = await ticket_channel.send(f'{ctx.author.mention} *Нажми ❌ чтобы закрыть тикет*.')
            await close_ticket.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and reaction.message == close_ticket
            # Waiting for the reaction
            reaction, user = await selentie.wait_for("reaction_add", check=check)
            await ticket_channel.delete()
            curs.execute('UPDATE tickets SET status == ? WHERE servername == ? AND userid == ?', (f'0', f'{server_name}', f'{ctx.author.id}'))
            data_base.commit()
        if lang_id == 200:
            close_ticket = await ticket_channel.send(f'{ctx.author.mention} *Pulsa ❌ para cerrar el ticket*.')
            await close_ticket.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and reaction.message == close_ticket
            # Waiting for the reaction
            reaction, user = await selentie.wait_for("reaction_add", check=check)
            await ticket_channel.delete()
            curs.execute('UPDATE tickets SET status == ? WHERE servername == ? AND userid == ?', (f'0', f'{server_name}', f'{ctx.author.id}'))
            data_base.commit()





@clear.error
async def clear_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@kick.error
async def kick_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@set_localization.error
async def set_localization_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")



@decode.error
async def decode_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")



@warn.error
async def warn_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@clearwarns.error
async def clearwarns_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")



@ban.error
async def ban_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")



@translate.error
async def translate_erro(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")



@ipinfo.error
async def ipinfo_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@write_hooby.error
async def write_hooby_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")


        

@write_about.error
async def write_about_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@minecraft.error
async def minecraft_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")





@binary_encode.error
async def binary_encode_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")





@binary_decode.error
async def binary_decode_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@report.error
async def report_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@set_report_channel.error
async def set_report_channel_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




@chatfilter.error
async def chatfilter_error(ctx, error):
    author = ctx.author
    server_name = ctx.message.guild.name
    localization_id = curs.execute('SELECT languageid FROM localization WHERE servername == ?', (f'{server_name}',)).fetchone()
    lang_id = int(localization_id[0])

    if isinstance(error, commands.MissingRequiredArgument):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹❌› *seems like, you missed argument*. ‹❌›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹❌› *похоже, что вы не ввели параметр комманды*. ‹❌›')
        elif lang_id == 200:
            await ctx.send(f'{author.mention} ‹❌› *parece que no ha ingresado el parámetro de comando*. ‹❌›')
    elif isinstance(error, commands.MissingPermissions):
        if lang_id == 0:
            await ctx.send(f'{author.mention} ‹🌀› *seems like you dont have permissions to use that*. ‹🌀›')
        elif lang_id == 100:
            await ctx.send(f'{author.mention} ‹🌀› *похоже что у тебя нет прав на использование этой комманды*. ‹🌀›')
        elif lang_id == 200:
            await ctx.send(f"{author.mention} ‹🌀› *parece que no tienes permiso para usar este comando*. ‹🌀›")




selentie_token = "YOUR BOT TOKEN HERE"
selentie.run( selentie_token )