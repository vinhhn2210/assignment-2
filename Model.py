from dataclasses import dataclass
from typing import List
import requests
@dataclass
class Location:
    lat: float
    lng: float
    address: str
    city: str
    country: str

@dataclass
class Amenities:
    general: List[str]
    room: List[str]

@dataclass
class Image:
    link: str
    description: str

@dataclass
class Images:
    rooms: List[Image]
    site: List[Image]
    amenities: List[Image]

@dataclass
class Hotel:
    id: str
    destination_id: int
    name: str
    description: str
    location: Location
    amenities: Amenities
    images: Images
    booking_conditions: List[str]


class BaseSupplier:
    
    supplier_name: str
    
    def endpoint():
        """URL to fetch supplier data"""
        
    def fetch(self):
        url = self.endpoint()
        resp = requests.get(url)
        return [dto for dto in resp.json()]

class Acme(BaseSupplier):
    
    supplier_name = 'acme'
    
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'

class Patagonia(BaseSupplier):
    
    supplier_name = 'patagonia'
    
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/patagonia'
        
class Paperflies(BaseSupplier):
    
    supplier_name = 'paperflies'
    
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/paperflies'


class AnotherSupplier(BaseSupplier):
    
    supplier_name = 'another'
    
    @staticmethod
    def endpoint():
        return 'https://5f2be0b4ffc88500167b85a0.mockapi.io/suppliers/acme'
