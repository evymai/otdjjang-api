"""Register user"""

import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token


@csrf_exempt
def login_user(request):
    """Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    """

    body = request.body.decode("utf-8")
    req_body = json.loads(body)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":

        # Use the built-in authenticate method to verify
        name = req_body["username"]
        pass_word = req_body["password"]
        authenticated_user = authenticate(username=name, password=pass_word)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps(
                {"valid": True, "token": token.key, "id": authenticated_user.id}
            )
            return HttpResponse(data, content_type="application/json")

        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type="application/json")

    return HttpResponseNotAllowed(permitted_methods=["POST"])


@csrf_exempt
def register_user(request):
    """Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    """

    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())

    # Validate the request data
    required_fields = ["username", "email", "password", "first_name"]
    for field in required_fields:
        if field not in req_body:
            error_message = {"error": f"Missing required field: {field}"}
            return HttpResponse(
                json.dumps(error_message),
                content_type="application/json",
                status=status.HTTP_400_BAD_REQUEST,
            )

    # Check if the username or email already exists
    if User.objects.filter(username=req_body["username"]).exists():
        return HttpResponse(
            json.dumps({"error": "Username already exists"}),
            content_type="application/json",
            status=status.HTTP_409_CONFLICT,
        )
    if User.objects.filter(email=req_body["email"]).exists():
        return HttpResponse(
            json.dumps({"error": "Email already exists"}),
            content_type="application/json",
            status=status.HTTP_409_CONFLICT,
        )

    # Create a new user by invoking the `create_user` helper method
    new_user = User.objects.create_user(
        username=req_body["username"],
        email=req_body["email"],
        password=req_body["password"],
        first_name=req_body["first_name"],
    )

    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)

    # Return the token and user ID to the client
    data = json.dumps({"token": token.key, "id": new_user.id})
    return HttpResponse(
        data, content_type="application/json", status=status.HTTP_201_CREATED
    )
