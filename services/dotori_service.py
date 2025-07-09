from models.dotori import UserDotori
from flask import current_app
from db import db
class DotoriService:
    @staticmethod
    def get_user_dotori(user_id: int):
        user_dotori = UserDotori.query.filter_by(id=user_id).first()
        if user_dotori:
            return user_dotori.dotori_count
        return None

    @staticmethod
    def initialize_user_dotori(user_id: int):
        user_dotori = UserDotori.query.filter_by(id=user_id).first()
        if not user_dotori:
            user_dotori = UserDotori(id=user_id, dotori_count=1000000)
            print(f"초기화 완료, {user_id}님의 도토리: {user_dotori.dotori_count}")
            db.session.add(user_dotori)
            db.session.commit()
        return user_dotori.dotori_count

    @staticmethod
    def buy_product(user_id: int, product_price: int):
        user_dotori = UserDotori.query.filter_by(id=user_id).first()
        if not user_dotori:
            return False
        
        if user_dotori.dotori_count < product_price:
            return False
        print(f"구매 완료, {user_id}님의 도토리: {user_dotori.dotori_count} -> {user_dotori.dotori_count - product_price}")
        user_dotori.decrement(product_price)
        db.session.commit()
        return True

    @staticmethod
    def add_dotori(user_id: int, amount: int):
        user_dotori = UserDotori.query.filter_by(id=user_id).first()
        if not user_dotori:
            user_dotori = UserDotori(id=user_id)
            db.session.add(user_dotori)
        print(f"도토리 추가, {user_id}님의 도토리: {user_dotori.dotori_count} -> {user_dotori.dotori_count + amount}")
        user_dotori.increment(amount)
        db.session.commit()
        return user_dotori.dotori_count

    @staticmethod
    def get_all_users_dotori() -> list:
        users = UserDotori.query.all()
        return [user.to_response() for user in users]
