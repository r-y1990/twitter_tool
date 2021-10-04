from requests_oauthlib import OAuth1Session
from db import Dbmaster
from follower_data import Follower_data
import json
import time
import datetime
from config import get_config

# 基本URL
BASE_URL = 'https://api.twitter.com/1.1/'


class TwitterController:
    '''
    TODO: やることが多い
    ・ファイル名の変更
    ・処理分けを考える
    ・いちおう構成を記載しておく
    ・設定ファイル化

    '''

    def __init__(self):
        self.twitter = OAuth1Session(get_config('CONSUMER_API_KEY'),
                                     get_config('CONSUMER_KEY_SECRET'),
                                     get_config('ACCESS_API_KEY'),
                                     get_config('ACCESS_SECRET_KEY'))

    def __del__(self):
        self.db = None

    def extract_follower(self, user, current_date):
        follower = Follower_data()

        follower.api_id = user['id']
        follower.ins_date = current_date
        follower.api_id_str = user['id_str']
        follower.twitter_id = user['screen_name']
        follower.name = user['name']
        follower.following = user['following']

        return follower

    def fetch_followers(self, next_cursor=None):
        retry_count = 0

        # TwitterAPIを実行する
        url = BASE_URL + 'followers/list.json?count=200'
        if next_cursor is not None:
            url = url + '&cursor=' + str(next_cursor)
        res = self.twitter.get(url)

        # エラーであればリトライ
        # while not res.status_code == 200 or res.status_code in (420, 429):
        while not res.status_code == 200 and 10 <= retry_count:
            # v1のエラーコードを受信する場合はリトライ
            if res.status_code in (420, 429):
                retry_count += 1
            else:
                # TwitterAPIのエラーでない場合は異常としてNoneを返却
                print('arere')
                return None
            time.sleep(30)

            res = self.twitter.get(url)

        return res

    def execute(self):
        info = []
        next_cursor = None
        current_date = datetime.datetime.now()

        while True:
            # API実施
            res = self.fetch_followers(next_cursor=next_cursor)
            print('nextcursor:', next_cursor, res)
            if res is None:
                return -1

            # 取得情報Jsonをロード
            followers = json.loads(res.text)
            for user in followers['users']:
                info.append(self.extract_follower(user, current_date))

            # 次のカーソルが存在しない場合終了
            if followers['next_cursor'] <= 0:
                break

            # 次のカーソルを設定する
            next_cursor = followers['next_cursor']
            # self.params['cursor'] = followers['next_cursor']

        # 取得した情報をDBに登録する
        # self.db.BeginSession()
        db = Dbmaster()
        db.BeginSession()
        print(len(info))
        db.insert_data(info)
        db.commit()

