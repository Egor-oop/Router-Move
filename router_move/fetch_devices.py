from app import app, Device


def fetch_devices(device_type: str) -> list:
    with app.app_context():
        return Device.query.filter_by(device_type=device_type).all()
