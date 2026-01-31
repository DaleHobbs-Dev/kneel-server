"""Module for JSON server handling Kneel Diamonds API requests"""

import json
from http.server import HTTPServer


# Add your imports below this line
from views import (
    retrieve_order,
    list_orders,
    create_order,
    delete_order,
    update_order,
    update_metal,
    list_metals,
    retrieve_metal,
)


from nss_handler import HandleRequests, status


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for Kneel Diamonds"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "orders":
            if url["pk"] != 0:
                response_body = retrieve_order(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_orders(url)
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        if url["requested_resource"] == "metals":
            if url["pk"] != 0:
                response_body = retrieve_metal(url)
                return self.response(response_body, status.HTTP_200_SUCCESS.value)

            response_body = list_metals()
            return self.response(response_body, status.HTTP_200_SUCCESS.value)

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_POST(self):
        """Handle POST requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        # Get content length to read the body
        content_length = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_length)
        # Parse the JSON body to a Python dictionary
        post_body = json.loads(post_body)

        if url["requested_resource"] == "orders":
            # Here you would handle creating a new order
            response_body = create_order(post_body)
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "metals":
            # Here you would handle creating a new metal
            response_body = json.dumps({"message": "Metal created", "metal": post_body})
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "customers":
            # Here you would handle creating a new customer
            response_body = json.dumps(
                {"message": "Customer created", "customer": post_body}
            )
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "sizes":
            # Here you would handle creating a new size
            response_body = json.dumps({"message": "Size created", "size": post_body})
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        elif url["requested_resource"] == "styles":
            # Here you would handle creating a new style
            response_body = json.dumps({"message": "Style created", "style": post_body})
            return self.response(response_body, status.HTTP_201_SUCCESS_CREATED.value)

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "orders":
            if pk != 0:
                successfully_deleted = delete_order(pk)
                if successfully_deleted:
                    return self.response(
                        "Successfully deleted",
                        status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value,
                    )
                else:
                    return self.response(
                        "Requested resource not found",
                        status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
                    )

        else:
            return self.response(
                "Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )

    def do_PUT(self):
        """Handle PUT requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        # PUT requries a primary key
        if pk == 0:
            return self.response(
                "ID required for PUT request",
                status.HTTP_400_CLIENT_ERROR_BAD_REQUEST_DATA.value,
            )

        # Get content length to read the body
        content_length = int(self.headers.get("Content-Length", 0))
        put_body = self.rfile.read(content_length)
        # Parse the JSON body to a Python dictionary
        put_body = json.loads(put_body)

        # Route to appropriate update function
        if url["requested_resource"] == "orders":
            successfully_updated = update_order(pk, put_body)
        elif url["requested_resource"] == "metals":
            successfully_updated = update_metal(pk, put_body)
        else:
            return self.response(
                "Resource not found",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )

        # Check if update was successful
        if successfully_updated:
            return self.response(
                "", status.HTTP_204_SUCCESS_NO_RESPONSE_BODY.value  # Empty body for 204
            )
        else:
            return self.response(
                "Resource not found",
                status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value,
            )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    """Starts the server on port 8088"""
    host = ""
    port = 8088
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
