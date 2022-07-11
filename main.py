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