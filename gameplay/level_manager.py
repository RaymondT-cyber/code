
from typing import Dict, Any
from .validators import BaseValidator, Week1Validator, Week2Validator, Week3Validator, Week4Validator, Competition1Validator, Competition2Validator


class LevelManager:
    def __init__(self):
        # simple registry mapping level id to validator and metadata
        self.levels: Dict[str, Dict[str, Any]] = {}
        self.register('week1', {'title': 'Week 1 - Lists', 'validator': Week1Validator(), 'competition': False})
        self.register('week2', {'title': 'Week 2 - More Lists', 'validator': Week2Validator(), 'competition': False})
        self.register('week3', {'title': 'Week 3 - Loops', 'validator': Week3Validator(), 'competition': False})
        self.register('week4', {'title': 'Week 4 - Functions', 'validator': Week4Validator(), 'competition': False})
        self.register('competition1', {'title': 'First Competition', 'validator': Competition1Validator(), 'competition': True})
        self.register('competition2', {'title': 'Midseason Competition', 'validator': Competition2Validator(), 'competition': True})

    def register(self, id, meta):
        self.levels[id] = meta

    def get_level(self, id):
        return self.levels.get(id)

    def validate(self, id, code_globals):
        meta = self.get_level(id)
        if not meta:
            return False, 'Unknown level'
        validator: BaseValidator = meta.get('validator')
        if not validator:
            return False, 'No validator'
        return validator.validate(code_globals)
