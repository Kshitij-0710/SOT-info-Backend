from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LinkedInEmbeds

class LinkedInEmbedsAPI(APIView):
    """
    API endpoint that returns LinkedIn embed URLs.
    """
    def get(self, request, format=None):
        try:
            # Get the first (and only) instance or create one if none exists
            embeds, created = LinkedInEmbeds.objects.get_or_create(pk=1)
            
            # Use the model method to extract URLs from the iframe code
            urls = embeds.extract_urls()
            
            return Response({"embed_urls": urls}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )