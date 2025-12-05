"""
Servicio para interactuar con NewsAPI.org
"""
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class NewsAPIService:
    """Servicio para obtener noticias de NewsAPI"""
    
    def __init__(self):
        self.api_key = settings.NEWSAPI_KEY
        self.base_url = settings.NEWSAPI_ENDPOINT
    
    def get_top_headlines(self, query=None, category=None, country=None, page_size=20):
        """
        Obtiene los titulares principales
        
        Args:
            query: Palabra clave para buscar
            category: Categoría de noticias (business, entertainment, general, health, science, sports, technology)
            country: Código del país (e.g., 'us', 'gb', 'cl')
            page_size: Número de noticias a retornar (máx 100)
        
        Returns:
            dict: Respuesta de la API con las noticias
        """
        try:
            params = {
                'apiKey': self.api_key,
                'pageSize': min(page_size, 100),
            }
            
            if query:
                params['q'] = query
            if category:
                params['category'] = category
            if country:
                params['country'] = country
            
            url = f"{self.base_url}/top-headlines"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener titulares de NewsAPI: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error al conectar con NewsAPI: {str(e)}',
                'articles': []
            }
    
    def search_everything(self, query, sort_by='publishedAt', page_size=20, from_date=None, to_date=None):
        """
        Busca noticias en todos los artículos (no solo titulares)
        
        Args:
            query: Palabra clave para buscar (requerida)
            sort_by: Ordenar por ('relevancy', 'popularity', 'publishedAt')
            page_size: Número de noticias a retornar
            from_date: Fecha inicial (formato: YYYY-MM-DD)
            to_date: Fecha final (formato: YYYY-MM-DD)
        
        Returns:
            dict: Respuesta de la API con las noticias
        """
        try:
            params = {
                'apiKey': self.api_key,
                'q': query,
                'sortBy': sort_by,
                'pageSize': min(page_size, 100),
                'language': 'es',  # Noticias en español
            }
            
            if from_date:
                params['from'] = from_date
            if to_date:
                params['to'] = to_date
            
            url = f"{self.base_url}/everything"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al buscar en NewsAPI: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error al conectar con NewsAPI: {str(e)}',
                'articles': []
            }
    
    def get_water_news(self, page_size=20):
        """
        Obtiene noticias relacionadas con agua y servicios de agua
        """
        return self.search_everything(
            query='agua agua potable servicios agua crisis hídrica',
            page_size=page_size
        )
