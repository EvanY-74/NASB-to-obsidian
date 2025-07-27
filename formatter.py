import os

os.makedirs(os.path.join('output', 'Bible'), exist_ok = True)

def create_book(name):
    os.makedirs(os.path.join('output', 'Bible', name), exist_ok = True)

def write_chapter(index):
    global chapters

    with open(os.path.join('output', 'Bible', chapters[index].book_folder_name, chapters[i].name + '.md'), "w", encoding="utf-8") as file:
        # 🡠 side
        if index != 0:
            prev_book = chapters[index - 1].book
            prev_name = chapters[index - 1].name
            if prev_book == chapters[index].book:
                top = f'[[{prev_name}|🡠]] '
            else:
                top = f'[[{prev_name}|🡠 {prev_name}]] | '
        else:
            top = '  '

        # middle
        top += f'**{chapters[i].name}**'

        # 🡠 side
        if index != len(chapters) - 1:
            next_book = chapters[index + 1].book
            next_name = chapters[index + 1].name
            if next_book == chapters[index].book:
                top += f' [[{next_name}|🡢]]'
            else:
                top += f' | [[{next_name}|{next_name} 🡢]]'

        top += '\n\n---\n'

        file.write(top + chapters[index].text)

with open(os.path.join('output', 'epub.md'), 'r', encoding='utf-8') as file:
    paragraphs = file.read().split('\n')

def parse_paragraph(paragraph):
    chapter_book, text = paragraph.split(' New American Standard Bible ', 1)
    book, number = chapter_book.rsplit(' ', 1)

    text = text.split(' ')
    for i in range(len(text)):
        if text[i].isdigit():
            text[i] = '\n###### ' + text[i] + '\n'
            if i == len(text) - 1: text[i] += '\n' #TODO: Is there a \n at the beginning of each chapter?
    
    return book, number, ' '.join(text)

class Chapter():
    def __init__(self, book, book_folder_name, number, text):
        self.book = book
        self.book_folder_name = book_folder_name
        self.number = number
        self.text = text
        self.name = self.book + ' ' + self.number

chapters = []

book_index = 0

for paragraph in paragraphs:
    if paragraph == '' or paragraph == '---': continue

    book, number, text = parse_paragraph(paragraph)

    if len(chapters) == 0 or book != chapters[-1].book:
        book_index += 1
        book_folder_name = f'{str(book_index).zfill(2)} - {book}'
        create_book(book_folder_name)
        chapters.append(Chapter(book, book_folder_name, '1', text))

    elif number != chapters[-1].number:
        chapters.append(Chapter(book, chapters[-1].book_folder_name, number, text))
    else:
        chapters[-1].text += text
    
# write_chapter(book, book_folder_name, chapter_number, chapter_text)

for i in range(len(chapters)):
    write_chapter(i)