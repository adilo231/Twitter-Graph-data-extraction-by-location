# Twitter Graph data extraction by location
In this project, the programme will construct a graph extracted form a real data by exploiting the API data-set.

# Twitter data extractor
Extract data from a [Twitter](https://twitter.com) account with Python.

Enter a Twitter username and this program will a graph of Twitter based on the starting user and the locations array.
For each user the following information will be extracted:
- 'id':'2229718597',
- 'name':'', 
- 'screen_name': '', 
- 'followers_count':'', 
- 'friends_count': '',
- 'checked' :0 ,
- 'location' :''

## Getting started
1. Enter your [Twitter API](https://apps.twitter.com) credentials
2. Entre the information of the first user
3. File up the array of locations
4. Launch the main.py file in your terminal
5. Enjoy !

## Prerequisites
:warning: This file runs on python 3.8 and depends on the [Tweepy](http://www.tweepy.org) library

**Install Tweepy**
```
pip install tweepy
````
**Install networkx**
```
pip install networkx
````

**The extracted graph**

The extracted graph will be saved in .gexf which is gephi extension. to visualize the graph, we recommend installing Gephi software. https://gephi.org/
