# Daangn Crawler

## 1. Poetry Installation

````sh
# Linux, macOS, Windows (WSL)
curl -sSL https://install.python-poetry.org | python3 -

# Windows (Powershell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

Reference: https://python-poetry.org/docs/#installing-with-the-official-installer

## 2. Installation

```sh
git clone https://github.com/jwkwon0817/daangn-crawler
cd daangn-crawler
poetry install
```

## 3. Run

```sh
poetry run python -m app.crawler.main
```
````
