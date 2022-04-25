import asyncio
from get_access_token import AccessToken
from update_anime_list import UpdateAnimeList

# access_token_bot = AccessToken()
# access_token_bot.main()

update_bot = UpdateAnimeList()
asyncio.get_event_loop().run_until_complete(update_bot.main())
