from PyPDF2 import PdfReader, PdfFileWriter
import re
import streamlit as st
from zipfile import ZipFile
st.title("Ronéo splitter")
prefix = st.text_input('Prefix', 'S1_R2_')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    text = ""
    i = 0

    subdocs = []
    subdocs.append(PdfFileWriter())
    titles = []
    titles.append("programme")
    for page in reader.pages:
        text = page.extract_text()
        x = re.search("Semaine[^\n]*\d+[^\n]*\n", text)
        if x is not None:
            i += 1
            res = re.search("Coronéo.+20\d{2}\s*(.+)\n", text)
            if res is not None:
                title = res.groups()[0]
                # title = re.sub("\-", " ", title)
                title = re.sub("\s{2,}", " ", title)
                title = title[0:60]
                st.write(title)
                titles.append(title)
                subdocs.append(PdfFileWriter())
            else:
                st.write("title not found")

        subdocs[i].addPage(page)
    zipObj = ZipFile('output.zip', 'w')
    for j in range(i):
        filename = f"{prefix}{j}_{titles[j]}.pdf"
        with open( filename, "wb") as outputStream:
            subdocs[j].write(outputStream)
        zipObj.write(filename)
    st.write(f"{i} elements detected")
    zipObj.close()
    # text_contents = '''This is some text'''
    # st.download_button('Download output', 'output.zip')
    with open("output.zip", "rb") as file:
        btn = st.download_button(
            label="Download zip",
            data=file,
            file_name="output.zip"
        )