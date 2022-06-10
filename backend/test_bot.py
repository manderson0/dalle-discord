import discord
from io import BytesIO
import consts
import dalle_model
import os

if __name__ == '__main__':
    dalle_version = consts.DALLE_MODEL_MINI
    dalle_model = dalle_model.DalleModel(dalle_version)
    print("--> Model selected - DALL-E {}. Initializing...".format(dalle_version))
    print("--> DALL-E Bot is up and running!")

    client = discord.Client()

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$blend') and len(message.content) > 7:
            prompt = message.content[7:]
            await message.channel.send("You queried: \"{}\"".format(prompt))
            await message.channel.send("But will it blend?")
            generated_imgs = dalle_model.generate_images(prompt, 1)

            for img in generated_imgs:
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                with open('output.jpeg', 'wb') as f:
                    f.write(buffered.getbuffer())

            with open('output.jpeg', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send("\"{}\":".format(prompt))
                await message.channel.send(file=picture)


    client.run(os.environ['DISCORD_TOKEN'])
