from tika import parser
from PyPDF2 import PdfFileWriter, PdfFileReader 
import os.path

def paginate_pdf(fp, threshold = 1):
    output_files_list = []
    
    filename, ext = os.path.splitext(fp)
    with open(fp, 'rb') as pdf_file_ref:
        input1 = PdfFileReader(pdf_file_ref)
        page_count = input1.getNumPages()
        if page_count < 1:
            raise Exception

        if page_count <= threshold:
            return [('single', fp)]

        for page in range(page_count):
            output = PdfFileWriter()
            output.addPage(input1.getPage(page))

            new_file = "{}-{}{}".format(filename,page,ext)
            output_files_list.append(('multi',new_file))
            with open(new_file, "wb") as outputStream:
                output.write(outputStream)
    
    return output_files_list


def crack_pdf(fp):
    parsed = parser.from_file(fp)
    #print(parsed["metadata"])
    return parsed["content"]

if __name__ == "__main__":
    import argparse

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-f","--filepath",help="Filepath")
    args = argparser.parse_args()
    
    pdfs = paginate_pdf(args.filepath)

    for pdf in pdfs:
        content = crack_pdf(pdf)
        print("WORKING ON {}".format(pdf))
        print(content)