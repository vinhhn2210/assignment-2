import json
import argparse
from Model import *
from HotelService import HotelSerivce

def fetch_hotels(hotel_ids, destination_ids):
    suppliers = [
        Acme(),
        Paperflies(),
        Patagonia(),
        # AnotherSupplier()
    ]

    svc = HotelSerivce()

    for supplier in suppliers:
        for dto in supplier.fetch():
            svc.addNewHotel(supplier.supplier_name, dto)
    
    # Process the merged data
    svc.processMergeData()

    # Fetch filtered data
    filtered = svc.find(hotel_ids, destination_ids)
    return filtered
    
def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("hotel_ids", type=str, help="Hotel IDs")
    parser.add_argument("destination_ids", type=str, help="Destination IDs")
    
    # Parse the arguments
    args = parser.parse_args()
    
    hotel_ids = args.hotel_ids
    destination_ids = args.destination_ids
    
    if hotel_ids == "None":
        hotel_ids = None
    else:
        hotel_ids = hotel_ids.split(',')
        # unique
        hotel_ids = list(set(hotel_ids))
        
    if destination_ids == "None":
        destination_ids = None
    else:
        destination_ids = destination_ids.split(',')
        destination_ids = list(map(int, destination_ids))
    
    result = fetch_hotels(hotel_ids, destination_ids)
    print(result)
    
if __name__ == "__main__":
    main()
