

class Bulk:
    def __init__(self):
        self._data = {}


    def get_bulk(self):
        return self._data

    def get_bulk_Key(self, key):
        try:
            return self._data[key]
        except Exception as exc:
            print(f"WARNING: problems getting kay value on bulk object: {exc}")
            return None

    def set_bulk_Key(self, key,  value):
        try:
            self._data[key] = value
            return True
        except Exception as exc:
            print(f"WARNING: problems  setting kay value on bulk object: {exc}")
            return False

    def del_bulk_Key(self, key):
        try:
            del self._data[key]
            return True
        except Exception as exc:
            print(f"WARNING: problems deleting kay value on bulk object: {exc}")
            return False

if __name__ == "__main__":
    pass