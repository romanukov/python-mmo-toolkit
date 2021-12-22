import json
from dataclasses import asdict
from enum import Enum

from backend.common.network.crypto.base import ICrypter


class JSONCrypter(ICrypter):
    
    def encode_dataclass(self, data):
        return json.dumps(asdict(data, dict_factory=self._enum_dataclass_asdict_factory))

    def _enum_dataclass_asdict_factory(self, data):
        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj
    
        return dict((k, convert_value(v)) for k, v in data)
    
    def decode(self, string: str) -> dict:
        return json.loads(string)
