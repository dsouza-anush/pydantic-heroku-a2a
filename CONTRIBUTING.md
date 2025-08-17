# Contributing to Pydantic Heroku A2A Demo

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Pydantic Heroku A2A Demo.

## Code of Conduct

By participating in this project, you are expected to uphold a respectful and inclusive environment.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Submit a pull request

## Development Setup

1. Clone the repository
2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Install development dependencies
```
4. Create a `.env` file from the example
```bash
cp .env.example .env
```
5. Edit the `.env` file with your Heroku Inference API key

## Testing

Run the tests with:
```bash
pytest
```

## Code Style

This project follows the [Black](https://github.com/psf/black) code style. Please ensure your code adheres to this style before submitting a pull request.

```bash
black .
```

## Documentation

Please update the documentation if you make changes to the API or add new features.

## Submitting a Pull Request

1. Ensure your code follows the style guidelines
2. Write tests for your changes
3. Update the documentation as needed
4. Submit your pull request with a clear description of the changes

## License

By contributing to this project, you agree that your contributions will be licensed under its MIT license.