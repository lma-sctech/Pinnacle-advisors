from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def api_root(request):
    """
    API Root endpoint - Provides information about available endpoints
    """
    return Response({
        'message': 'Bienvenue sur l\'API du cabinet de conseil en supply chain',
        'version': '1.0',
        'endpoints': {
            'api': '/api/',
            'admin': '/admin/',
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint - Verifies the API is running
    """
    return Response({
        'status': 'healthy',
        'message': 'L\'API fonctionne correctement'
    }, status=status.HTTP_200_OK)
