# running: ./this-script-name input.pdf output.pdf

import sys

from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from PyPDF2.pdf import PageObject


class OutputPage:
    def __init__(self):
        self.page_width = 841
        self.page_height = 595
        self.border = 20
        self.margin = 20
        self.front = []
        self.back = []
        self.content_size = 0
        self.card_width = None

    def is_full(self):
        return self.content_size == 8

    def is_not_empty(self):
        return self.content_size != 0

    def add_card(self, front: PageObject, back: PageObject):
        if self.is_full():
            raise Exception('Cannot add card to page: Page is already full')
        self.front.append(front)
        self.back.append(back)
        self.content_size += 1
        self.card_width = front.mediaBox.upperRight[0]
        self.card_height = front.mediaBox.upperRight[1]

    def create_pdf(self):
        output = PdfFileWriter()
        front_page = pdf.PageObject.createBlankPage(None, self.page_width, self.page_height)
        self.fill_front_page(front_page, self.front)
        output.addPage(front_page)
        rear_page = pdf.PageObject.createBlankPage(output)
        self.fill_rear_page(rear_page, self.back)
        output.addPage(rear_page)
        return output

    def append_to_pdf(self, output):
        front_page = pdf.PageObject.createBlankPage(output)
        self.fill_front_page(front_page, self.front)
        output.addPage(front_page)
        rear_page = pdf.PageObject.createBlankPage(output)
        self.fill_rear_page(rear_page, self.back)
        output.addPage(rear_page)

    def fill_front_page(self, target_page, list):
        x = self.border
        y = self.border
        for i in range(0, min(len(list), 4)):
            page = list[i]
            target_page.mergeScaledTranslatedPage(page, 1, x, y + self.card_height + self.border)
            x += self.card_width + self.margin
        if len(list) <= 4:
            return  # no more cards
        x = self.border
        y = self.border
        for i in range(4, min(len(list), 8)):
            page = list[i]
            target_page.mergeScaledTranslatedPage(page, 1, x, y)
            x += self.card_width + self.margin

    def fill_rear_page(self, target_page, list):
        x = self.page_width - self.border - self.card_width
        y = self.border
        for i in range(0, min(len(list), 4)):
            page = list[i]
            target_page.mergeScaledTranslatedPage(page, 1, x, y + self.card_height + self.border)
            x -= self.card_width + self.margin
        if len(list) <= 4:
            return  # no more cards
        x = self.page_width - self.border - self.card_width
        y = self.border
        for i in range(4, min(len(list), 8)):
            page = list[i]
            target_page.mergeScaledTranslatedPage(page, 1, x, y)
            x -= self.card_width + self.margin


#
# Open source pdf and iteratively create OutputPages and fill them with cards
#
output_page = OutputPage()
target_pdf = None

input = PdfFileReader(open(sys.argv[1], "rb"))

for i in range(0, int(input.getNumPages() / 2)):
    first = input.getPage(2 * i)
    second = input.getPage(2 * i + 1)

    if output_page.is_full():
        if target_pdf is None:
            target_pdf = output_page.create_pdf()
            output_page = OutputPage()
        else:
            output_page.append_to_pdf(target_pdf)
            output_page = OutputPage()

    output_page.add_card(first, second)

if output_page.is_not_empty():
    output_page.append_to_pdf(target_pdf)

target_pdf.write(open(sys.argv[2], "wb"))
