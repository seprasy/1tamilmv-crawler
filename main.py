#%%
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup



def get_data_from_movie_list_item(movie):

    main_content = movie.find("div", {"class": "ipsDataItem_main"})

    if main_content is None: 
        return None

    link = main_content.find("a", {"data-ipshover-target": True})

    if link is None:
        return None

    return {"name": link["title"], "link": link["href"] }


def get_torrent_links_from_movie_page(url):

    page_content = requests.get(url).text

    html_parsed = BeautifulSoup(page_content, "html.parser")

    # a[data-fileext="torrent"]

    torrent_links = html_parsed.find_all("a", {"data-fileext": "torrent"})

    all_torrents = []
    for torrent in torrent_links: 
        name = torrent.text
        link = torrent["href"]
        all_torrents.append({"name": name, "link": link})
    
    all_magnets = []

    # searching magnet links using the selector : a[href*='magnet']
    def check_link(link):
        if link is not None:
            return link.startswith("magnet")
        return False
    
    magnet_links = html_parsed.find_all("a", {"href":  check_link } )
    for magnet_link in magnet_links:
        link = magnet_link["href"]
        name = list(filter(lambda x: x.startswith("dn="),link.split("&")))[0].replace("dn=","")
        name = unquote(name)
        all_magnets.append({"name": name, "link": link})
    
    return {"torrentFiles": all_torrents, "magnetLinks": all_magnets}


def get_all_movies_from_list_page(url):

    page_content = requests.get(url).text

    html_parsed = BeautifulSoup(page_content, "html.parser")

    movie_list = html_parsed.find_all("li", {"class": "ipsDataItem"})

    all_movies = []
    for movie in movie_list:
        movie_data = get_data_from_movie_list_item(movie)
        if movie_data is not None :
            print("processing: " + movie_data["name"])
            torrents_magnets = get_torrent_links_from_movie_page(movie_data["link"])
            if len ( torrents_magnets["torrentFiles"]) > 0 or len ( torrents_magnets["magnetLinks"]) > 0 :
                movie_data["torrents"] =  torrents_magnets["torrentFiles"]
                movie_data["magnets" ]=  torrents_magnets["magnetLinks"] 
                all_movies.append(movie_data)
            else: 
                print("### NO TORRENTS FOUND")

    return all_movies


language_wise_directories = {
    "tamil": "https://www.1tamilmv.click/index.php?/forums/forum/11-web-hd-itunes-hd-bluray/",
    "malayalam": "https://www.1tamilmv.click/index.php?/forums/forum/36-web-hd-itunes-hd-bluray/"
}

movies_from_all_pages = []
for entry in language_wise_directories.items() :
    print("processing", entry)

    for i in range(1,2):

        curr_url =  entry[1]+ "page/" + str(i) + "/"
        movie_details = get_all_movies_from_list_page(curr_url)
        movies_from_all_pages += movie_details



print ("Got" + str(len(movies_from_all_pages)) + "movies: ")





