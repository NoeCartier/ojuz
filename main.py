import os
import discord
from discord.ext import commands,tasks
import datetime
import db
import update
import random
import re
import pytz


#LOCAL
"""
GUILD_ID           = 1117791942764396707
TRAINER_ROLE_ID    = 1341179125271887982
POTW_CHANNEL       = 1341182372921610281
LOG_CHANNEL        = 1341331653334798336
POTW_ROLE_ID       = 1341180071460864061
MY_ID              = 468810262263365643
AC_ROLE_ID         = 1343260330637398136
"""

#PROD

GUILD_ID           = 696724725279359097
TRAINER_ROLE_ID    = 696727567780282459
POTW_CHANNEL       = 1345135478529069086
LOG_CHANNEL        = -1
POTW_ROLE_ID       = 1345134997287469137
MY_ID              = 468810262263365643
AC_ROLE_ID         = -1


TOKEN = os.getenv("DISCORD_TOKEN")

paris_tz = pytz.timezone("Europe/Paris")

async def log(str):
    if(LOG_CHANNEL == -1):
        print(str)
        return
    channel = await bot.fetch_channel(LOG_CHANNEL)
    await channel.send(str)

async def chat(channel_id, str):
    channel = await bot.fetch_channel(channel_id)
    await channel.send(str)

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def show_leaderboard():
    potw_number = db.get_variable_value("potw_number")
    leaderboard = db.get_leaderboard()
    print(leaderboard)
    if leaderboard == []:
        await chat(POTW_CHANNEL, "`No submission found for the past POTW :(`")
        return
    
    leaderboard.sort(key=lambda x: x[1], reverse=True)
    embed = discord.Embed(title=f"Leaderboard for Problem #{potw_number}", color=0xFFD700)
    
    for i, entry in enumerate(leaderboard):
        user_id, score = entry
        user = await bot.fetch_user(user_id)
        embed.add_field(name=f"{i+1}. {user.name}", value=f"Score: {score * 100}%", inline=False)
    
    channel = await bot.fetch_channel(POTW_CHANNEL)
    await channel.send(embed=embed)

async def postPOTW():
    NO_PROBLEM = db.get_variable_value("potw_number") == 0
    if not NO_PROBLEM:
        await show_leaderboard()
    db.erase_leaderboard()
    guild = bot.get_guild(GUILD_ID)
    if(AC_ROLE_ID != -1):
        role = guild.get_role(AC_ROLE_ID)
        if role:
            for member in guild.members:
                if role in member.roles:
                    await member.remove_roles(role)
                    await log(f"Removed AC role from {member.display_name}")
    problem = db.get_highest_priority_problem()
    print(problem)
    await log(str(problem))
    await log("Posting POTW")
    channel = await bot.fetch_channel(POTW_CHANNEL)
    problem_id = problem[0]
    problem_code = problem[1]
    problem_title = problem[2]
    problem_priority = problem[3]
    problem_proposer = problem[4]
    problem_link = problem[5]
    potw_number = db.get_variable_value("potw_number")
    db.update_variable_value("potw_number", potw_number + 1)
    potw_number += 1
    db.update_variable_value("potw_problem_id", problem_id)
    db.update_problem_priority(problem_id, -1)
    embed = discord.Embed(description=f"# Problem #{potw_number} - {problem_title}\n### [{problem_code}]({problem_link})")
    embed.color = random.randint(0, 0xFFFFFF)
    embed.set_author(name="Problem of the Week")
    try:
        proposer_user = await bot.fetch_user(problem_proposer)  # Fetch user globally
        avatar_url = proposer_user.avatar.url if proposer_user.avatar else proposer_user.default_avatar.url
        embed.set_footer(
            text=f"Proposed by : {proposer_user.name}",
            icon_url=avatar_url
        )
        await log(f"The username for ID {problem_proposer} is {proposer_user.name}")
    except discord.NotFound:
        await log("User not found.")
    except discord.HTTPException:
        await log("An error occurred while fetching the user.")

    await channel.send(embed=embed)

    try:
        # Construct the file path
        pdf_id = problem_id
        file_path = f'statements/{pdf_id}.pdf'
        # Open the file and send it as an attachment
        with open(file_path, 'rb') as pdf_file:
            await channel.send(file=discord.File(pdf_file, f'{pdf_id}.pdf'))
        print(f"Uploaded {pdf_id}.pdf successfully!")
    
    except FileNotFoundError:
        await channel.send(f"File `{pdf_id}.pdf` not found")


    # Create a thread in the current channel
    thread = await channel.create_thread(
        name=f"Problem #{potw_number} - {problem_title}",
        type=discord.ChannelType.public_thread,  # You can also use private_thread
        auto_archive_duration=4320  # Auto-archive after 60 minutes of inactivity
    )
    await log(f"Thread '{thread.name}' created successfully!")

    # Store the thread ID in the database
    db.add_problem_thread(problem_id, thread.id)
    await log(f"Thread ID {thread.id} for problem {problem_id} stored in the database.")

    
