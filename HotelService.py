from Adapter import Adapter
from MergeSelector import MergeSelector
import json

class HotelSerivce:
    def __init__(self):
        self.adapter = Adapter("rules")
        self.merge_selector = MergeSelector()
        self.hotels = {}
        self.merge_flatten = {}
        
    def addNewHotel(self, supplier_name, raw_data: dict):
        adapted_data = self.adapter.adapt(supplier_name, raw_data) 
        hotel_id = adapted_data['id']
        if hotel_id not in self.merge_flatten:
            self.merge_flatten[hotel_id] = {}
        self.merge_flatten[hotel_id] = self.merge_selector.mergingFlattenData(adapted_data, self.merge_flatten[hotel_id])
        
    def processMergeData(self):
        for hotel_id, flatten_data in self.merge_flatten.items():
            self.hotels[hotel_id] = self.adapter.restructuring(flatten_data)
        # save to DB.json
        with open("DB.json", "w") as f:
            json.dump(self.hotels, f, indent=4)
            
    def fetchData(self, hotel_id) -> dict:
        return self.hotels[hotel_id]
    
    def hasData(self, hotel_id, dest_ids) -> bool:
        if hotel_id in self.hotels:
            if dest_ids == None or self.hotels[hotel_id]['destination_id'] in dest_ids:
                return True
        return False
    
    def find(self, hotel_ids, destination_ids):
        filters = []
        if hotel_ids == None:
            if destination_ids == None: # fetch all
                for hotel_id, data in self.hotels.items():
                    filters.append(data)
            return filters
        else:
            for hotel_id in hotel_ids:
                if self.hasData(hotel_id, destination_ids):
                    filters.append(self.fetchData(hotel_id))
        return filters
    