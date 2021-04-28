import time
import tweepy
import os
import networkx as nx
import matplotlib.pyplot as plt
import json

consumer_key=[]
consumer_secret=[]
access_key=[]
access_secret=[]

# set the API logins for several applications
consumer_key.append("rk1XoOWV2Q0krplJmZGzcyIxT")
consumer_secret.append("099nyxS6kXnNCjzQ9b6b07s7aKLdiJfUPVQefxlVQ2ZelnGSsp")
access_key.append("963769414163271680-QfZGuBqaumPoBq1jJAQuQEE4pi9gvkY")
access_secret.append("qDMEnozHGWV9AQkFGG4PhJS7dRpBcsoau0nbaj0hbpXZl")


#consumer_key.append("--")
#consumer_secret.append("--")
#access_key.append("---")
#access_secret.append("---")

    
auth = []
for i in range(len(consumer_key)):
    auth.append(tweepy.OAuthHandler(consumer_key[i], consumer_secret[i]))
    auth[i].set_access_token(access_key[i], access_secret[i])


api = tweepy.API(auth[0])

#loading an existante graph
try:
    print("Loading graph ...")
    G = nx.read_gexf("Graph.gexf")
    print("Loading graph finished ...")
except:
    G=nx.DiGraph()


#load a list of locations that you what extract the graph around        
with open("Location.txt", "r") as fp:
    Locations = json.load(fp)
    
print ("Number Of nodes collected so far:", G.number_of_nodes())
print ("Number Of nodes collected so far:", G.number_of_edges())

Nodeslist=[]
# if the graph is empty we need to initiate the graph with the first user
if G.number_of_nodes() ==0:
    
    G.add_nodes_from([('2229718597', {'id':'2229718597',
                                        'name':'', 
                                        'screen_name': '', 
                                        'followers_count':'', 
                                        'friends_count': '',
                                        'checked' :0 ,
                                        'location' :''
                                        }
                              )
                             ]
                            )

Nodeslist = [v for v in G.nodes()]

# set the waiting time
Time=0
Limited_number_of_followers=4000
Limited_number_of_friends=4000
for v in Nodeslist:
 
   try:
   
        print(" node: ",G.nodes[v]['screen_name']," is it checked : ",G.nodes[v]['checked'])
        # check if the node has not been check it and belong to the disired location
        if  G.nodes[v]['checked']==0 and G.nodes[v]['location'] in Locations: 
            print("Collecting data for",G.nodes[v]['screen_name'],v,G.nodes[v]['location'])  
            print("The number of followers of the user are : " + str(G.nodes[v]['followers_count']))
            print("The number of followers of the user are : " + str(G.nodes[v]['friends_count']))
            if G.nodes[v]['followers_count']<Limited_number_of_followers:
                # get the follower the the user v
                followers = []
                for page in tweepy.Cursor(api.followers, screen_name=G.nodes[v]['screen_name'], wait_on_rate_limit=True,count=300).pages():
                    try:
                        followers.extend(page)
                    except tweepy.TweepError as e:
                        print("Going to sleep:", e)
                        time.sleep(60)
                G.nodes[v]['checked']=1
                for user in followers:
                    user.screen_name
                    Time=0                  
                    if str(user.id) not in G:
                        G.add_nodes_from([(str(user.id), {'id':str(user.id),
                                                                'name': user.name, 
                                                                'screen_name': user.screen_name, 
                                                                'followers_count':user.followers_count, 
                                                                'friends_count':user.friends_count,
                                                                'checked' :0 ,
                                                                'location' :user.location
                                                                }
                                                      )
                                                     ]
                                                    )
   
                    G.add_edge(str(user.id),v)
                print ("\t\tNumber Of nodes collected so far followers:", G.number_of_nodes())
                print ("\t\tNumber Of edges collected so far followers:", G.number_of_edges())
            else:
                G.nodes[v]['checked']=2
            if G.nodes[v]['friends_count']<Limited_number_of_friends:
                # collect the list of the user v friends
                Friends = []
                for page in tweepy.Cursor(api.friends, screen_name=G.nodes[v]['screen_name'], wait_on_rate_limit=True,count=200).pages():
                    try:
                        Friends.extend(page)
                    except tweepy.TweepError as e:
                        print("Going to sleep:", e)
                        time.sleep(60)
                for user in Friends:
                    user.screen_name
                    Time=0
                    G.nodes[v]['checked']=1
                    if str(user.id) not in G:
                       
                        G.add_nodes_from([(str(user.id), {'id':str(user.id),
                                                                 'name': user.name, 
                                                                'screen_name': user.screen_name, 
                                                                'followers_count':user.followers_count, 
                                                                'friends_count':user.friends_count,
                                                                'checked' :0 ,  
                                                                'location' :user.location
                                                                }
                                                      )
                                                     ]
                                                    )
                   
                    G.add_edge(v,str(user.id))
                print ("\t\tNumber Of nodes collected so far followers: ", G.number_of_nodes())
                print ("\t\tNumber Of edge collected so far followers: ", G.number_of_edges())
            else:
                G.nodes[v]['checked']=2
            nx.write_gexf(G, "Graph.gexf") 
            print ("\tNumber Of nodes collected so far ", G.number_of_nodes())
            print ("\tNumber Of edges collected so far", G.number_of_edges())
            
         
    
     
   except tweepy.TweepError as ex: 
        if ex.reason == "Not authorized.":
            print("exep ", ex)
            G.nodes[v]['checked']=2
        else:
            os.system('clear')
            print(ex)
            print("waiting time so far : ", Time)
            Time+=1
            print ("Number Of nodes collected so far:", G.number_of_nodes())
            print ("Number Of edges collected so far:", G.number_of_edges())
            nx.write_gexf(G, "Graph.gexf") 
    
            time.sleep(60)
       
