import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level


async def main():
    api = API()  # or API("path-to.db") – default is `accounts.db`

    # ADD ACCOUNTS (for CLI usage see next readme section)

    # Option 1. Adding account with cookies (more stable)
    # or '{"abc": "12", "ct0": "xyz"}'
    cookies = "ct0=e27d1af268d4d7eea09c5839b8b23f14535d3adc06be587fb5cb355c21045937c43c1baf0962279f26160e0cab2500c667ebed5a7e953b6a1419115f7bbb37ab806fc7dae5760dd38f5d28151000b6ff; auth_token=5d1e240468d6ee285cec4b20e349463229963f61"
    await api.pool.add_account("cs4701_nmt", "nidhimahitimmy", "fake@mail.com", "fake", cookies=cookies)
    # or '{"abc": "12", "ct0": "xyz"}'
    cookies2 = "ct0=33043e650c2d30052745c69ac9e382c5d610168f483c71e0eedf6cb50a13331fa1f7aa1bdb093b468945357355f5acfbb55e4c4482c0be4bdb58ed9159266feb821ec558dfd53832af86f978ee760a5f; auth_token=49df2d71d2620b15dfa3e75d02feb0f7a14e3124"
    await api.pool.add_account("timmy_li45369", "nidhimahitimmy", "fake@mail.com", "fake", cookies=cookies2)

    # Option2. Adding account with login / password (less stable)
    # email login / password required to receive the verification code via IMAP protocol
    # (not all email providers are supported, e.g. ProtonMail)
    # await api.pool.add_account("user1", "pass1", "u1@example.com", "mail_pass1")
    # await api.pool.add_account("user2", "pass2", "u2@example.com", "mail_pass2")
    await api.pool.login_all()  # try to login to receive account cookies

    # API USAGE

    # search (latest tab)
    await gather(api.search("elon musk", limit=20))  # list[Tweet]
    print("elon mulk thing")
    # change search tab (product), can be: Top, Latest (default), Media
    # await gather(api.search("elon musk", limit=20, kv={"product": "Top"}))
    # print("elon musk 2 thing")
    # tweet info
    # tweet_id = 20
    # await api.tweet_details(tweet_id)  # Tweet
    # await gather(api.retweeters(tweet_id, limit=20))  # list[User]

    # Note: this method have small pagination from X side, like 5 tweets per query
    # await gather(api.tweet_replies(tweet_id, limit=20))  # list[Tweet]

    # get user by login
    user_login = "xdevelopers"
    # await api.user_by_login(user_login)  # User

    # user info
    user_id = 2244994945
    # await api.user_by_id(user_id)  # User
    # await gather(api.following(user_id, limit=20))  # list[User]
    # await gather(api.followers(user_id, limit=20))  # list[User]
    # await gather(api.verified_followers(user_id, limit=20))  # list[User]
    # await gather(api.subscriptions(user_id, limit=20))  # list[User]
    # await gather(api.user_tweets(user_id, limit=20))  # list[Tweet]
    # await gather(api.user_tweets_and_replies(user_id, limit=20))  # list[Tweet]
    # await gather(api.user_media(user_id, limit=20))  # list[Tweet]

    # list info
    # await gather(api.list_timeline(list_id=123456789))

    # trends
    # await gather(api.trends("news"))  # list[Trend]
    # print("finished news thing")
    # await gather(api.trends("sport"))  # list[Trend]
    # print("finished sports thing")
    # await gather(api.trends("VGltZWxpbmU6DAC2CwABAAAACHRyZW5kaW5nAAA"))  # list[Trend]

    # NOTE 1: gather is a helper function to receive all data as list, FOR can be used as well:
    # async for tweet in api.search("elon musk"):
    # print(tweet.id, tweet.user.username, tweet.rawContent)  # tweet is `Tweet` object

    # NOTE 2: all methods have `raw` version (returns `httpx.Response` object):
    # async for rep in api.search_raw("elon musk"):
    # print(rep.status_code, rep.json())  # rep is `httpx.Response` object

    # change log level, default info
    set_log_level("DEBUG")

    # Tweet & User model can be converted to regular dict or json, e.g.:
    # doc = await api.user_by_id(user_id)  # User
    # doc.dict()  # -> python dict
    # doc.json()  # -> json string

if __name__ == "__main__":
    asyncio.run(main())
