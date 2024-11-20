class MergeSelector:
    @staticmethod
    def checkValidValue(value):
        # return false if null, None, empty string, empty list, empty dict
        if value is None:
            return False
        if isinstance(value, str) and not value:
            return False
        if isinstance(value, list) and not value:
            return False
        if isinstance(value, dict) and not value:
            return False
        return True

    @staticmethod
    def similarString(str1: str, str2: str) -> bool:
        # use LCS to temporarily match strings, if match > 0.8, return True
        # if match < 0.8, return False
        # can replace with other string similarity algorithm or LLM

        lcs = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
        for i in range(1, len(str1) + 1):
            for j in range(1, len(str2) + 1):
                if str1[i - 1] == str2[j - 1]:
                    lcs[i][j] = lcs[i - 1][j - 1] + 1
                else:
                    lcs[i][j] = max(lcs[i - 1][j], lcs[i][j - 1])
        return lcs[-1][-1] / max(len(str1), len(str2)) > 0.5

    @staticmethod
    def canCombineValue(source: any, target: any) -> bool:
        if isinstance(source, str) and isinstance(target, str):
            if ".jpg" in source or ".png" in source:
                return source == target
            return MergeSelector.similarString(source, target)
        return False
    @staticmethod
    def canAddValue(source: any, target: any) -> bool:
        if isinstance(source, str) and isinstance(target, str):
            return True
        return False
    
    def addValue(source: str, target: str) -> str:
        if source in target:
            return target
        if target in source:
            return source
        if len(source) > len(target):
            return source + " " + target
        return target + " " + source

    @staticmethod
    def combineValue(source: str, target: str) -> str:
        if len(source) > len(target):
            return source
        return target

    @staticmethod
    def canReplaceValue(target):
        if not MergeSelector.checkValidValue(target):  # simple rule
            return True
        return False

    @staticmethod
    def canCreateNewIndex(source_key: str):
        return ".#" in source_key

    @staticmethod
    def conflict_key(source_key: str, target: dict) -> str:
        return source_key in target

    @staticmethod
    # new index for conflict key
    def getNextIndex(source_key: str, target: dict) -> str:
        components = source_key.split('.')
        for index, component in enumerate(components):
            if component.startswith('#'):
                current_index = int(component[1:])
                while MergeSelector.conflict_key(".".join(components), target):
                    current_index += 1
                    components[index] = f"#{current_index}"
                return ".".join(components)
        return source_key

    @staticmethod 
    # merge two flatten data
    def mergingFlattenData(source: dict, target: dict) -> dict:
        for key, value in source.items():
            if not MergeSelector.checkValidValue(value):
                continue
            if key not in target:
                target[key] = value
            else:  # simple strategy rule
                if MergeSelector.canReplaceValue(target[key]):  # target data error
                    target[key] = value
                elif MergeSelector.canCombineValue(value, target[key]):
                    target[key] = MergeSelector.combineValue(value, target[key])
                elif MergeSelector.canCreateNewIndex(key):
                    new_key = MergeSelector.getNextIndex(key, target)
                    target[new_key] = value
                elif MergeSelector.canAddValue(value, target[key]):
                    target[key] = MergeSelector.addValue(value, target[key])
                else:
                    # skip or do other strategy
                    pass
        return target
