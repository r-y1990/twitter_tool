from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Dbmaster():
    def __init__(self):
        self.engine = create_engine(
            'sqlite:///twitter.db', echo=True
        )
        self.session = None

    def getEngine(self):
        """
        エンジン取得
        """
        return self.engine

    def insert_data(self, items):
        """
        INSERT
        """
        try:
            self.session.add_all(items)
        finally:
            # Commitタイミングとか検討
            # SQLAlchemyはセッションとか切る必要なさそう
            pass

    def BeginSession(self):
        self.session = sessionmaker(bind=self.engine)()

    def commit(self):
        self.session.commit()
        self.session.close()
