from twitter_controller import TwitterController
from db import Dbmaster

if __name__ == "__main__":
    tw = TwitterController()
    follower_list = tw.fetch_follower_list()

    # DB登録する
    db = Dbmaster()
    db.BeginSession()
    db.insert_data(follower_list)
    db.commit()
