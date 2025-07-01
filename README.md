# Gitfo

[![GitHub version](https://img.shields.io/badge/version-0.2.0-green?logo=github&logoColor=white)](https://github.com/qProve-P/gitfo)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/qProve-P/gitfo/blob/main/LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)


---

**Gitfo** is a command-line tool that retrieves information from the GitHub API about repositories and users. It supports detailed views, optional authentication, and output to various file formats.

## Features

- Get detailed info about GitHub repositories
- Get info about GitHub user profiles
- Get info about GitHub users and repositories in bulk from a file
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

#### Command Template:
```bash
python -m gitfo <command> [options]
```

### Help
---

#### Get Help About App:
```bash
python -m gitfo --help
```

#### Get Help About Command:
```bash
python -m gitfo <command> --help
```

### General
---

#### Save Output To File:
```bash
python -m gitfo <command> <input> -o out.json
```

#### Use GitHub Token:
```bash
python -m gitfo <command> <input> -a YOUR_GITHUB_TOKEN
```

### Repository
---

#### Repository Info:
```bash
python -m gitfo repo octocat/Hello-World
```

#### Repository With Languages:
```bash
python -m gitfo repo octocat/Hello-World --with-languages
```

#### Full Repository Info (branches, languages, releases, PRs):
```bash
python -m gitfo repo octocat/Hello-World --full
```

### User
---

#### User Info:
```bash
python -m gitfo user octocat
```

### Bulk Operations
---

#### Batch Of Repositories:
```bash
python -m gitfo repobatch <source file> <output file> [options]
```

#### Batch Of Users:
```bash
python -m gitfo userbatch <source file> <output file>
```

### Rate Limit
---

#### Get Your Rate Limit:
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
