import json
import asyncio
import aiohttp
import re
import time

time_now = time.time()

#get access token previously saved before
def get_access_token(access_token_file_path):
    with open(access_token_file_path, 'r') as file:
        access_token = json.load(file)['access_token']
    return access_token

#uses regex to find all the anime ids from the 9anime text file
def get_anime_ids(anime_ids_path):
    with open(anime_ids_path, 'r') as file:
        anime_ids = re.findall('(\d+)', file.read())
    return list(set(anime_ids))

#asynchronously send put requests to myanimelist api with headers and payload
async def update_list(access_token, anime_id, session, status_list):
    url = f'https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status'
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'status': 'plan_to_watch'}
    async with session.put(url, data=payload, headers=headers) as response:
        status_list.append(response.status)

#asynchronously send delete requests to myanimelist api with headers and payload
async def delete_list(access_token, anime_id, session, status_list):
    url = f'https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status'
    headers = {'Authorization': f'Bearer {access_token}'}
    payload = {'status': 'plan_to_watch'}
    async with session.delete(url, data=payload, headers=headers) as response:
        status_list.append(response.status)


async def main():
    access_token_file_path = './data/access_token.json'
    anime_ids_path = './data/9anime_list.txt'
    access_token = get_access_token(access_token_file_path)
    anime_ids = get_anime_ids(anime_ids_path)
    #get status code lists from all the requests made
    status_list = []
    async with aiohttp.ClientSession() as session:
        try:
            task = input('delete(d) or update(u) list?: ')
            if task == 'd':
                tasks = [
                    delete_list(access_token, anime_id, session, status_list)
                    for anime_id in anime_ids
                ]
            elif task == 'u':
                tasks = [
                    update_list(access_token, anime_id, session, status_list)
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


asyncio.get_event_loop().run_until_complete(main())
print(f'The program took {time.time()-time_now} seconds')