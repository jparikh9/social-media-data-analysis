import os.path

import tweepy
import twitterKeys as tk
import pandas as pd


# function to authenticate user credentials. Returned object is used to get data from twitter apis.
def authenticate():
    auth_var = tweepy.OAuthHandler(tk.ApiKey, tk.ApiKeySecret)
    auth_var.set_access_token(tk.AccessToken, tk.AccessTokenSecret)
    tweepy_api = tweepy.API(auth_var, wait_on_rate_limit=True)
    return tweepy_api


# returns information of specific user
def getUserInfo(tweepy_api):
    info = tweepy_api.get_user(screen_name="ParikhJinit")
    return info


if __name__ == '__main__':
    print('hey twitter')
    api_info = authenticate()
    user_info = getUserInfo(api_info)
    print(user_info)

    #path_edges = 'C:/Users/jinit/PycharmProjects/osna_project_1/edges.csv'
    #path_id_file = 'C:/Users/jinit/PycharmProjects/osna_project_1/'
    user = 1

    # get 'following' (friends) list of user
    following_ids_of_user = api_info.get_friend_ids(user_id=user_info.id)
    # get 'followers' list of user
    follower_ids_of_user = api_info.get_follower_ids(user_id=user_info.id)
    # storing friends (list of nodes) in a file 
    data_frame = pd.DataFrame(following_ids_of_user, columns=['following_user_id'])
    data_frame.index.name = 'index'
    data_frame.to_csv("friends_list.csv")

    df = pd.DataFrame(columns=["source", "target"])

    # forming edges of the user whom he follows and who follows him back
    for friend in following_ids_of_user:
        df.loc[len(df)] = [user_info.id, friend]
    for follower in follower_ids_of_user:
        df.loc[len(df)] = [follower, user_info.id]

    # storing edges in file if not exist
    if os.path.exists("edges.csv"):
        os.remove("edges.csv")
    df.to_csv("edges.csv", index=False)

    # loop for getting following list of each user from user's following list
    for i in following_ids_of_user:
        try:
            if os.path.exists(str(i) + '.csv'):
                continue
            user = i
            # storing every user's following list in a file due to twitter apis rate limit
            following_list = api_info.get_friend_ids(user_id=i)
            df_following_list_of_i = pd.DataFrame(following_list, columns=['following_user_id'])
            df_following_list_of_i.index.name = 'index'
            df_following_list_of_i.to_csv(str(i) + ".csv")
        except tweepy.errors.Unauthorized:
            df_unauthorized = pd.DataFrame()    # omitting if there is any unauthorized user
            df_unauthorized['unauthorized_user'] = [user]
            # df_unauthorized.index.name = 'index'
            if os.path.exists('unauthorized_users.csv'):
                df_unauthorized.to_csv('unauthorized_users.csv', mode='a', index=False, header=False)
            else:
                df_unauthorized.to_csv('unauthorized_users.csv',index=False)
            continue
        except Exception as ex:
            print(ex)

    for i in following_ids_of_user:
        try:
            if os.path.exists(str(i) + '.csv'):     # making edges in this loop from stored files
                nodes = pd.read_csv(str(i) + ".csv")
                following_list = nodes['following_user_id'].tolist()
                user_set = set(following_ids_of_user)
                following_user_set = set(following_list)
                common = user_set.intersection(following_user_set)
                list_common = list(common)
                df_append = pd.DataFrame(columns=["source", "target"])
                for j in list_common:
                    df_append.loc[len(df_append)] = [i, j]
                df_append.to_csv('edges.csv', mode='a', index=False, header=False)
        except:
            continue
    print(len(following_ids_of_user))
    print(following_ids_of_user)
    print(len(follower_ids_of_user))
    print(follower_ids_of_user)
