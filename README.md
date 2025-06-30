# Gitfo

[![GitHub version](https://img.shields.io/badge/version-0.1.0-green?logo=github&logoColor=white)](https://github.com/qProve-P/gitfo)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/qProve-P/gitfo/blob/main/LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![GitHub top language](https://img.shields.io/github/languages/top/qProve-P/gitfo)


---

**Gitfo** is a command-line tool that retrieves information from the GitHub API about repositories and users. It supports detailed views, optional authentication, and output to various file formats.

## Features

- Get detailed info about GitHub repositories
- Query GitHub user profiles
- Fetch releases, branches, open PR count, language breakdown
- Use a GitHub token to bypass rate limits
- Save results as `.json`, `.txt`, or `.csv`
- Clean, colorized terminal output

## Installation
```bash
git clone https://github.com/qProve-P/Gitfo.git
cd gitfo
pip install -r requirements.txt
```

## Usage

### Command Template:
```bash
python -m gitfo <command> [options]
```

### Get Help About App:
```bash
python -m gitfo --help
```

### Get Help About Command:
```bash
python -m gitfo <command> --help
```

### Repository Info:
```bash
python -m gitfo repo octocat/Hello-World
```

### Repository With Languages:
```bash
python -m gitfo repo octocat/Hello-World --with-languages
```

### Full Repository Info (branches, languages, releases, PRs):
```bash
python -m gitfo repo octocat/Hello-World --full
```

### Save Output To File:
```bash
python -m gitfo repo octocat/Hello-World -o repo.json
```

### Use GitHub Token:
```bash
python -m gitfo repo octocat/Hello-World -a YOUR_GITHUB_TOKEN
```

### User Info:
```bash
python -m gitfo user octocat
```

### Save User Info To File:
```bash
python -m gitfo user octocat --output user.json
```

### Get Your Rate Limit:
```bash
python -m gitfo limit YOUR_GITHUB_TOKEN
```

## Running Tests

Tests are written using pytest and use mocking to simulate API responses.

To run a specific test file:
```bash
python -m pytest tests/test_<filename>.py
```

## Authentication & Rate Limits

GitHub’s API limits unauthenticated requests to 60 per hour.  
By providing a GitHub token (`-a YOUR_GITHUB_TOKEN`), you can increase this limit to 5000 requests per hour, avoiding errors due to rate limiting.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/qProve-P/gitfo/blob/main/LICENSE) file for details.
