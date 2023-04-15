import pandas as pd
from instagram_private_api import (
    Client, ClientCompatPatch, ClientError)
def get_followers(api, username, count=1000):
    followers = []
    user_id = api.username_info(username)['user']['pk']
    rank_token = Client.generate_uuid()
    next_max_id = None
    num_followers = 0

    while num_followers < count:
        followers_response = api.user_followers(user_id, rank_token=rank_token, max_id=next_max_id, count=min(50, count - num_followers))
        for user in followers_response['users']:
            followers.append({
                'Profile name': user['full_name'],
                'username': user['username']
            })
            num_followers += 1
        if 'next_max_id' not in followers_response or not followers_response['next_max_id']:
            break
        next_max_id = followers_response['next_max_id']
    return followers
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")
api = Client(username, password)
results = []
target_username = input("Enter the Instagram username you want to get followers of: ")
try:
    results = get_followers(api, target_username)
except ClientError as e:
    print(e)
df = pd.DataFrame(results)
df.to_excel(f'{target_username}.xlsx')
print('DataFrame is written to Excel File successfully.')
