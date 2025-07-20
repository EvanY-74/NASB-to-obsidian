# Fully written by ChatGPT :|

import os
from ebooklib import epub
from bs4 import BeautifulSoup

def clean_html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    md_lines = []

    for elem in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'span']):
        text = elem.get_text(strip=True)
        if not text:
            continue
        # Use Markdown-style headings
        if elem.name == 'h1':
            md_lines.append(f'# {text}')
        elif elem.name == 'h2':
            md_lines.append(f'## {text}')
        elif elem.name == 'h3':
            md_lines.append(f'### {text}')
        elif elem.name == 'h4':
            md_lines.append(f'#### {text}')
        else:
            md_lines.append(text)

    return '\n\n'.join(md_lines)

def epub_to_markdown(epub_path, output_path=os.path.join('output', 'epub.md')):
    book = epub.read_epub(epub_path)
    all_text = []

    print(f'\n📚 Total items: {len(book.items)}\n')

    for item in book.get_items():
        if item.get_name().endswith('.html') or item.get_name().endswith('.xhtml'):
            try:
                print(f'📖 Processing: {item.get_name()}')
                content = item.get_content().decode('utf-8', errors='ignore')
                md = clean_html_to_markdown(content)
                if md.strip():
                    all_text.append(md)
            except Exception as e:
                print(f'⚠️ Error reading {item.get_name()}: {e}')

    if all_text:
        full_text = '\n\n---\n\n'.join(all_text)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f'\n✅ Markdown file saved to: {output_path}')
    else:
        print('\n❌ No usable HTML content found in EPUB.')

epub_to_markdown(os.path.join('NASB', 'NASB New American Standard Bible (NASB).epub'))