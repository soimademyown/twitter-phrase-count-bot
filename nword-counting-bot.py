import tweepy, os, pprint, time
from dotenv import load_dotenv


# id and username for @nwordcounting
bot_user_id = 1937985416650473472
bot_username = "nwordcounting"

# returns Twitter API v2 Client for @nwordcounting
def get_client():

    load_dotenv()
    try:
        client = tweepy.Client(
            bearer_token=os.getenv("BEARER_TOKEN"),
            consumer_key=os.getenv("CONSUMER_KEY"),
            consumer_secret=os.getenv("CONSUMER_SECRET"),
            access_token=os.getenv("ACCESS_TOKEN"),
            access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
            wait_on_rate_limit=True
        )
        return client

    except Exception as e:
        print(f"Failed to initialize client: {e}")
        return None
client = get_client()

# retrieves info of user 
def get_user_info(client, user):

    response = client.get_user(id=user)
    return [response.data.id, response.data.username]

# retrieves the last 5 mentions of @nwordcounting
def last_mention_id(client):

    response = client.get_users_mentions(bot_user_id, max_results=5)
    return response.meta.oldest_id


def phrase_counter(client):

    if not client:
        print("No valid client connection")
        return 

    # Stores the username of the last mention to user variable
    user = get_user_info(client, last_mention_id(client))

    #search parameters for tweet queries
    phrases = {
        "nwords": ["nigga", "hard-r", "nig", "ngga", "negro"],
        "AAVE": ["ts", "sybau"]}
    print(phrases["nwords"][0])

    # searches specified user's tweets for words in phrases dict and returns their usage frequency
    def search_user_tweets(client, user):

        query = f"{phrases["nwords"][0]} from:{user} -is:retweet"
        
        try:
            response = client.search_recent_tweets(query=query, max_results=10)
            pprint(response)

            if not response.data:
                print(f"No tweets found from @{username} with '{keyword}' in the past 7 days")
                return None

        except tweepy.TooManyRequests as t:
            reset = int(t.response.headers['x-rate-limit-reset'])
            wait = reset - time.time()
            print(f"🚨 Jar locked! Wait {wait} secs.")

        except Exception as e:
            print(f"Error: {e}")

    search_user_tweets(client, user)
phrase_counter(client)


        # results = f"In the past 7 days, @{user} has used the nword: {count} times"