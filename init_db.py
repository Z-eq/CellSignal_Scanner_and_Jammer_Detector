from app import db, app
from models import WifiData, JammingEvent  # Import JammingEvent


def create_tables():
    with app.app_context():
        db.create_all()

        # You can optionally add some initial data here
        wifi1 = WifiData(ssid='WiFi1', address='Address1', rssi='-80')
        wifi2 = WifiData(ssid='33333', address='3', rssi='-70')
        db.session.add(wifi1)
        db.session.add(wifi2)
        db.session.commit()

if __name__ == "__main__":
    create_tables()
