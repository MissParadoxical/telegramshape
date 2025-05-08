# Essential Files for Deployment

When pushing this project to GitHub, you only need these files for a proper deployment:

## Core Bot Files

- `main.py` - Main entry point for the bot
- `bot.py` - Core Telegram bot functionality
- `db.py` - Database handler for API key storage
- `api_handler.py` - Integration with the Shapes API
- `.env.example` - Template for environment variables

## Deployment Files

- `Dockerfile` - Docker configuration
- `docker-compose.yml` - Docker Compose configuration
- `setup.sh` - Helper script for setup
- `start_bot.sh` - Helper script for starting the bot

## Documentation

- `README.md` - Main documentation
- `DEPLOYMENT.md` - Deployment guide
- `ESSENTIAL_FILES.md` - This file

## What to Ignore

The `.gitignore` file has been updated to exclude all the Replit-specific files and test files that are not needed for deployment. These include:

- `replit_app.py`
- `app.py`
- `.replit` and related Replit configuration files
- All `test_*.py` files
- Other testing and Replit-specific configuration files

## Quick Verification

To verify you have the essential files before pushing to GitHub, you can run this command:

```bash
git ls-files
```

The output should match the essential files listed above, plus any additional files you intentionally added.