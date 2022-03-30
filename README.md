# Linkchecker

Recursively check for bad links on a website.

Will check that external links return 200 but will only find new URLs to parse on the same domain as the starting URL.

## Installation

Acquire `main.py`.

## Usage

### Basic usage

```bash
$ python3 main.py https://example.com

500 https://example.com/some-broken-url
None https://broken.example.com Connection error

2 good URLs!
2 bad URLs :(
```

### Get real-time feedback with `-v` or `--verbose`

```bash
$ python3 main.py https://example.com
https://example.com ... 200
https://example.com/good ... 200

500 https://example.com/some-broken-url
None https://broken.example.com Connection error

2 good URLs!
2 bad URLs :(
```

### JSON Output

Note: don't use -v with this as that will generate an invalid JSON file, which is a problem I could probably get around but haven't yet, so just don't do that, ok?

```bash
$ python main.py https://example.com --format json > output.json
```
