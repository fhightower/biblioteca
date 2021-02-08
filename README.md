# Biblioteca

[![Build Status](https://travis-ci.com/fhightower/biblioteca.svg?branch=main)](https://travis-ci.com/fhightower/biblioteca)
[![codecov](https://codecov.io/gh/fhightower/biblioteca/branch/main/graph/badge.svg?token=FVbbjk9B65)](https://codecov.io/gh/fhightower/biblioteca)


Memory augmentation system to help you remember what you want to remember. Also, a personal search-engine.

## Usage

```python
from biblioteca import hub

l = [
    'http://recursivedrawing.com/'
]

for i in l:
    print(i)
    hub.add(i)
```

... more documentation coming soon...

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and Floyd Hightower's [Python project template](https://github.com/fhightower-templates/python-project-template).
