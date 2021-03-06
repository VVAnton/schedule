from settings import logger
from abc import ABCMeta, abstractmethod, abstractproperty, abstractclassmethod
from settings import *


# from marshmallow import Schema, fields, UnmarshalResult
# TODO: Add validate data for create Session
# schema for validate Entity for generate Session
# class DefSchema(Schema):
#     login = fields.String(required=True)
#     id = fields.Integer(required=True)


# base Session
class Session:
    __slots__ = 'id', 'login', 'name', 'sid', 'email', 'phone', 'description', 'flags'

    # load data from dict/object or kwargs
    def __init__(self, data: dict={}, **kwargs):
        # init object
        super().__init__()
        # int
        self.id = None
        # str
        self.login = None
        # str
        self.name = None
        # str
        self.email = None
        # str
        self.phone = None
        # str
        self.description = None
        # int
        self.flags = 0
        # str
        self.sid = None

        # set attrs from data-dict
        if data:
            self.load_dict(data)
        # set attrs by params
        if kwargs:
            self.load_dict(kwargs)

    # load attributes from dict
    def load_dict(self, data: dict):
        for field in data:
            try:
                getattr(self, field)
                self.__setattr__(field, data[field])
            except:
                pass

    def __bool__(self):
        return True if self.sid else False

    @property
    def is_admin(self):
        return True if self.flags == -4 else False

    @property
    def __dict__(self) -> dict:
        return dict(
            id=self.id,
            login=self.login,
            name=self.name,
            sid=self.sid,
            email=self.email,
            phone=self.phone,
            description=self.description,
            flags=self.flags
        )

    def __str__(self):
        return 'Session {}. id={}, login={}, sid={}'.format(id(self), self.id, self.login, self.sid, self.flags)