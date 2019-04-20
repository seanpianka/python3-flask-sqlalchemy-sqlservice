from flask import Flask
from sqlalchemy import Column, ForeignKey, orm
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, BOOLEAN, TEXT
import sqlservice


app = Flask(__name__)
app.config.from_object("config")


def as_dict(self, *exclude):
    if not exclude:
        exclude = []

    exclude = [".".join([self.__tablename__, c]) for c in exclude]

    return {
        c.name: getattr(self, c.name)
        for c in self.__table__.columns
        if str(c) not in exclude
    }


BaseModel = sqlservice.declarative_base()
BaseModel.as_dict = as_dict


class Advisor(BaseModel):
    __tablename__ = "Advisor"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False)
    is_undergraduate = Column(BOOLEAN, nullable=False)


db = sqlservice.SQLClient(
    {"SQL_DATABASE_URI": app.config["SQLALCHEMY_DATABASE_URI"]}, model_class=BaseModel
)


@app.route("/")
def index():
    advisors = [a.as_dict() for a in db.query(Advisor).all()]
    return f"<html><body>{advisors}</body></html>"
