import json
import asyncio
import aiohttp
import re
import time

time_now = time.time()


class UpdateAnimeList:
    def __init__(self):
        # get access token
        with open("./data/access_token.json", "r") as file:
            self.access_token = json.load(file)["access_token"]
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.payload = {"status": "plan_to_watch"}

    # uses regex to find all the anime ids from the 9anime text file
    def get_anime_ids(self, anime_ids_path):
        with open(anime_ids_path, "r") as file:
            anime_ids = re.findall("(\d+)", file.read())
        return list(set(anime_ids))

    # asynchronously send put requests to myanimelist api with headers and payload
    async def update_list(self, anime_id, session, status_list):
        url = f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status"
        async with session.put(
            url, data=self.payload, headers=self.headers
        ) as response:
            status_list.append(response.status)
    
    # asynchronously send delete requests to myanimelist api with headers and payload
    async def delete_list(self, anime_id, session, status_list):
        url = f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status"
        async with session.delete(
            url, data=self.payload, headers=self.headers
        ) as response:
            status_list.append(response.status)

    async def main(self):
        anime_ids_path = "./data/9anime_list.txt"
        anime_ids = self.get_anime_ids(anime_ids_path)
        # get status code lists from all the requests made
        status_list = []
        async with aiohttp.ClientSession() as session:
            try:
                task = input("delete(d) or update(u) list?: ")
                if task == "d":
                    tasks = [
                        self.delete_list(anime_id, session, status_list)
                        for anime_id in anime_ids
                    ]
                elif task == "u":
                    tasks = [
                        self.update_list(anime_id, session, status_list)
                        for anime_id in anime_ids
                    ]
                r = await asyncio.gather(*tasks)
                print(status_list)
                if 500 in status_list:
                    print(
                        "Mal's server experienced server error,  please run the program one more time :D"
                    )
            except Exception as e:
                print(Exception)