async def upd():
    users = db.list_all_users()
    submissions = update.update_submissions(users)
    submissions = list(reversed(submissions))
    for iSub in range(len(submissions)):
        await log(str(submissions[iSub]))
        submission_id = submissions[iSub][0]
        submission_time = submissions[iSub][1]
        ojuz_handle = submissions[iSub][2]
        problem_name = submissions[iSub][3]
        language = submissions[iSub][4]
        score = submissions[iSub][5]

        user_id = db.get_user_id_by_ojuz_handle(ojuz_handle)
        result = re.search(r'\((.*?)\)', problem_name)
        problem_code = result.group(1) if result else None
        problem_id = db.get_problem_id_by_code(problem_code)
        if(user_id):
            await log("User found")
            best_score = db.check_best_score_of_user(user_id, problem_id)
            db.add_submission(submission_id, score, user_id, problem_id)
            await log("Submission added")
            if score > best_score:
                await log("New best score")
                if problem_id == db.get_variable_value("potw_problem_id"):
                    db.add_to_leaderboard(user_id, score)
                thread_id = db.get_thread_id_of_problem(problem_id)
                if thread_id:
                    await log("Thread found")
                    #thread = await bot.fetch_channel(thread_id)
                    if(score == 1.0):
                        await chat(thread_id, f":green_square: <t:{submission_time}:T> | <@{user_id}> solved the problem !")
                        guild = bot.get_guild(GUILD_ID)
                        member = guild.get_member(user_id)
                        if(AC_ROLE_ID != -1):
                            role = guild.get_role(AC_ROLE_ID)
                            if member and role:
                                await member.add_roles(role)
                                await log(f"Added AC role to {member.display_name}")
                    elif(score == 0.0) :
                        await chat(thread_id, f":red_square: <t:{submission_time}:T> | <@{user_id}> attempted the problem without success.")
                    else:
                        await chat(thread_id, f":yellow_square: <t:{submission_time}:T> | <@{user_id}> scored {score * 100} !")
    await log("Update done.")

@bot.event
async def on_ready():
    await log(str(f'{bot.user} is now online!!!'))
    #await bot.tree.sync()  # Sync slash commands with Discord
    NO_PROBLEM = db.get_variable_value("potw_number") == 0
    if(NO_PROBLEM):
        await postPOTW()
        NO_PROBLEM = False
    schedule_task.start()  # Start the scheduled task
    update_auto.start()  # Start the auto update task


@bot.command(name='register', description="Register with your OJ.uz handle")
async def register(ctx, handle: str):
    if db.add_user(ctx.author.id, handle):
        await ctx.send(f'You have been registered with the handle: {handle}')
        guild = bot.get_guild(GUILD_ID)
        member = await guild.fetch_member(ctx.author.id)
        role = guild.get_role(POTW_ROLE_ID)
        if member and role:
            # Add the role to the user
            await member.add_roles(role)
            await ctx.send(f"Role {role.name} has been added to {member.display_name}.")
        else:
            await ctx.send("Invalid user ID or role ID.")
    else:
        await ctx.send(f'An unexpected error occurred while registering. Please contact an admin.')
    


# Slash command to manually trigger queue processing
@bot.command(name="post_POTW", description="post the POTW")
async def post_POTW(ctx):
    guild = bot.get_guild(GUILD_ID)
    member = await guild.fetch_member(ctx.author.id)
    trainer_role = guild.get_role(TRAINER_ROLE_ID)
    if trainer_role in member.roles:
        await postPOTW()
    else:
        await log("You do not have permission to execute this command.")


@bot.command(name="update", description="Update the database")
async def update_command(ctx):
    await upd()

@bot.command(name='add_problem', description="Add a problem to the database")
async def add_problem(ctx, problem_code: str, problem_title: str, problem_priority: int, problem_link: str):
    guild = bot.get_guild(GUILD_ID)
    member = await guild.fetch_member(ctx.author.id)
    trainer_role = guild.get_role(TRAINER_ROLE_ID)
    if trainer_role not in member.roles:
        await ctx.send("You don't have permission to add problems.")
        return
    existing_problem_id = db.get_problem_id_by_code(problem_code)
    if existing_problem_id:
        db.update_problem_priority(existing_problem_id, problem_priority)
        db.update_problem_proposer(existing_problem_id, ctx.author.id)
        await log(f"Problem {problem_code} already exists. Updated priority and proposer.")
        return
    problem_proposer = ctx.author.id
    if db.add_problem(problem_code, problem_title, problem_priority, problem_proposer, problem_link):
        await log(f'Problem {problem_title} has been added to the database.')
    else:
        await log(f'An error occurred while adding the problem. Please try again.')




# Scheduled task to run daily at 7:42 AM
@tasks.loop(minutes=1)
async def schedule_task():
    now = datetime.datetime.now(paris_tz)
    if now.weekday() == 0 and now.hour == 7 and now.minute == 42:
        await log("It's time to post the POTW!")
        postPOTW()


@tasks.loop(minutes=5)  # Exécuter toutes les 5 minutes
async def update_auto():
    await upd()


# Run the bot with your token
bot.run(TOKEN)