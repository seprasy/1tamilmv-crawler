
#%%
import re
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from model import Movie, Link


def get_data_from_movie_list_item(movie):

    main_content = movie.find("div", {"class": "ipsDataItem_main"})

    if main_content is None: 
        return None

    link = main_content.find("a", {"data-ipshover-target": True})

    if link is None:
        return None

    movie = Movie()
    movie.name = link['title']
    movie.main_page = link['href']
    return movie

def parse_name(name):
    name_exp = re.compile("(?:www\.[\.\w]+)? ?(?:- )?(?P<name>.*) \((?P<year>\d\d\d\d)\) (?P<language>tamil|malayalam|hindi|kannada|telugu|english)? ?(?P<quality>.*)",re.RegexFlag.IGNORECASE)
    parsed_details = name_exp.match(name.strip())
    if parsed_details is None:
        print("##### link doesn't match : ", name, " ###")
        return None
    result = {}
    result["name"] = parsed_details.group("name").strip()
    result["year"] = parsed_details.group("year")
    result["language"] = parsed_details.group("language")
    result["quality"] = parsed_details.group("quality")
    return result

def get_torrent_links_from_movie_page(url):

    page_content = requests.get(url).text

    html_parsed = BeautifulSoup(page_content, "html.parser")

    # a[data-fileext="torrent"]

    torrent_links = html_parsed.find_all("a", {"data-fileext": "torrent"})

    all_torrents = []
    for torrent in torrent_links: 
        name = torrent.text
        torrent_link = torrent["href"]
        torrent_data = parse_name(name)


        link = Link()
        link.link = torrent_link
        link.link_type = "torrent_file"
        if torrent_data is not None:
            link.name = torrent_data["name"]
            link.quality = torrent_data["quality"]
            link.language = torrent_data["language"] 
        else:
            link.name = name
        
        all_torrents.append(link)
    
    all_magnets = []

    # searching magnet links using the selector : a[href*='magnet']
    def check_link(link):
        if link is not None:
            return link.startswith("magnet")
        return False
    
    magnet_links = html_parsed.find_all("a", {"href":  check_link } )
    for magnet_link_elem in magnet_links:
        magnet_link = magnet_link_elem["href"]
        name = list(filter(lambda x: x.startswith("dn="),magnet_link.split("&")))[0].replace("dn=","")
        name = unquote(name)
        torrent_data = parse_name(name)
        link = Link()
        link.link = magnet_link
        link.link_type = "magnet"

        if torrent_data is not None:
            link.quality = torrent_data["quality"]
            link.name = torrent_data["name"]
            link.language = torrent_data["language"] 
        else: 
            link.name = name
        
        all_magnets.append(link)
    
    return {"torrentFiles": all_torrents, "magnetLinks": all_magnets}


def get_all_movies_from_list_page(url):

    page_content = requests.get(url).text

    html_parsed = BeautifulSoup(page_content, "html.parser")

    movie_list = html_parsed.find_all("li", {"class": "ipsDataItem"})

    all_movies = []
    for movie_element in movie_list:
        movie = get_data_from_movie_list_item(movie_element)
        if movie is not None :
            print("processing: " + movie.name)
            parsed_name = parse_name(movie.name)
            if parsed_name is not None:
                movie.year = parsed_name["year"] 
                movie.name = parsed_name["name"] 
            torrents_magnets = get_torrent_links_from_movie_page(movie.main_page)
            if len ( torrents_magnets["torrentFiles"]) > 0 or len ( torrents_magnets["magnetLinks"]) > 0 :
                movie.torrents  =  torrents_magnets["torrentFiles"]
                movie.magnet_links =  torrents_magnets["magnetLinks"] 
                all_movies.append(movie)
            else: 
                print("### NO TORRENTS FOUND")

    return all_movies