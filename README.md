# Pseudo-random number generators

This is a simple implementation of three pseudo-random number generators (Linear Congruential Generator, Mersenne Twister, Xorshift)
for my university assignment.

You can access report here: [Link](https://cxrsed.notion.site/Report-ae0ebbd0e41845b599f3c6bc39b5baa7)

## Installation

```sh
pip install -r requirements.txt
```

## Usage

You can import any of the generators by direct import `from generators import SomeGenerator` or get a list of all generators:

```py
import generators


print(generators.__all__)
# [<class 'generators.lcg.LinearCongruentialGenerator'>, ...]
```

Also, you can create your own generators on top of existing `PseudoRandomNumberGenerator` abstract class.  
If you want to make your generator accessible through `import generators`, you can add following code in your file:

```py
__all__ = ["YourGeneratorClass"]
```

After this, your class will be loaded in `generators/__init__.py`.

## Statistics

In `tests.py` file, you can find `PseudoRandomTests` class. It fetches all generators inside of `generators/` folder and does Chi-Square and Kolmogorov-Smirnov tests with `scipy.stats` module. After running the tests, `out/` folder will appear, containing generated numbers, text report of tests, and images with some stats.

## Testing

Currently, there are no tests yet.