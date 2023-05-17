import pandas as pd
import pytesseract

file_name = '5.jpeg'
tsv_file_name = 'test.tsv'

data = pytesseract.image_to_data(file_name, output_type=pytesseract.Output.STRING)
with open(tsv_file_name, 'w') as f:
    f.write(data)

df = pd.read_csv(tsv_file_name, sep="\t", lineterminator="\n", verbose=True)

print(df["text"])
print(df["conf"])
