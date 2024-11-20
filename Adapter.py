from dataclasses import dataclass
from RuleMapper import RuleMapper
from utils import *
@dataclass
class FlattenParams:
    data: dict
    prefix: str = ''
    delimiter: str = '.'

class Adapter:
    def __init__(self, rule_path: str):
        self.rule_mapper = RuleMapper(rule_path)
            
    # flatten a dictionary to a simple key-value pair
    def flattenData(self, params: FlattenParams) -> dict:
        result = {}

        data, prefix, delimiter = params.data, params.prefix, params.delimiter

        if isinstance(data, dict):
            for key, value in data.items():
                new_prefix = f"{prefix}{delimiter}{key}" if prefix else key
                result.update(self.flattenData(FlattenParams(value, new_prefix, delimiter)))
        elif isinstance(data, list):
            for index, value in enumerate(data):
                new_prefix = f"{prefix}{delimiter}#{index}"
                result.update(self.flattenData(FlattenParams(value, new_prefix, delimiter)))
        else:
            result[prefix] = data

        return result

    # recover flattened data to original structure
    def restructuring(self, flattened_data: dict) -> dict:
        result = {}

        for key, value in flattened_data.items():
            keys = key.split('.')
            previous = None
            current = result
            pre_component = None
            for component in keys: 
                if isItemList(component):  # Check if it's a list
                    index = int(component[1:])
                    if not isinstance(previous[pre_component], list):
                        previous[pre_component] = [] # If it's not a list, initialize it as a list
                        current = previous[pre_component]
                    previous = current

                    if len(current) <= index:
                        current.append({})
                    
                    current = current[index]  # Move to the new dictionary
                else:
                    # Ensure the dictionary exists
                    previous = current
                    if component not in current:
                        current[component] = {}
                    current = current[component]  # Move to the next level in the dictionary
                pre_component = component
            
            # assign primitive value to the last component            
            if isItemList(keys[-1]):
                index = int(keys[-1][1:])
                previous[index] = value
            else:
                previous[pre_component] = value

        return result
    
    def adapt(self, supplier_name: str, data: dict) -> dict:
        flattened_data = self.flattenData(FlattenParams(data))
        result = {}
        for key, value in flattened_data.items():
            new_key = self.rule_mapper.mapping(supplier_name, normalizeKey(key))
            if isinstance(value, str):
                result[new_key] = normalizeString(value)
            else:
                result[new_key] = value
        return result
