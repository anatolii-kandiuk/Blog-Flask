from .. import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount_ram = db.Column(db.Integer, nullable=False)
    pc = db.relationship('PersonalComputer', backref='category', lazy=True)


class PersonalComputer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firm = db.Column(db.String(50), nullable=False)
    type_processor = db.Column(db.String(100), nullable=True)
    clock_frequency = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default_comp.jpg')
    category_ram_id = db.Column(db.Integer, db.ForeignKey('category.id') , nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"PersonalComputer('{self.id}', '{self.firm}', '{self.type_processor}', '{self.date_created}')"

#db.create_all()