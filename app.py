from pipes import Template
import numpy as np
# import sqlite3
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, Column, String, Integer, Float
from flask import Flask, jsonify, render_template
import pandas as pd

#################################################
# Database Setup
#################################################
username = "postgres"
password = "admin123"
rds_endpoint = "mydb2.cdvcwkjcaojs.us-east-1.rds.amazonaws.com"

# engine = create_engine("sqlite:///players.sqlite")
engine = create_engine(f"postgresql://{username}:{password}@{rds_endpoint}:5432")
# postgresql://scott:tiger@localhost:5432/mydatabase
# reflect an existing database into a new model
# Base = automap_base()
# reflect the tables
# Base.prepare(engine, reflect=True)
from sqlalchemy.orm import registry

# equivalent to Base = declarative_base()

mapper_registry = registry()
Base = mapper_registry.generate_base()

# Save reference to the table
# print(Base.classes.keys())

# player_stats = Base.classes.players

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# def get_db_connection():
#     conn = sqlite3.connect('players.sqlite')
#     conn.row_factory = sqlite3.Row
#     return conn
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///players.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin123@mydb2.cdvcwkjcaojs.us-east-1.rds.amazonaws.com:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class ffplayer(Base):
    __tablename__ = 'players'
    id = Column("_c0",Integer, primary_key=True)
    player = Column("Player", String)
    points2019 = Column("2019 FantasyPoints", String)
    points2020 = Column("2020 FantasyPoints", Float)
    points2021 = Column("2021 FantasyPoints", Float)
    production = Column("Production21", Float)
    atp = Column("Average Total Production", Float)
    team = Column("2021 Tm", String)
    pos = Column("Pos", String)
    avg = Column("AVG", Float)
    pred = Column("Prediction", Float)

#################################################"
# Flask Routes
#################################################

@app.route("/api")
def welcome():
    """List all available api routes."""
    return (
        f'<b>Available Routes:</b><br/>'
        f'# retrieves unique list of player names<br/>'
        f'@app.route("/players/names")<br/>'
        # f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route("/")
def template():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# retrieves unique list of stock ticker names
@app.route("/players/all")
def playerAll():
    session = Session(engine)

    names = session.query(ffplayer.player, ffplayer.points2019, ffplayer.points2020, ffplayer.points2021, ffplayer.production, ffplayer.atp, ffplayer.team, ffplayer.pos, ffplayer.avg, ffplayer.pred).all()
    names_df = pd.DataFrame(names)
    # ffplayer.points2020, ffplayer.points2021, ffplayer.production, ffplayer.atp, ffplayer.team, ffplayer.pos, ffplayer.avg, ffplayer.pred)
    names_df.columns = ["player", "points2019", "points2020", "points2021", "production", "atp", "team", "pos", "avg", "pred"]
    # , "points2021", "production", "atp", "team", "pos", "avg", "pred"]    
    names_dict = names_df.to_dict(orient="records")
    
    session.close()
    return jsonify(names_dict)

@app.route("/players/names")
def playerNames():
    session = Session(engine)

    names = session.query(ffplayer.player, ffplayer.points2019).all()
    names_df = pd.DataFrame(names)
    names_df.columns = ["player", "points2019"]    
    names_dict = names_df.to_dict(orient="records")

    session.close()
    return jsonify(names_dict)

# added this new route for the radius chart
@app.route("/draft")
def draft():
    df = pd.read_csv('Lynne/Resources/Draft.csv')
    return jsonify (df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)

# radius chart with actual rds
 


#scratch
