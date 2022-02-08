import requests
import json
import matplotlib.pyplot as plt
import textblob
import nltk
!pip install syllables
import syllables
nltk.download("punkt")
nltk.download('averaged_perceptron_tagger')
#This program will perform an analysis based on the user's choice of customer service tweets from popular companies. Then, it will print the result along with a bar graph.
companies = ["@amazonhelp", "@applesupport", "@ask_spectrum",
"@askplaystation", "@comcastcares", "@hulu_support",
"@spotifycares", "@sprintcare", "@tmobilehelp", "@uber_support",
"@upshelp", "@xboxsupport"]
print("Welcome to the customer service linguistics analyzer!")
analysis = "yes"
#Loop to ask if user wants to run another analysis
while analysis == "yes":
  response = requests.get("https://dgoldberg.sdsu.edu/515/customer_service_tweets_full.json")
  if response:
    data = json.loads(response.text)
    #Asking for user input
    option = input("Which analysis would you like to perform(polarity/subjectivity/readability/formality)?")
    option = option.lower()
    values = []
    if option == "polarity" or option == "subjectivity" or option == "readability" or option == "formality":
      for company in companies:
        polarity = 0
        subjectivity = 0
        readability = 0
        formality = 0
        count = 0
        for item in data:
          if item["Company"].lower() == company:
            count = count + 1
            text = item["Text"]
            blob = textblob.TextBlob(text)
            #Sentiment analysis
            polarity = polarity + blob.polarity
            subjectivity = subjectivity + blob.subjectivity
            #Readability formula
            readability = readability + (0.39 * (len(blob.words)/len(blob.sentences)) + 11.8 * (syllables.estimate(text)/len(blob.words)) - 15.59)
            tags = blob.tags
            f = 0
            c = 0
            #Checking for tags
            for tag in tags:
              if "NN" in tag[1] or "JJ" in tag[1] or "IN" in tag[1] or "DT" in tag[1]:
                f = f + 1
              elif "PR" in tag[1] or "VB" in tag[1] or "RB" in tag[1] or "UH" in tag[1]:
                c = c + 1
            formality = formality + (50 * ((f - c)/(f + c) + 1))
        #Getting the final numbers
        polarity = polarity / count
        subjectivity = subjectivity / count
        readability = readability / count
        formality = formality / count
        #Prints out result
        if option == "polarity":
          print(company,":", polarity)
          values.append(polarity)
        elif option == "subjectivity":
          print(company,":", subjectivity)
          values.append(subjectivity)
        elif option == "readability":
          print(company,":", readability)
          values.append(readability)
        elif option == "formality":
          print(company,":", formality)
          values.append(formality)
      #Prints out bar graphs
      if option == "polarity":
        plt.title("Polarities by Twitter handle")
        plt.xlabel("Twitter handle")
        plt.ylabel("Polarity")
        plt.xticks(rotation = 45, ha = "right")
        plt.bar(companies, values)
        plt.show()
      elif option == "subjectivity":
        plt.title("Subjectivity by Twitter handle")
        plt.xlabel("Twitter handle")
        plt.ylabel("Subjectivity")
        plt.xticks(rotation = 45, ha = "right")
        plt.bar(companies, values)
        plt.show()
      elif option == "readability":
        plt.title("Flesch-Kincaid Grade Levels by Twitter handle")
        plt.xlabel("Twitter handle")
        plt.ylabel("Flesch-Kincaid Grade Level")
        plt.xticks(rotation = 45, ha = "right")
        plt.bar(companies, values)
        plt.show()
      elif option == "formality":
        plt.title("Formality Index by Twitter handle")
        plt.xlabel("Twitter handle")
        plt.ylabel("Formality Index")
        plt.xticks(rotation = 45, ha = "right")
        plt.bar(companies, values)
        plt.show()
    else:
      print("Sorry, that type of analysis is not supported. Please try again.")
  else:
    print("Sorry, connection error.")
  #Ask user if they want to run another analysis
  analysis = input("Would you like to run another analysis(yes/no)?")
  analysis = analysis.lower()
