# Python Mastery Path

A structured learning path for mastering Python with a focus on strict typing and modern tooling.

## Setup

1. Install Python 3.11+ using [pyenv](https://github.com/pyenv/pyenv):
   ```bash
   brew install pyenv
   pyenv install 3.11.8
   pyenv global 3.11.8
   ```

2. Install [uv](https://github.com/astral-sh/uv) (fast Python package installer):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Create and activate a virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # On Unix/macOS
   ```

4. Install dependencies:
   ```bash
   uv pip install -e .
   ```

## Learning Path

### 1. Basics (`basics/`)
- Python syntax and fundamentals
- Type hints and static typing
- Basic data structures
- Control flow
- Functions and modules

### 2. Intermediate (`intermediate/`)
- Object-oriented programming
- Decorators and context managers
- Error handling
- File I/O
- Working with collections
- Generators and iterators

### 3. Advanced (`advanced/`)
- Metaclasses
- Asynchronous programming
- Type system advanced features
- Design patterns
- Performance optimization
- Memory management

### 4. Projects (`projects/`)
- Real-world applications
- Web development
- Data processing
- API development
- Testing and deployment

### 5. Exercises (`exercises/`)
- Practice problems
- Coding challenges
- Type checking exercises
- Best practices

## Development Tools

- **Type Checking**: `mypy` with strict settings
- **Code Formatting**: `black` and `isort`
- **Linting**: `ruff`
- **Testing**: `pytest` with coverage
- **Package Management**: `uv`

## Type System

This project uses a strict type system similar to TypeScript. Key features:
- Type hints for all functions and variables
- No implicit `Any` types
- Strict type checking with `mypy`
- Pydantic for runtime type validation

## Best Practices

1. Always use type hints
2. Write docstrings for all public functions
3. Follow PEP 8 style guide
4. Write tests for all new code
5. Use type aliases for complex types
6. Prefer composition over inheritance
7. Use dataclasses for data containers
8. Implement proper error handling

## Getting Started

1. Start with the basics directory
2. Complete exercises for each topic
3. Move to intermediate concepts
4. Work on projects to apply knowledge
5. Review advanced topics as needed

## Resources

- [Python Documentation](https://docs.python.org/3/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [PEP 8 - Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Mypy Documentation](https://mypy.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/) 
