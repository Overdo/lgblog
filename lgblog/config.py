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
    SECRET_KEY = 'hahahah'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    RECAPTCHA_PUBLIC_KEY = "6LezbjsUAAAAAHqK2IXQ-SrVLv9oP8nIiNSwxy54"
    RECAPTCHA_PRIVATE_KEY ="6LezbjsUAAAAAGgK8RVMYfC8wr3GJ53wVpQuPIzp"
