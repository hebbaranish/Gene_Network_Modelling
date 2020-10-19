class StrictDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError("{} is not a legal input for this code. Please check init.txt again.".format(repr(key)))
        dict.__setitem__(self, key, value)
