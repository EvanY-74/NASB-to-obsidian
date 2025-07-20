import os

os.makedirs(os.path.join('output', 'Bible'), exist_ok = True)

def create_book(name):
    os.makedirs(os.path.join('output', 'Bible', name), exist_ok = True)

def write_chapter(book, book_folder_name, chapter_number, text, is_last_chapter = False):
    name = f'{book} {chapter_number}' # maybe I don't need this variable, we'll see
    with open(os.path.join('output', 'Bible', book_folder_name, name + '.md'), "w", encoding="utf-8") as file:
        top = '\n---\n'
        file.write(top + text)

with open(os.path.join('output', 'epub.md'), 'r', encoding='utf-8') as file:
    paragraphs = file.read().split('\n')

def parse_paragraph(paragraph):
    chapter_book, text = paragraph.split(' New American Standard Bible ', 1)
    book, chapter_number = chapter_book.rsplit(' ', 1)

    text = text.split(' ')
    for i in range(len(text)):
        if text[i].isdigit():
            text[i] = '\n###### ' + text[i] + '\n'
            if i == len(text) - 1: text[i] += '\n' #TODO: Is there a \n at the beginning of each chapter?
    
    return book, int(chapter_number), ' '.join(text)

book = ''
book_folder_name = ''
book_index = 0
chapter_number = 0
chapter_text = ''

for paragraph in paragraphs:
    if paragraph == '' or paragraph == '---': continue

    new_book, new_chapter_number, text = parse_paragraph(paragraph)

    if new_book != book:
        book_index += 1
        book = new_book
        book_folder_name = f'{str(book_index).zfill(2)} - {book}'
        create_book(book_folder_name)
        chapter_number = 1
        chapter_text = text

    elif new_chapter_number != chapter_number:
        chapter_number = new_chapter_number
        chapter_text = text

    else:
        chapter_text += text
    
    write_chapter(book, book_folder_name, chapter_number, chapter_text)
    