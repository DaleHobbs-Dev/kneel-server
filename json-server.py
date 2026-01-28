"""Module for JSON server handling Kneel Diamonds API requests"""

import json
from http.server import HTTPServer


# Add your imports below this line
from views import retrieve_order, list_orders


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

        else:
            return self.response(
                "", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND.value
            )


#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    """Starts the server on port 8000"""
    host = ""
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()


if __name__ == "__main__":
    main()
