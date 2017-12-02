class Config(object):
    """Base config class."""
    pass


class ProdConfig(Config):
    """Production config class."""
    pass


class DevConfig(Config):
    """Development config class."""
    # Open the DEBUG
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/lgtalk?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///../nowstagram.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
