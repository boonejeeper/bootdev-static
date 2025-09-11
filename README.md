# Static Site Generator

A Python-based static site generator that converts Markdown files to HTML with support for configurable base paths and recursive content processing.

## Features

- **Recursive Content Processing**: Automatically processes all Markdown files in the content directory while maintaining directory structure
- **Configurable Base Path**: Support for custom base paths for deployment in subdirectories or behind reverse proxies
- **Markdown Support**: Full Markdown parsing with support for:
  - Headings (H1-H6)
  - Bold and italic text
  - Inline code (single backticks) and code blocks (triple backticks)
  - Links and images
  - Blockquotes
  - Ordered and unordered lists
- **Template System**: HTML template with placeholder replacement for title and content
- **Static Asset Management**: Automatic copying of static files (CSS, images, etc.)

## Installation

1. Clone the repository
2. Install dependencies (if using a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Generate the site with the default root path (`/`):

```bash
python src/main.py
```

### Custom Base Path

Generate the site with a custom base path:

```bash
# Custom basepath
python src/main.py /my-blog

# Path normalization (automatically adds leading slash)
python src/main.py my-site

# Trailing slash removal
python src/main.py /test-site/
```

### Usage Examples

```bash
# Default root path - generates paths like href="/index.css"
python src/main.py

# Custom basepath - generates paths like href="/my-blog/index.css"
python src/main.py /my-blog

# Path normalization - "my-site" becomes "/my-site"
python src/main.py my-site

# Trailing slash removal - "/test-site/" becomes "/test-site"
python src/main.py /test-site/
```

## Project Structure

```
bootdev-static/
├── content/                 # Markdown content files
│   ├── index.md            # Homepage
│   └── blog/               # Blog posts directory
│       ├── contact/
│       ├── glorfindel/
│       ├── majesty/
│       └── tom/
├── src/                    # Source code
│   ├── main.py            # Main entry point
│   ├── nodeutilities.py   # Markdown parsing utilities
│   ├── textnode.py        # Text node classes
│   ├── htmlnode.py        # HTML node classes
│   ├── leafnode.py        # Leaf node classes
│   └── parentnode.py      # Parent node classes
├── static/                 # Static assets (CSS, images)
├── template.html          # HTML template
└── public/                # Generated site output
```

## How It Works

1. **Content Discovery**: Recursively scans the `content/` directory for Markdown files
2. **Path Mapping**: Maps Markdown file paths to HTML output paths while preserving directory structure
3. **Markdown Processing**: Converts Markdown to HTML using custom parsing logic
4. **Template Rendering**: Replaces placeholders in the HTML template with processed content
5. **Path Replacement**: Updates all `href="/` and `src="/` patterns with the configured base path
6. **Static Asset Copying**: Copies static files from `static/` to `public/`

## Markdown Features

### Inline Code
Use single backticks for inline code:
```markdown
This is `inline code` within a paragraph.
```

### Code Blocks
Use triple backticks for code blocks:
```markdown
```
def hello_world():
    print("Hello, World!")
```
```

### Other Features
- **Bold text**: `**bold**`
- **Italic text**: `_italic_`
- **Links**: `[text](url)`
- **Images**: `![alt](src)`
- **Headings**: `# H1`, `## H2`, etc.
- **Lists**: `- item` or `1. item`
- **Blockquotes**: `> quote`

## Development

### Running Tests
```bash
python -m pytest src/test_*.py
```

### Adding New Content
1. Add Markdown files to the `content/` directory
2. Maintain the desired directory structure
3. Run the generator: `python src/main.py [basepath]`

## License

This project is part of the Boot.dev static site generator course.
