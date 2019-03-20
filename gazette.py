import re

import utils


def main():
    for year in range(2006, 2019 + 1):
        download_files(year)


def download_files(year: int) -> None:
    path = utils.download_file(YEAR_URL.format(year=year), 'gazette/{}.html'.format(year))
    text = path.read_text()
    for m in re.finditer(r'text/(\d+_\w+\d+)_Registrar.cfm', text):
        docid = m.group(1)
        utils.download_file(DOC_URL.format(year=year, docid=docid), 'gazette/{}/{}.txt'.format(year, docid))


YEAR_URL = 'http://www.qp.alberta.ca/alberta_gazette.cfm?page=gazette_{year}_registrar.cfm'
DOC_URL = 'http://www.qp.alberta.ca/documents/gazette/{year}/text/{docid}_Registrar.cfm'


if __name__ == '__main__':
	main()
