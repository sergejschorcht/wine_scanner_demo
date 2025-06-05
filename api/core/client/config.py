class Config:
    _data = {}

    @classmethod
    def get(cls, key, default=None):
        return cls._data.get(key, default)
