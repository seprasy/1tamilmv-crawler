# %%
from tamilmv import get_all_movies_from_list_page

language_wise_directories = {
    "tamil": "https://www.1tamilmv.click/index.php?/forums/forum/11-web-hd-itunes-hd-bluray/",
    # "malayalam": "https://www.1tamilmv.click/index.php?/forums/forum/36-web-hd-itunes-hd-bluray/"
}

movies_from_all_pages = []
for entry in language_wise_directories.items() :
    print("processing", entry)

    for i in range(1,2):
        curr_url =  entry[1]+ "page/" + str(i) + "/"
        movie_details = get_all_movies_from_list_page(curr_url)
        movies_from_all_pages += movie_details

print ("Got " + str(len(movies_from_all_pages)) + "movies: ")
for movie in movies_from_all_pages:
    print(movie.name)

# %%
import sqlite3

con = sqlite3.connect("movies.db")
con.execute("PRAGMA foreign_keys = 1")

for movie in movies_from_all_pages:
    key = movie.name + "-" + str(movie.year)
    try:
        result = con.execute("INSERT INTO movies (name, year, key, main_page) values ( ?, ?, ?, ?);", 
        (movie.name, movie.year, key , movie.main_page)) 
    except Exception as e:
        print("failed to insert movie " , e)
    
    for link in movie.torrents + movie.magnet_links :
        try: 
            result = con.execute("INSERT INTO links (key, link, link_type, quality,language) values ( ?, ?, ?, ?, ?);", 
            (key, link.link, link.link_type , link.quality, link.language))
        except Exception as e:
            print("failed to insert link ", e)

# %%
result = con.execute("select m.name, l.link, l.quality from movies as m  join links as l on l.key = m.key ;")
print (result.fetchall())