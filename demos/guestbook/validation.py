
from wheezy.validation import Validator
from wheezy.validation.rules import length
from wheezy.validation.rules import required

greeting_validator = Validator({
    'author': [length(max=20)],
    'message': [required, length(min=5, max=512)],
})
