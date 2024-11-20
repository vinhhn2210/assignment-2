# process string data

def normalizeKey(s: str) -> str:
    s = s.lower().strip()
    s = " ".join(s.split())
    return s

def normalizeString(s: str) -> str:
    s = s.strip()
    s = " ".join(s.split())
    return s

def isItemList(component: str) -> bool:
    return component.startswith('#') and component[1:].isdigit()
