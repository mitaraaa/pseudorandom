"""
The `generators` package contains implementations of various pseudorandom
number generators that adhere to the `PseudoRandomNumberGenerator` class.

Pseudorandom number generators (PRNGs) are algorithms used to
generate a sequence of numbers that appear random but are
actually deterministic. These generators are widely used in simulation,
cryptography, and other applications where randomness is required.

To create a new generator, follow these steps:
1. Create a new Python module within the `generators` package.
2. In the new module, define your generator class and make sure it inherits
    from `PseudoRandomNumberGenerator`.
3. Add `__all__ = ["YourGeneratorClass"]` for your class to be visible.

Please note that the pseudorandom number generators
in this package are intended for educational and illustrative purposes.
If you require high-quality random number generation,
it is recommended to use the random module from the Python
standard library.
"""


import os
import importlib

directory = os.path.dirname(__file__)

__all__ = []

for module_file in os.listdir(directory):
    if module_file.endswith(".py") and module_file != "__init__.py":
        module_name = module_file[:-3]
        module_path = ".".join([__name__, module_name])
        module = importlib.import_module(module_path)
        __all__.append(getattr(module, module.__all__[0]))
