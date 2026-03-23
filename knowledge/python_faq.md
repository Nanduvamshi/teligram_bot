# Python Frequently Asked Questions

## What are decorators in Python?
Decorators are a way to modify or extend the behavior of functions or classes without changing their source code. A decorator is a function that takes another function as an argument, adds some functionality, and returns a new function. You use the @decorator_name syntax above a function definition. Common built-in decorators include @staticmethod, @classmethod, and @property. Decorators are widely used in web frameworks like Flask and Django for routing and authentication.

## What is the difference between a list and a tuple?
Lists are mutable sequences defined with square brackets [], while tuples are immutable sequences defined with parentheses (). Since tuples are immutable, they can be used as dictionary keys and are slightly faster than lists. Use lists when you need to modify the collection, and tuples when you need an unchangeable sequence of items. Lists have methods like append(), extend(), and remove(), while tuples only have count() and index().

## What is the Global Interpreter Lock (GIL)?
The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time. This means that even on multi-core processors, only one thread runs Python code simultaneously. The GIL exists to protect memory management in CPython. For CPU-bound tasks, use multiprocessing instead of threading to achieve true parallelism. For I/O-bound tasks, threading still works well because the GIL is released during I/O operations.

## What are list comprehensions?
List comprehensions provide a concise way to create lists based on existing lists or iterables. The syntax is [expression for item in iterable if condition]. For example, [x**2 for x in range(10) if x % 2 == 0] creates a list of squares of even numbers. They are more readable and often faster than equivalent for loops. Python also supports dictionary comprehensions and set comprehensions with similar syntax.

## What is the difference between == and is?
The == operator checks for value equality, meaning it compares the values of two objects. The is operator checks for identity, meaning it verifies whether two variables point to the exact same object in memory. For example, a = [1, 2, 3] and b = [1, 2, 3] would give a == b as True but a is b as False because they are different objects with the same values. Use is primarily for comparing with None: if x is None.

## What are Python virtual environments?
Virtual environments are isolated Python environments that allow you to install packages for a specific project without affecting other projects or the system Python installation. You create one using python -m venv myenv and activate it. Each virtual environment has its own Python binary and pip. This prevents version conflicts between projects. Tools like conda, poetry, and pipenv also manage virtual environments with additional features.
