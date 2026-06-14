import os
class Config:
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
         "mysql+mysqlconnector://root:9848%40Mysql@localhost:3306/lmsdb",
    )
    SECRET_KEY=os.environ.get("secret_key", "dev-key")