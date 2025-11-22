
# Simple validators for levels. Each validator accepts execution namespace (globals) and returns (ok, message)
from typing import Tuple, Any


class BaseValidator:
    def validate(self, ns: dict) -> Tuple[bool, str]:
        raise NotImplementedError()


class Week1Validator(BaseValidator):
    def validate(self, ns: dict):
        # Expect a list named 'brass_section' of length >=3
        val = ns.get('brass_section')
        if isinstance(val, list) and len(val) >= 3:
            return True, 'Good job - found brass_section with at least 3 items'
        return False, 'Please create a list named brass_section with at least 3 items'


class Week2Validator(BaseValidator):
    def validate(self, ns: dict):
        # Expect a list named 'woodwind_section' of length >=3
        val = ns.get('woodwind_section')
        if isinstance(val, list) and len(val) >= 3:
            return True, 'Good job - found woodwind_section with at least 3 items'
        return False, 'Please create a list named woodwind_section with at least 3 items'


class Week3Validator(BaseValidator):
    def validate(self, ns: dict):
        # Expect a tempo variable between 60 and 200
        tempo = ns.get('tempo')
        if isinstance(tempo, int) and 60 <= tempo <= 200:
            return True, f'Good job - tempo set to {tempo} BPM'
        return False, 'Please set tempo to an integer value between 60 and 200'


class Week4Validator(BaseValidator):
    def validate(self, ns: dict):
        # Expect at least one function definition
        functions = [name for name, obj in ns.items() if callable(obj) and not name.startswith('_')]
        if len(functions) > 0:
            return True, f'Good job - found function(s): {", ".join(functions[:3])}'
        return False, 'Please define at least one function'


class Competition1Validator(BaseValidator):
    def validate(self, ns: dict):
        # For competition, check for multiple settings
        tempo = ns.get('tempo')
        color = ns.get('uniform_color')
        volume = ns.get('volume')
        
        # Check if all required variables are set
        if tempo is None:
            return False, 'Please set tempo (e.g., tempo = 120)'
        if color is None:
            return False, 'Please set uniform_color (e.g., uniform_color = "blue")'
        if volume is None:
            return False, 'Please set volume (e.g., volume = 7)'
            
        # Validate types
        if not isinstance(tempo, int) or not (60 <= tempo <= 200):
            return False, 'Tempo should be an integer between 60 and 200'
        if not isinstance(color, str) or len(color) == 0:
            return False, 'Uniform color should be a non-empty string'
        if not isinstance(volume, int) or not (0 <= volume <= 10):
            return False, 'Volume should be an integer between 0 and 10'
            
        return True, 'Ready for competition! All settings configured correctly.'


class Competition2Validator(BaseValidator):
    def validate(self, ns: dict):
        # More advanced competition validation
        tempo = ns.get('tempo')
        color = ns.get('uniform_color')
        volume = ns.get('volume')
        formation = ns.get('formation')
        
        # Check if all required variables are set
        if tempo is None:
            return False, 'Please set tempo (e.g., tempo = 120)'
        if color is None:
            return False, 'Please set uniform_color (e.g., uniform_color = "blue")'
        if volume is None:
            return False, 'Please set volume (e.g., volume = 7)'
            
        # Validate types
        if not isinstance(tempo, int) or not (60 <= tempo <= 200):
            return False, 'Tempo should be an integer between 60 and 200'
        if not isinstance(color, str) or len(color) == 0:
            return False, 'Uniform color should be a non-empty string'
        if not isinstance(volume, int) or not (0 <= volume <= 10):
            return False, 'Volume should be an integer between 0 and 10'
            
        return True, "Excellent! You're ready for the advanced competition."
