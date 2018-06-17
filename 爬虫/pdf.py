from PyPDF2 import PdfFileReader, PdfFileWriter
import glob

pdf_writer = PdfFileWriter()
for filename in glob.glob('E:/Working/Cryptology/lecture1-12/*'):
	pdf = PdfFileReader(filename)
	for page in range(1, pdf.getNumPages() - 1):
		pdf_writer.addPage(pdf.getPage(page))
with open('result.pdf', 'wb') as f:
	pdf_writer.write(f)