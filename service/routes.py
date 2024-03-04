######################################################################
# Copyright 2016, 2024 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Wishlist Store Service

This service implements a REST API that allows you to Create, Read, Update
and Delete Wishlists from the inventory of wishlists in the WishlistShop
"""

from flask import jsonify, request, url_for, abort
from flask import current_app as app  # Import Flask application
from service.models import Wishlists, Item, DataValidationError
from service.common import status  # HTTP Status Codes


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


# REST API code
@app.route("/items", methods=["POST"])
def create_item():
    """
    Creates an Item

    This endpoint will create a Pet based the data in the body that is posted
    """
    app.logger.info("Request to create a pet")
    check_content_type("application/json")

    items = Item()
    items.deserialize(request.get_json())
    items.create()
    message = items.serialize()
    location_url = url_for("get_item", item_id=items.id, _external=True)

    app.logger.info("Item with ID: %d created.", items.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


@app.route("/wishlists/<int:wishlist_id>", methods=["PUT"])
def update_wishlists(wishlist_id):
    """
    Update a Wishlist

    This endpoint will update a Wishlist based the body that is posted
    """
    app.logger.info("Request to update wishlist with id: %d", wishlist_id)
    check_content_type("application/json")

    wishlist = Wishlists.find(wishlist_id)
    if not wishlist:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id: '{wishlist_id}' was not found.",
        )

    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.update()

    app.logger.info("Wishlist with ID: %d updated.", wishlist.id)
    return jsonify(wishlist.serialize()), status.HTTP_200_OK
