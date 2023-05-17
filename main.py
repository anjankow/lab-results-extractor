import pytesseract

print('langs:')
print(pytesseract.get_languages())

file_name = '5.jpeg'
text = pytesseract.image_to_string(file_name)
print(text)

data = pytesseract.image_to_boxes(file_name) #, output_type='dict', )
print(data)


data = pytesseract.image_to_data(file_name) #, output_type='dict', )
print(data)
with open('test.tsv', 'w+b') as f:
    f.write(data)


pdf = pytesseract.image_to_pdf_or_hocr(file_name, extension='pdf')
with open('test.pdf', 'w+b') as f:
    f.write(pdf)

xml = pytesseract.image_to_alto_xml(file_name)
with open('test.xml', 'w+b') as f:
    f.write(pdf)
