#IBM Hack Challenge 2020
#Project SKIP V1.0
#SPS_PRO_1497

#required library and modules
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self):
        # authenticating
        consumerKey = '4Epntf86LIBHfsxkDeTHT6rvn'
        consumerSecret = 'vzIwGuYwgOx4k8lrCXIcN8JrKBDt3TOHIVrHwhCPInuu0yw6p8'
        accessToken = '983721813422190592-RY6Fq2M6sBy1ZBtdk8ABityuiCzdjuj'
        accessTokenSecret = 'Ct6HGgjViMluBbumwMJ9CjftDRs6QfiBoky8XcKX9rX9w'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        searchTerm = "COVID19"
        NoOfTerms = 100

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en", ).items(NoOfTerms)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0
        report=""

        # iterating through tweets fetched
        for tweet in self.tweets:
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        wpositive = self.percentage(wpositive, NoOfTerms)
        spositive = self.percentage(spositive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        wnegative = self.percentage(wnegative, NoOfTerms)
        snegative = self.percentage(snegative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)

        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("The opinion of people regarding " + searchTerm + " is shown by analyzing " + str(NoOfTerms) + " tweets at a time.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
            report="Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
            report="Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
            report="Positive"
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
            report="Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
            report="Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
            report="Negative"
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")
            report="Strongly Negative"

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, NoOfTerms,report)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfSearchTerms,report):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('The opinion of people on ' + searchTerm + ' by analyzing their Tweets' '\n General report ='+report)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
 
if __name__== "__main__":  
    sa = SentimentAnalysis()
    sa.DownloadData()
