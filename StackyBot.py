import os
import discord
import datetime
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

eboard_members = {"President": ["<@324592281204031488>"],
                  "Vice_president": ["<@1080204682212933662>"],
                  "Treasurer": ["[Madou Thiare](<https://www.linkedin.com/in/madouthiare/>)"],
                  "Secretary": ["<@707711310074478605>"],
                  "Tech Leads": ["<@1078897463479517264>", "<@422538392337907712>", "<@541441680046424076>", "<@505766080816480257>"],
                  "Community": ["[Brianna Minus](<https://www.linkedin.com/in/brianna-minus-434467349/>)"],
                  "Event Coordinators": ["[David Buna](<https://www.linkedin.com/in/david-buna-79a280395/>)", "Nedra Banks"],
                  "Marketing": ["<@434438133786869760>", "<@782436954515701760>", "[Devin Terrel](<https://www.linkedin.com/in/devin-terrell05/>)" ],
                  "Outreach": ["[Abdul-Rahman Dauda](<https://www.linkedin.com/in/abdul--dauda01/>)", "[Jesse Igbide](<https://www.linkedin.com/in/jigbide/>)"]}

metrics = {324592281204031488: 0,
           1078897463479517264: 0,
           422538392337907712: 0,
           541441680046424076: 0,
           505766080816480257: 0}

checkMark = ":white_check_mark:"
crossOut = ":x:"

def checkCompleteMetric(techLeadId):
    if metrics[techLeadId] == 0:
        return crossOut
    else:
        return checkMark

@bot.event
async def on_ready():
    await bot.tree.sync()
    if not resetmetric_weekly.is_running():
        resetmetric_weekly.start()
    print(f"{bot.user} IS HERE BABY!")

# Start of Event listeners
# Something the bot does when something happens
@bot.event
async def on_message(msg):
    # exit if stacky is reading its own message
    if msg.author.id == bot.user.id:
        return 

    # exit if the message is not in the resource channels
    if (msg.channel.id != 1479158848647467161 and
        msg.channel.id != 1458598556020772974 and
        msg.channel.id != 1461112630206009404 and
        msg.channel.id != 1461113108734148830 and
        msg.channel.id != 1461113158906150932 and
        msg.channel.id != 1461114022945362235):
        return

    # exit if the message isnt a tech lead
    if (msg.author.id != 324592281204031488 and 
        msg.author.id != 1078897463479517264 and 
        msg.author.id != 422538392337907712 and 
        msg.author.id != 541441680046424076 and 
        msg.author.id != 505766080816480257):
        return

    # exit if the message doesn't tag stacky
    if bot.user not in msg.mentions:
        return

    # get tech lead and check off for this week
    currentTechLead = 0
    for techLead in metrics.keys():
        if techLead == msg.author.id:
            currentTechLead = techLead
            metrics[currentTechLead] = 1

    await msg.channel.send(f"Got you for this week, {msg.author.mention}!")

# Start of Slash commands
# Something the bot does when someone calls its '/' command
@bot.tree.command(name="hi", description="Say Hi to Stacky!")
async def hi(interation: discord.Interaction):
    username = interation.user.mention
    await interation.response.send_message(f"Well Hi there, {username}")


@bot.tree.command(name='eboard', description='List all eboard members!')
async def eboard(interaction: discord.Interaction):
    embed = discord.Embed(title="Current Eboard", description="A list of all eboard members")
    embed.add_field(name="President", value=f"{eboard_members['President'][0]}")
    embed.add_field(name="Vice-President", value=f"{eboard_members['Vice_president'][0]}")
    embed.add_field(name="Treasurer", value=f"{eboard_members['Treasurer'][0]}")
    embed.add_field(name="Secretary", value=f"{eboard_members['Secretary'][0]}")
    embed.add_field(name="Tech Leads", value=f"{eboard_members['Tech Leads'][0]}, {eboard_members['Tech Leads'][1]}, {eboard_members['Tech Leads'][2]}, {eboard_members['Tech Leads'][3]}")
    embed.add_field(name="Community", value=f"{eboard_members['Community'][0]}")
    embed.add_field(name="Event Coordinators", value=f"{eboard_members['Event Coordinators'][0]}, {eboard_members['Event Coordinators'][1]}")
    embed.add_field(name="Marketing", value=f"{eboard_members['Marketing'][0]}, {eboard_members['Marketing'][1]}, {eboard_members['Marketing'][2]}")
    embed.add_field(name="Outreach", value=f"{eboard_members['Outreach'][0]}, {eboard_members['Outreach'][1]}")

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='metrics', description='Display this weeks tech lead status metrics for resources!')
async def techmetrics(interaction: discord.Interaction):
    embed = discord.Embed(title="Tech Lead Metrics :bar_chart:", description="A place where you check if you posted a resource this week")
    embed.add_field(name="Josias", value=checkCompleteMetric(324592281204031488))
    embed.add_field(name="Tyson", value=checkCompleteMetric(541441680046424076))
    embed.add_field(name="Talan", value=checkCompleteMetric(1078897463479517264))
    embed.add_field(name="Vanita", value=checkCompleteMetric(422538392337907712))
    embed.add_field(name="Kareem", value=checkCompleteMetric(505766080816480257))

    await interaction.response.send_message(embed=embed)
    
# start of loop section
@tasks.loop(time=datetime.time(hour=23, minute=0))
async def resetmetric_weekly():
    day = datetime.datetime.now(datetime.timezone.utc).weekday()
    if day == 5:
        for techleadId in metrics.keys():
            metrics[techleadId] = 0


bot.run(TOKEN)