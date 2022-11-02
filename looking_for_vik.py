import fitz
import pdfkit

pdf_document = "dict.pdf"
doc = fitz.open(pdf_document)
text = []
for current_page in range(len(doc)):
    page = doc.load_page(current_page) #загружаем каждую страницу pdf-словаря
    page_text = page.get_text("html") #берём со стр. текст в формате html, т.к. будем "ловить" начало словарной статьи по выравниванию
    text.append(page_text)
entries = []
for page in text:
    paragraphs = page.split("\n") #делим страницу на строки
    for i in range (0, len(paragraphs)-1):
        if "left:315" in paragraphs[i] or "left:60" in paragraphs[i]: #ищем строки с нужным выравниванием
            entry = paragraphs[i]
            while i <= len(paragraphs)-2:
                if "left:315" not in paragraphs[i+1] and "left:60" not in paragraphs[i+1]: #останавливаемся, встретив новое начало словарной статьи
                    entry += paragraphs[i+1]
                    i = i+1
                else:
                    break
            entries.append(entry)
vik_entries = []
for entry in entries:
    if "vik" in entry: #теперь из списка всех словарных статей берём те, где есть нужный формант
        vik_entries.append(entry)
with open("vik_entries.html", "w+", encoding="utf-8") as f:
    for vik_entry in vik_entries:
        f.write(vik_entry)
        
#далее, чтобы  сохранить файл сразу как pdf, нужно не только установить модуль pdfkit, но и opensourse инструмент wkhtmltopdf
#можно выбрать нужный установщик по этой ссылке https://wkhtmltopdf.org/downloads.html
#в качестве альтернативы можно остановиться на сохранении файла html и переформатировать его в pdf на каком-нибудь онлайн-ресурсе
#вроде этого https://convertio.co/ru/html-pdf/

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
pdfkit.from_file('vik_entries.html', 'vik_entries.pdf', configuration=config) 

