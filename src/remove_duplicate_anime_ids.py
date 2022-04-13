import re
def remove_duplicate_anime_list():
    with open('./data/9anime_list.txt', 'r+') as file:
        anime_ids = re.findall('(http://myanimelist.net/anime/\d+)', file.read())
        anime_ids_remove_duplicates = list(set(anime_ids))
        file.seek(0)
        file.truncate()
        file.write('\n'.join(anime_ids_remove_duplicates))
remove_duplicate_anime_list()