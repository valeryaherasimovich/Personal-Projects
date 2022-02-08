!pip install xmltodict
import requests
import json
import xmltodict
import matplotlib.pyplot as plt
import skimage.io
import wordcloud
import textblob
import nltk
nltk.download("punkt")
#This code will get a movie name from the user and ask which analysis they would like to do on that movie. Based on the selection this code will search for the correct information and print out the result.
print("Welcome to the movie analysis tool!")
analysis = "yes"

while analysis == "yes":
  base_url = "https://www.omdbapi.com/?r=xml&apikey=4f2f75c0&t="
  movie = input("What movie would you like to analyze?")
  blob = textblob.TextBlob(movie)
  movie = blob.correct()
  full_url = base_url + str(movie)
  response = requests.get(full_url)
  if response:
    data = xmltodict.parse(response.text)
    option = input("What would you like to see (background/reception/poster/wordcloud/sentiment)?")
    blob = textblob.TextBlob(option)
    option = blob.correct()
    if option == "background":
      year = data["root"]["movie"]["@year"]
      rating = data["root"]["movie"]["@rated"]
      runtime = data["root"]["movie"]["@runtime"]
      genre = data["root"]["movie"]["@genre"]
      actors = data["root"]["movie"]["@actors"]
      plot = data["root"]["movie"]["@plot"]
      print("Year: ",year)
      print("Rating: ",rating)
      print("Runtime: ",runtime)
      print("Genre: ",genre)
      print("Actors: ",actors)
      print("Plot: ",plot)
    elif option == "reception":
      awards = data["root"]["movie"]["@awards"]
      mtscore = data["root"]["movie"]["@metascore"]
      imdb = data["root"]["movie"]["@imdbRating"]
      print("Awards: ",awards)
      print("Metascore: ",mtscore)
      print("IMDb rating: ",imdb)
    elif option == "poster":
      poster = data["root"]["movie"]["@poster"]
      image = skimage.io.imread(poster)
      plt.imshow(image, interpolation = "bilinear")
      plt.axis("off")
      plt.show()
    elif option == "wordcloud":
      response = requests.get("https://dgoldberg.sdsu.edu/515/imdb/"+str(movie)+".json")
      if response:
        data = json.loads(response.text)
        text = ""
        for line in data:
            review = line["Review text"]
            text = text + review + " "
        cloud = wordcloud.WordCloud(width = 2000, height = 2000, background_color = "black", colormap = "GnBu")
        cloud.generate(text)
        plt.imshow(cloud, interpolation = "bilinear")
        plt.axis("off")
        plt.show()
      else:
        print("Sorry, the tool could not successfully load wordcloud for this movie. Please try another analysis or movie.")
    elif option == "sentiment":
      response = requests.get("https://dgoldberg.sdsu.edu/515/imdb/"+str(movie)+".json")
      if response:
        for review in json.loads(response.text):
          review = review["Review text"]
          blob = textblob.TextBlob(review)
          sentences = blob.sentences
          polarity = 0
          subjectivity = 0
          for sentence in sentences:
            polarity = polarity + sentence.polarity
            subjectivity = subjectivity + sentence.subjectivity
          polarity = polarity / len(sentences)
          subjectivity = subjectivity / len(sentences)
        print("Average IMDb review polarity:" ,polarity)
        print("Average IMDb review subjectivity:" ,subjectivity)
      else:
        print("Sorry, the tool could not successfully load any IMDb reviews for this movie. Please try another analysis or movie.")
    else:
      print("Sorry that analysis is not supported. Please try again")
    analysis = input("Would you like to run another analysis(yes/no)?")
    blob = textblob.TextBlob(analysis)
    analysis = blob.correct()
    analysis = analysis.lower()
