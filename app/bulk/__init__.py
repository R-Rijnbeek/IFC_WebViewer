from ..decorators import argument_check

class Bulk:
    @argument_check(object)
    def __init__(self):
        self._data = {}

    @argument_check(object)
    def get_bulk(self):
        return self._data

    @argument_check(object,str)
    def get_bulk_Key(self, key):
        from ..shared import LOG
        try:
            return self._data[key]
        except Exception as exc:
            LOG.warning(f"WARNING: problems getting kay value on bulk object: {exc}")
            return None

    @argument_check(object,str,object)
    def set_bulk_Key(self, key,  value):
        from ..shared import LOG
        try:
            self._data[key] = value
            return True
        except Exception as exc:
            LOG.warning(f"WARNING: problems  setting kay value on bulk object: {exc}")
            return False

    @argument_check(object,str)
    def del_bulk_Key(self, key):
        from ..shared import LOG
        try:
            del self._data[key]
            return True
        except Exception as exc:
            LOG.warning(f"WARNING: problems deleting kay value on bulk object: {exc}")
            return False

if __name__ == "__main__":
    pass