import discord
from discord.ext import commands
import os
from model import detect
# Making sure that my savedimages folder exists
os.makedirs('/savedimages/', exist_ok=True)


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)




#pycord stuff further
GUILD_IDS = [PUT YOUR GUILD IDS HERE!!!!] 

@bot.event
async def on_ready():
    print(f'I am in! My codename is: "{bot.user}"')




# Command to process the image
@bot.slash_command(
    name="process_image",
    description="Processes an attached image",
    guild_ids=GUILD_IDS
)
async def process_image(ctx,
                        weather:discord.Attachment):
    await ctx.response.defer()
    if not weather.content_type.startswith('image/'):
        await ctx.respond("Please attach a valid image file.", ephemeral=True)
        return

    # Save the image to a file
    save_path = f"savedimages/{weather.filename}"
    await weather.save(save_path)

    try:
        # Detect the class of the image
        class_name, confidence_score = detect(save_path)

        # Formulate response                                        I've got not clue why this doesn't round it up correctly
        response_message = f"The weather seems to be: {class_name}, I'm about {confidence_score:.2f}/1.00% sure that it is."
        sunny = "You shouldn't wear anything too warm, a light jacket and jogging pants/shorts should do the job"
        snowy = "Oh! My favourite weather! Seems a little cold, so get thick clothes if you aren't okay with catching a cold. Something like a furcoat would do the job."
        rainy = "Care to not catch a cold! I'd stay inside, but if you have to go out, get a raincoat and rubber shoes to not get your feet wet"
        # Respond to the interaction
        await ctx.respond(response_message)
        if class_name == "1 Sunny":
            await ctx.respond(sunny)
        elif class_name == "0 Rainy":
            await ctx.respond(rainy)
        elif class_name == "2 Snowy":
            await ctx.respond(snowy)

    except Exception as e:
        error_message = f"Error processing image: {str(e)}"
        await ctx.respond(error_message, ephemeral=True)





token = "GETYOUROWNTOKEN"
bot.run(token)
