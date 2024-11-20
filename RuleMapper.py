import os
import json

class RuleMapper:
    def __init__(self, path: str):
        self.path = path
        # read all json files in the path
        self.rules = {}
        for file in os.listdir(path):
            if file.endswith('.json'):
                with open(f'{path}/{file}', 'r') as f:
                    self.rules[file[0:-5]] = json.load(f)
    
    def getRule(self, supplier_name: str, key: str) -> str:
        components = key.split('.')
        for i, component in enumerate(components):
            if self.isItemList(component):
                components[i] = '#id'
        what_rule = '.'.join(components)
        if what_rule not in self.rules[supplier_name]:
            return None
        return self.rules[supplier_name][what_rule]
    
    def applyRule(self, rule: str, items_list: list) -> str:
        mapping_components = rule.split('.')
        for i, component in enumerate(mapping_components):
            if component == '#id':
                mapping_components[i] = items_list.pop(0)
        return '.'.join(mapping_components)
    
    def mapping(self, supplier_name: str, key: str) -> str:
        if supplier_name not in self.rules:
            supplier_name = 'default'
        items_list = self.getItemsList(key)
        rule = self.getRule(supplier_name, key)
        if rule is None:
            return key
        return self.applyRule(rule, items_list)
    
    
    def isItemList(self, component: str) -> bool:
        return component.startswith('#') and component[1:].isdigit()
    
    def getItemsList(self, key: str) -> list:
        components = key.split('.')
        items_list = []
        for i, component in enumerate(components):
            if self.isItemList(component):
                items_list.append(component)
        return items_list
