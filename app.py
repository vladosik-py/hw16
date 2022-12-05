import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import data

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_homework.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)

    def to_dict(self):
        """возвращает словарь с данными пользователя"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        """возвращает словарь с данными заказа"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        """возвращает словарь с данными предложения"""
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


@app.route("/users", methods=["GET", "POST"])
def users():
    """получает всех пользователей; создает пользователя"""
    if request.method == "GET":
        result = []
        for user in User.query.all():
            result.append(user.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

        return 'User Created', 201


@app.route("/users/<int:uid>", methods=["GET", "PUT", "DELETE"])
def user(uid: int):
    """получает пользователя по его id,
    обновляет и удаляет данные пользователя"""
    if request.method == "GET":
        return json.dumps(User.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        user_data = json.loads(request.data)
        user = User.query.get(uid)
        user.first_name = user_data["first_name"]
        user.last_name = user_data["last_name"]
        user.age = user_data["age"]
        user.email = user_data["email"]
        user.role = user_data["role"]
        user.phone = user_data["phone"]

        db.session.add(user)
        db.session.commit()

        return 'User Updated', 204

    if request.method == "DELETE":
        user = User.query.get(uid)

        db.session.delete(user)
        db.session.commit()

        return 'User Deleted', 204


@app.route("/orders", methods=["GET", "POST"])
def orders():
    """получает все заказы"""
    if request.method == "GET":
        result = []
        for user in Order.query.all():
            result.append(user.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        order_data = json.loads(request.data)
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

        return "Order Created", 201


@app.route("/orders/int:uid>", methods=["GET", "PUT", "DELETE"])
def order(uid: int):
    """получает заказ по его id,
    обновляет и удаляет данные о заказе"""
    if request.method == "GET":
        return json.dumps(Order.query.get(uid).to_dict()), 200

    if request.method == "PUT":
        order_data = json.loads(request.data)
        user = Order.query.get(uid)
        user.name = order_data["name"]
        user.description = order_data["description"]
        user.start_date = order_data["start_date"]
        user.end_date = order_data["end_date"]
        user.address = order_data["address"]
        user.price = order_data["price"]
        user.customer_id = order_data["customer_id"]
        user.executor_id = order_data["executor_id"]

        db.session.add(user)
        db.session.commit()

        return 'Order Updated', 204

    if request.method == "DELETE":
        user = Order.query.get(uid)

        db.session.delete(user)
        db.session.commit()

        return 'Order Deleted', 204


@app.route("/offers", methods=["GET", "POST"])
def offers():
    """получает все предложения"""
    if request.method == "GET":
        result = []
        for user in Offer.query.all():
            result.append(user.to_dict())

        return json.dumps(result), 200

    if request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()

        return 'Offer Created', 201


@app.route("/offers/<int:uid>", methods=["GET", "PUT", "DELETE"])
def offer(uid: int):
    """получает предложение по его id,
    обновляет и удаляет данные о предложении"""
    if request.method == "GET":
        return json.dumps(Offer.query.get(uid).to_dict()), 201

    if request.method == "PUT":
        offer_data = json.loads(request.data)
        user = Offer.query.get(uid)
        user.order_id = offer_data["order_id"]
        user.executor_id = offer_data["executor_id"]

        db.session.add(user)
        db.session.commit()

        return 'Offer Updated', 204

    if request.method == "DELETE":
        user = Offer.query.get(uid)

        db.session.delete(user)
        db.session.commit()

        return 'Offer Deleted', 204


def init_database():
    """создает базу данных и добавляет в нее данные
    о пользователе, заказе и предложении"""
    db.drop_all()
    db.create_all()

    for user_data in data.Users:
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )

        db.session.add(new_user)
        db.session.commit()

    for order_data in data.Orders:
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"],
        )

        db.session.add(new_order)
        db.session.commit()

    for offer_data in data.Offers:
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"],
        )

        db.session.add(new_offer)
        db.session.commit()


if __name__ == '__main__':
    init_database()
    app.run(debug=True)