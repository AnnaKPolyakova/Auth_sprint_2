from typing import Union

from flask import request

from flask_app.api.v1.utils.defines import DICT
from flask_app.db import db as _db


class ObjCreator:
    def __init__(self, data, model, db_model, db, format_data=DICT):
        self.data: Union[dict, request] = data
        self.model = model
        self.db_model: _db.Model = db_model
        self.format: str = format_data
        self.formats_and_classes = {DICT: self.get_obj_dict}
        self.obj: _db.Model = self._create_obj()
        self.db: _db = db

    def get_obj_dict(self):
        return self.model(**self.obj.to_dict()).dict()

    def _save_obj(self):
        try:
            self.db.session.add(self.obj)
            self.db.session.flush()
            data = self.formats_and_classes[self.format]()
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            return False, error
        return True, data

    def _create_obj(self):
        if type(self.data) == dict:
            return self.db_model(**self.data)
        return self.db_model(**self.data.get_json())

    def save(self):
        return self._save_obj()


def dell_obj(db, objs: list):
    try:
        for obj in objs:
            db.session.delete(obj)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return False, error
    return True, ""


class ObjUpdater:
    def __init__(self, new_data, model, db_model, db, obj, format_data=DICT):
        self.new_data: dict = new_data
        self.model = model
        self.db_model: _db.Model = db_model
        self.format: str = format_data
        self.obj = obj
        self.formats_and_classes = {DICT: self._get_obj_dict}
        self.db: _db = db

    def _get_obj_dict(self):
        return self.model(**self.obj.to_dict()).dict()

    def _save(self):
        try:
            self.db.session.add(self.obj)
            self.db.session.flush()
            data = self.formats_and_classes[self.format]()
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            return False, error
        return True, data

    def _update_obj(self):
        for field, value in self.new_data.items():
            setattr(self.obj, field, value)

    def update(self):
        self._update_obj()
        return self._save()
