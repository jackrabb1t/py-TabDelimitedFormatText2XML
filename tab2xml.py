"""Read tab-separated files and output XML"""

def create_parser():
    from optparse import OptionParser
    parser = OptionParser('usage: python %s filename.tsv [options]' % __file__)
    return parser

def get_rows(fname):
    """
    Parse table rows from a TSV file.  Each row is a list of cells.  Each
    cell is a string.
    """
    #
    # Read rows from the file, discarding empty (zero length) rows.
    # Check that the width of each row is equal.  If not, then
    # there's a stray tab somewhere, and we cannot proceed.
    #
    lines = filter(lambda x: x, open(fname).read().split('\n'))
    rows = map(lambda x: x.split('\t'), lines)
    row_widths = map(len, rows)
    assert(sum(row_widths) == len(row_widths)*row_widths[0])
    return rows

def rows2xml(rows):
    #
    # http://www.postneo.com/projects/pyxml/
    #
    from xml.dom.minidom import Document
    doc = Document()
    table = doc.createElement('table')
    doc.appendChild(table)
    for i, r in enumerate(rows):
        if i == 0:
            #
            # Don't write column labels as a separate row.
            #
            continue
        row = doc.createElement('row')
        row.setAttribute('id', str(i))
        for j, c in enumerate(r):
            cell = doc.createElement('cell')
            name = doc.createElement('name')
            name.appendChild(doc.createTextNode(rows[0][j]))
            val = doc.createElement('val')
            val.appendChild(doc.createTextNode(c))

            cell.appendChild(name)
            cell.appendChild(val)
            row.appendChild(cell)

        table.appendChild(row)

    return doc

def main():
    parser = create_parser()
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error('incorrect number of arguments')

    rows = get_rows(args[0])
    doc = rows2xml(rows)
    print doc.toprettyxml(indent='  ')

if __name__ == '__main__':
    main()
