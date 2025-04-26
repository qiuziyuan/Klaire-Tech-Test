import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Address
from .serializers import AddressSerializer

class AddressCreateView(APIView):
    """
    Crée une adresse basée sur une requête utilisateur.

    - **q**: Chaîne de recherche pour trouver l'adresse via l'API BAN.

    Retourne l'objet adresse enregistré en base de données, ou l'adresse existante si elle est déjà présente.
    """
    def post(self, request):
        q = request.data.get('q', '').strip()
        if not q:
            return Response({"error": "Le champ 'q' est requis et doit être une chaîne non vide."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={q}&limit=1", timeout=5)
            if response.status_code != 200:
                raise Exception("API request failed")
            data = response.json()
        except Exception:
            return Response({"error": "Erreur serveur : impossible de contacter l'API externe."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not data['features']:
            return Response({"error": "Adresse non trouvée. Aucun résultat ne correspond à votre recherche."}, status=status.HTTP_404_NOT_FOUND)

        properties = data['features'][0]['properties']
        geometry = data['features'][0]['geometry']['coordinates']
        longitude = geometry[0]
        latitude = geometry[1]

        existing = Address.objects.filter(latitude=latitude, longitude=longitude).first()

        if existing:
            serializer = AddressSerializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)

        address = Address.objects.create(
            label=properties.get('label', ''),
            housenumber=properties.get('housenumber'),
            street=properties.get('street'),
            postcode=properties.get('postcode', ''),
            citycode=properties.get('citycode', ''),
            latitude=latitude,
            longitude=longitude,
        )
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddressRiskView(APIView):
    """
    Récupère les risques géographiques associés à une adresse.

    - **id**: L'identifiant de l'adresse enregistrée en base.

    Retourne un objet JSON contenant les risques retournés par l'API Géorisques.
    """
    def get(self, request, id):
        try:
            address = Address.objects.get(id=id)
        except Address.DoesNotExist:
            return Response({"error": "Adresse non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        try:
            response = requests.get(
                f"https://georisques.gouv.fr/api/v1/resultats_rapport_risque?latlon={address.longitude},{address.latitude}",
                timeout=20
            )
            if response.status_code != 200:
                raise Exception("API request failed")
            data = response.json()
        except Exception:
            return Response({"error": "Erreur serveur : échec de la récupération des données de Géorisques."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data, status=status.HTTP_200_OK)