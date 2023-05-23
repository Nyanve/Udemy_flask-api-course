from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt

from sqlalchemy.exc import SQLAlchemyError


from db import db
from models import ItemModel
from models import BlocklistModel
from schemas import ItemSchema, ItemUpdateSchema, BlocklistSchema



blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item


@blp.route("/bloklist")
class Blocklist(MethodView):
    @blp.response(200, BlocklistSchema(many=True))
    def get(self):
        return BlocklistModel.query.all()


    # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6dHJ1ZSwiaWF0IjoxNjgzNTU1MTYzLCJqdGkiOiJmNmI2OThhYy1kMTc2LTQ2ZDctOTZiMC02YjAyYmNhMTdlOTUiLCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoxLCJuYmYiOjE2ODM1NTUxNjMsImV4cCI6MTY4MzU1NjA2MywiaXNfYWRtaW4iOnRydWV9.1_hmbVLA4zDjXkjSPQh4GO_LO-qMrE1gFT8EMlh93sI