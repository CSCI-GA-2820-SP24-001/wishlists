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
from service.models import Wishlists, Item
from service.common import status  # HTTP Status Codes


# app = app(__name__)
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


# Create New Item
@app.route("/items", methods=["POST"])
def create_item():
    """
    Creates an Item

    This endpoint will create an Item based the data in the body that is posted
    """
    app.logger.info("Request to create an item")
    check_content_type("application/json")

    items = Item()
    items.deserialize(request.get_json())
    items.create()
    message = items.serialize()
    # Todo: uncomment this code when get_item is implemented
    # location_url = url_for("get_item", item_id=items.id, _external=True)
    location_url = "unknown"
    app.logger.info("Item with ID: %d created.", items.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


# Create wishlist
@app.route("/wishlists", methods=["POST"])
def create_wishlists():
    """
    Creates a Wishlist

    This endpoint will create a Wishlist based the data in the body that is posted
    """
    app.logger.info("Request to create a wishlist")
    check_content_type("application/json")

    wishlist = Wishlists()
    wishlist.deserialize(request.get_json())
    wishlist.create()
    message = wishlist.serialize()
    # Todo: uncomment this code when get_wishlists is implemented
    # location_url = url_for("get_wishlists", wishlist_id=wishlist.id, _external=True)
    location_url = "unknown"

    app.logger.info("Wishlists with ID: %d created.", wishlist.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


# List wishlist
@app.route("/wishlists", methods=["GET"])
def list_wishlists():
    """Returns all of the Wishlists"""
    app.logger.info("Request for wishlist list")

    wishlists = []

    # See if any query filters were passed in
    category = request.args.get("category")
    name = request.args.get("name")
    if category:
        wishlists = Wishlists.find_by_category(category)
    elif name:
        wishlists = Wishlists.find_by_name(name)
    else:
        wishlists = Wishlists.all()

    results = [wishlist.serialize() for wishlist in wishlists]
    app.logger.info("Returning %d wishlists", len(results))
    return jsonify(results), status.HTTP_200_OK


# Update wishlist
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
        app.error(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id: '{wishlist_id}' was not found.",
        )

    wishlist.deserialize(request.get_json())
    wishlist.id = wishlist_id
    wishlist.update()

    app.logger.info("Wishlist with ID: %d updated.", wishlist.id)
    return jsonify(wishlist.serialize()), status.HTTP_200_OK


# Delete wishlist
@app.route("/wishlists/<int:wishlist_id>", methods=["DELETE"])
def delete_wishlists(wishlist_id):
    """
    Delete a Wishlist

    This endpoint will delete a Wishlist based the id specified in the path
    """
    app.logger.info("Request to delete wishlist with id: %d", wishlist_id)

    wishlist = Wishlists.find(wishlist_id)
    if wishlist:
        wishlist.delete()

    app.logger.info("Wishlist with ID: %d delete complete.", wishlist_id)
    return "", status.HTTP_204_NO_CONTENT


@app.route("/items/<int:wishlist_id>/items", methods=["POST"])
def create_items(wishlist_id):
    """
    Create an item on a wishlist

    This endpoint will add an item to a wishlist
    """
    app.logger.info("Request to create an Item for Wishlist with id: %s", wishlist_id)
    check_content_type("application/json")

    # See if the account exists and abort if it doesn't
    wishlist = Wishlists.find(wishlist_id)
    if not wishlist:
        abort(
            status.HTTP_404_NOT_FOUND,
            f"Wishlist with id '{wishlist_id}' could not be found.",
        )

    # Create an address from the json data
    item = Item()
    item.deserialize(request.get_json())

    # Append the address to the account
    wishlist.items.append(item)
    wishlist.update()

    # Prepare a message to return
    message = item.serialize()

    return jsonify(message), status.HTTP_201_CREATED


######################################################################
# READ A WISHLIST
######################################################################
@app.route("/wishlists/<int:wishlist_id>", methods=["GET"])
def get_wishlists(wishlist_id):
    """
    Retrieve a single Wishlists

    This endpoint will return a Wishlists based on it's id
    """
    app.logger.info("Request for wishlist with id: %s", wishlist_id)

    wishlist = Wishlists.find(wishlist_id)
    if not wishlist:
        error(
            status.HTTP_404_NOT_FOUND,
            f"Wishlists with id '{wishlist_id}' was not found.",
        )

    app.logger.info("Returning wishlist: %s", wishlist.name)
    return jsonify(wishlist.serialize()), status.HTTP_200_OK


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    error(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )


def error(status_code, reason):
    """Logs the error and then aborts"""
    app.logger.error(reason)
    abort(status_code, reason)
