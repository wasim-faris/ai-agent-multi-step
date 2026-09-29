import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import run_product_search


class ProductSearchView(APIView):
    """Handle POST /api/products/search/ requests."""

    def post(self, request):
        message = request.data.get("message", "")
        if not isinstance(message, str) or not message.strip():
            return Response(
                {"error": "Please enter what you are looking for."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = run_product_search(message.strip())
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        except (requests.RequestException, RuntimeError, KeyError, ValueError) as error:
            print(f"Product search failed: {error}")
            return Response(
                {"error": "The AI search is unavailable right now. Please try again."},
                status=status.HTTP_502_BAD_GATEWAY,
            )