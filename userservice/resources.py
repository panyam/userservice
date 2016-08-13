
import sys
from datetime import datetime
from flask import request
from flask_restful import Resource
import models
import servicelib

from servicelib import utils as slutils
from servicelib import resources as slresources
from servicelib import decorators as sldecorators
from servicelib.resources import ok_json, error_json

class User(slresources.BaseResource):
    """
    The model class over which this resource provides restful API.
    """
    ResourceModel = models.User

    @classmethod
    def get_routes(cls):
        return ['/users/<string:userid>/',
                '/users/<string:userid>',
                '/users/']

    def do_get(self, userid):
        user = self.ResourceModel.get_by_id(long(userid))
        if not user:
            return error_json("Not Found"), 404
        return user.to_json()

    @sldecorators.ensure_param("fullname")
    def do_create(self, **kwargs):
        """
        Create a new user.
        """
        if not slutils.is_dev_mode():
            return error_json("Not allowed"), 403

        fullname = kwargs["fullname"]
        phone = request.get_json().get("phone", "").strip()
        email = request.get_json().get("email", "").strip()
        if not phone and not email:
            return error_json("Either email or phone number required"), 400

        # TODO: only take in ID if in dev mode
        id = None
        if request.get_json().get("id", 0) > 0:
            id = request.get_json().get("id")
        newuser = self.ResourceModel(fullname=fullname,
                                      phone=phone, 
                                      email=email, 
                                      id = id)
        newuser.put()
        return newuser.to_json()

    def do_put(self, userid):
        """
        Update user data
        """
        user = self.ResourceModel.get_by_id(long(userid))

        fullname = request.get_json().get("fullname", "").strip()
        phone = request.get_json().get("phone", "").strip()

        if fullname:
            user.fullname = fullname
        if phone:
            user.phone = phone
        user.put()
        return user.to_json()

    def do_delete(self, userid):
        """
        Delete a user
        """
        user = self.ResourceModel.get_by_id(long(userid))
        if user:
            user.is_active = False
            user.last_update_at = datetime.now()
            user.put()
            return ok_json("OK"), 200
        else:
            return error_json("User not found"), 404

    def do_action_register(self, **kwargs):
        """
        Register a user.   This only creates a new user but marks the user as inactive until
        verification is done.
        """
        pass

    def do_action_verify(self, **kwargs):
        """
        Verifies a registered user.
        """
        pass

    def do_action_authenticate(self, **kwargs):
        """
        Performs a user authentication.
        """
        pass
