# Discord Server Cloner

A powerful tool for cloning Discord servers, including roles, channels, categories, and emojis. Available in both GUI and command-line interfaces.

## ⚠️ Important Notice

This tool should only be used on servers where you have proper authorization and permissions. Unauthorized cloning of Discord servers may violate Discord's Terms of Service.

## Features

- Clone server roles with permissions
- Clone categories and channels (both text and voice)
- Clone server emojis
- Modern GUI interface with real-time progress tracking
- Detailed error logging
- Configuration saving for convenience
- Rate limit handling to prevent API abuse

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token with required permissions
- Proper permissions on both source and target servers

## Installation

1. Install Python from [python.org](https://python.org) if you haven't already
2. Clone or download this repository
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Create a Discord Bot at [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable required intents in the Bot section:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
3. Copy your bot token
4. Invite the bot to both source and target servers with required permissions

## Usage

### GUI Mode (Recommended)

1. Double-click `run_cloner.bat` and select option 1
2. Enter your bot token (will be saved for future use)
3. Enter source and target server IDs
4. Select which elements to clone
5. Click "Start Cloning" and monitor the progress

### Command Line Mode

1. Double-click `run_cloner.bat` and select option 2
2. Follow the prompts to enter:
   - Bot token (if not already saved)
   - Source server ID
   - Target server ID
3. Monitor the cloning progress in the console

## Configuration

The `config.json` file stores:
- Bot token
- Default source server ID
- Default target server ID

## Error Handling

- All errors are logged to `error.log`
- View detailed logs through the GUI's "View Logs" button
- Check the log file for troubleshooting

## Best Practices

1. Always verify you have proper permissions before cloning
2. Keep your bot token secure and never share it
3. Run a test clone on a small server first
4. Monitor the progress and check logs for any issues

## Troubleshooting

### Common Issues:

1. **Permission Errors**
   - Ensure the bot has administrator permissions in both servers
   - Verify the bot's role hierarchy

2. **Rate Limits**
   - The tool automatically handles rate limits
   - For large servers, the process may take longer

3. **Missing Elements**
   - Check error.log for specific failures
   - Verify bot permissions for specific actions

## Technical Details

- Built with discord.py
- Uses PySimpleGUI for the modern interface
- Implements asyncio for efficient API handling
- Includes rate limit handling and error logging

## Security Considerations

- Store your bot token securely
- Regularly rotate bot tokens if security is compromised
- Monitor server audit logs for unauthorized actions

## Limitations

- Cannot clone messages due to Discord API limitations
- Emoji copying may be limited by server boost level
- Some role permissions may require manual adjustment

## Support

For issues and support:
1. Check the error.log file
2. Verify your permissions and setup
3. Ensure all prerequisites are met

## Legal

This tool is provided for legitimate use cases only. Users are responsible for ensuring they have proper authorization for any server cloning operations.
