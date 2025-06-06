import discord
import json
import logging
import asyncio
from discord.ext import commands
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='error.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ServerCloner:
    def __init__(self, token):
        self.token = token
        intents = discord.Intents.default()
        intents.guilds = True
        intents.guild_emojis = True
        intents.guild_messages = True
        intents.guild_reactions = True
        intents.guild_presences = True
        intents.members = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.source_guild = None
        self.target_guild = None

    async def clone_roles(self):
        try:
            existing_roles = [role.name for role in self.target_guild.roles]
            
            for role in self.source_guild.roles:
                if role.name not in existing_roles and role.name != "@everyone":
                    try:
                        await self.target_guild.create_role(
                            name=role.name,
                            permissions=role.permissions,
                            colour=role.colour,
                            hoist=role.hoist,
                            mentionable=role.mentionable
                        )
                        logging.info(f"Created role: {role.name}")
                        print(f"Created role: {role.name}")
                        await asyncio.sleep(1)
                    except Exception as e:
                        logging.error(f"Error creating role {role.name}: {str(e)}")
                        print(f"Error creating role {role.name}: {str(e)}")
        except Exception as e:
            logging.error(f"Error in clone_roles: {str(e)}")
            print(f"Error in clone_roles: {str(e)}")

    async def clone_categories_and_channels(self):
        try:
            for category in self.source_guild.categories:
                try:
                    # Create category
                    new_category = await self.target_guild.create_category(
                        name=category.name,
                        position=category.position
                    )
                    logging.info(f"Created category: {category.name}")

                    # Clone text channels in this category
                    for channel in category.text_channels:
                        try:
                            await self.target_guild.create_text_channel(
                                name=channel.name,
                                category=new_category,
                                topic=channel.topic,
                                slowmode_delay=channel.slowmode_delay,
                                nsfw=channel.nsfw,
                                position=channel.position
                            )
                            logging.info(f"Created text channel: {channel.name}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            logging.error(f"Error creating text channel {channel.name}: {str(e)}")

                    # Clone voice channels in this category
                    for channel in category.voice_channels:
                        try:
                            await self.target_guild.create_voice_channel(
                                name=channel.name,
                                category=new_category,
                                bitrate=channel.bitrate,
                                user_limit=channel.user_limit,
                                position=channel.position
                            )
                            logging.info(f"Created voice channel: {channel.name}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            logging.error(f"Error creating voice channel {channel.name}: {str(e)}")

                except Exception as e:
                    logging.error(f"Error creating category {category.name}: {str(e)}")

        except Exception as e:
            logging.error(f"Error in clone_categories_and_channels: {str(e)}")

    async def clone_emojis(self):
        try:
            for emoji in self.source_guild.emojis:
                try:
                    # Download emoji image
                    emoji_image = await emoji.read()
                    # Create emoji in target guild
                    await self.target_guild.create_custom_emoji(
                        name=emoji.name,
                        image=emoji_image
                    )
                    logging.info(f"Created emoji: {emoji.name}")
                    await asyncio.sleep(1)
                except Exception as e:
                    logging.error(f"Error creating emoji {emoji.name}: {str(e)}")
        except Exception as e:
            logging.error(f"Error in clone_emojis: {str(e)}")

    async def start_cloning(self, source_id, target_id):
        try:
            @self.bot.event
            async def on_ready():
                try:
                    self.source_guild = self.bot.get_guild(int(source_id))
                    self.target_guild = self.bot.get_guild(int(target_id))

                    if not self.source_guild or not self.target_guild:
                        raise ValueError("Could not find source or target guild")

                    logging.info(f"Starting clone from {self.source_guild.name} to {self.target_guild.name}")
                    
                    # Start cloning process
                    await self.clone_roles()
                    await self.clone_categories_and_channels()
                    await self.clone_emojis()
                    
                    logging.info("Cloning process completed")
                    await self.bot.close()
                except Exception as e:
                    logging.error(f"Error in on_ready: {str(e)}")
                    await self.bot.close()

            # Start the bot
            await self.bot.start(self.token)

        except Exception as e:
            logging.error(f"Error in start_cloning: {str(e)}")

def main():
    try:
        # Load configuration
        with open('config.json', 'r') as f:
            config = json.load(f)

        token = config.get('bot_token')
        if not token:
            token = input("Please enter your bot token: ")
            config['bot_token'] = token
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)

        source_id = input("Enter source server ID: ")
        target_id = input("Enter target server ID: ")

        # Create and run the cloner
        cloner = ServerCloner(token)
        asyncio.run(cloner.start_cloning(source_id, target_id))

    except Exception as e:
        logging.error(f"Error in main: {str(e)}")
        print(f"An error occurred. Check error.log for details.")

if __name__ == "__main__":
    main()
