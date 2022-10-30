
from bson import json_util
import json

from app.utils.misc import get_random_from_list


class DocumentReferencer:

    @classmethod
    def count_documents(cls, **query) -> int:
        return cls.objects(**query).count()

    def has_document(self, **query) -> bool:
        return self.count_documents(**query) > 0 

    def get_document(self, as_json=False) -> dict:
        data = self.to_json()

        if not as_json:
            data = json.loads(data)
        
        return data

    @classmethod
    def fetch_all(cls):
        return cls.objects.all()

    @classmethod
    def fetch_random(cls, query={}):
        if not (all_objects := cls.objects(**query)):
            return None

        return get_random_from_list(all_objects)

    def as_dict(self) -> dict:
        return dict(self.to_mongo())

    def jsonify(self) -> json:
        return json_util.dumps(self.as_dict())

    def load_dict_from_json(self) -> dict:
        return json.loads(self.jsonify())