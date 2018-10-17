from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, CruiseLine, Ship, Port, Cruise, Day

app = Flask(__name__)

engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def cruise_by_price_pre_day():
    cruises = session.query(Cruise).order_by(Cruise.price / Cruise.nights)
    return render_template('cruise.html', cruises=cruises)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)