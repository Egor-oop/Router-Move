from router_move import db


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    user_name = db.Column(db.String(40), nullable=False)
    user_password = db.Column(db.String(50), nullable=False)
    device_type = db.Column(db.String(30), nullable=False)

    def __init__(self, ip, name, user_name, user_password, device_type):
        self.ip = ip
        self.name = name
        self.user_name = user_name
        self.user_password = user_password
        self.device_type = device_type

    def __repr__(self):
        return f'<Device {self.ip}>'


class BackupDirectory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(150), nullable=False)

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'<BackupDirectory {self.path}>'


class BackupFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    path = db.Column(db.String(150), nullable=False)

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'<BackupFile {self.path}>'
