import discord
from deep_translator import GoogleTranslator

client = discord.Client()
Languages = ['general-english', 'general-español', 'генеральный-русский',
             'allgemeines-deutsch', 'généralités-français']
LangCodes = ['en', 'es', 'ru', 'de', 'fr']
Marches = [['none','Sipendihi','00:00:00','00:00:00','00:00:00','00:00:00','00:00:00']]
TargetNames = ['Center', 'North', 'East', 'South', 'West']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global Languages
    global LangCodes
    global Marches
    global TargetNames
    
    if message.author == client.user:
        return

    for i in Languages:
        if message.channel.name == i:
            for channel in message.guild.text_channels:
                if channel != message.channel:
                    for j in range(0,len(LangCodes)):
                        if channel.name == Languages[j]:
                            msg = GoogleTranslator(source='auto', target=LangCodes[j]).translate(message.content)
                            await channel.send(message.author.name + ' - ' + msg)
            return

    if message.content.lower() == 'hi sipendibot' or message.content.lower() == 'hello sipendibot':
        await message.channel.send('Hello ' + message.author.name + ' :hugging:')
        return            

    if message.content.startswith('SetMarch'):
        msgsplit = message.content.split(' ')
        player = message.author.name
        index = 1
        if not msgsplit[1].isdigit():
            player = msgsplit[1]
            index = 2
        for march in Marches:
            if march[0] == message.guild.id and march[1] == player:
                march[int(msgsplit[index])+1] = msgsplit[index+1]
                await message.channel.send(player + '\'s march to ' + TargetNames[int(msgsplit[index])-1] + ' updated')
                return
        newMarch = [message.guild.id, player]
        for i in range(1,len(TargetNames)+1):
            if i == int(msgsplit[index]):
                newMarch.append(msgsplit[index+1])
            else:
                newMarch.append('00:00:00')
        Marches.append(newMarch)
        await message.channel.send(player + '\'s march to ' + TargetNames[int(msgsplit[index])-1] + ' added')
        print(player + '\'s guild ID is ' + str(message.guild.id))
        return

    if message.content.startswith('Sipendibot ClearMarches'):
        #for march in Marches:
        for i in range(len(Marches),0):
            if Marches[i][0] == message.guild.id:
                Marches.remove(march)
        await message.channel.send('All marches cleared')
        return

    if message.content.lower().startswith('sipendibot help'):
        msg = 'Sipendibot stores march data to 5 targets and will calculate the time each person needs to send at to arrive ' + \
            'at a secified time, The target is selected by number, 1 = Center, 2 = North, 3 = East, 4 = South, 5 = West\n\n' + \
            'To add a march time send \'SetMarch player(optional) x HH:MM:SS\' If you do not include a players name then the ' + \
            'author of the message will be used. x is the number for which target you are assigning a march to.\n\n' + \
            'You can check the marches already assigned with the command \'Sipendibot Status\' and clear marches with the command ' \
            '\'Sipendibot ClearMarches player(optional)\' if no player is specified then all marches will be cleared'
        await message.channel.send(msg)
        return

    if message.content.lower().startswith('sipendibot status'):
        messages = ['Marches to Center: ', 'Marches to North: ', 'Marches to East: ', 'Marches to South: ',
                    'Marches to West: ']
        for i in range(0,5):
            for march in Marches:
                if march[0] == message.guild.id and march[i+2] != '00:00:00':
                    messages[i] += march[1] + ' = ' + march[i+2] + ', '
            await message.channel.send(messages[i])

    if message.content.startswith('AttackTarget'):
        msgsplit = message.content.split(' ')
        target = (int)(msgsplit[1])
        time = msgsplit[2]
        for i in range(3,len(msgsplit)):
            time = add_time(time,msgsplit[i])
        for rally in Marches:
            if rally[0] == message.guild.id and rally[target+1] != '00:00:00':
                await message.channel.send(rally[1] + ', please send troops at ' + subtract_time(time,rally[target+1]))
        return

def add_time(time1,time2):
    times1 = time1.split(':')
    times2 = time2.split(':')
    remainder = 0
    seconds = int(times1[2]) + int(times2[2])
    if seconds > 59:
        seconds = seconds - 60
        remainder = 1
    minutes = int(times1[1]) + int(times2[1]) + remainder
    remainder = 0
    if minutes > 59:
        minutes = minutes - 60
        remainder = 1
    hours = int(times1[0]) + int(times2[0]) + remainder
    if hours > 23:
        hours = hours - 24
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

def subtract_time(time1,time2):
    times1 = time1.split(':')
    times2 = time2.split(':')
    remainder = 0
    seconds = int(times1[2]) - int(times2[2])
    if seconds < 0:
        seconds = seconds + 60
        remainder = 1
    minutes = int(times1[1]) - int(times2[1]) - remainder
    remainder = 0
    if minutes < 0:
        minutes = minutes + 60
        remainder = 1
    hours = int(times1[0]) - int(times2[0]) - remainder
    if hours < 0:
        hours = hours + 24
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

client.run('********************************************************')
