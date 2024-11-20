import json
import os
from Adapter import *
from utils import *

class PatternGenerator:
    def __init__(self):
        self.adapter = Adapter("rules")
    
    def getPattern(self, key):
        components = key.split('.')
        for i, component in enumerate(components):
            if isItemList(component):
                components[i] = '#id'
        what_pattern = '.'.join(components)
        return what_pattern
    
    def generate(self, raw_data: dict) -> dict:
        flatten_data = self.adapter.flattenData(FlattenParams(raw_data))
        pattern_list = {}
        for key in flatten_data:
            pattern = self.getPattern(normalizeKey(key))
            pattern_list[pattern] = "*"
        return pattern_list
    
    def generateSuppliersPattern(self, supplier_name, raw_data) -> dict:
        # write to rules/supplier_name.json
        patterns = self.generate(raw_data)
        with open(f"pattern/{supplier_name}.json", "w") as f:
            json.dump(patterns, f, indent=4)
        return patterns
    
    def patternToRule(self, source_name, target_name):
        with open(f"pattern/{source_name}.json", "r") as f:
            source = json.load(f)
        with open(f"pattern/{target_name}.json", "r") as f:
            target = json.load(f)
        rules = {}
        
        
        # can use LLM to generate rules here
        
        with open(f"rules/{source_name}-{target_name}.json", "w") as f:
            json.dump(rules, f, indent=4)
        return rules
    
if __name__ == "__main__":
    path = "sample_data"
    generator = PatternGenerator()
    for file in os.listdir(path):
        if file.endswith('.json'):
            with open(f'{path}/{file}', 'r') as f:
                data = json.load(f)
                generator.generateSuppliersPattern(file[0:-5], data)
