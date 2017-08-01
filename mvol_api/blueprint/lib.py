import xml.etree.ElementTree as ElementTree


class OCRBuilder:
    # Based on work by https://github.com/johnjung.
    # See:
    # https://github.com/johnjung/pos-to-xtf-converted-book-2/blob/master/src/build-ia-bookreader-ocr.py
    def __init__(self, dc, info_dicts, min_year=1900, max_year=2000):
        self.dc = ElementTree.fromstring(dc)
        self.info_dicts = info_dicts
        self.min_year = min_year
        self.max_year = max_year

        ElementTree.register_namespace('xtf', 'http://cdlib.org/xtf')

    # Begin Copy-Pasted Meta Requirements

    def get_human_readable_date(self):
        months = {
            '01': 'January',
            '02': 'February',
            '03': 'March',
            '04': 'April',
            '05': 'May',
            '06': 'June',
            '07': 'July',
            '08': 'August',
            '09': 'September',
            '10': 'October',
            '11': 'November',
            '12': 'December'
        }
        d = self.get_dc_date().split('-')
        if len(d) == 1:  # year
            return d[0]
        elif len(d) == 2:  # month  year
            return '%s %s' % (months[d[1]], d[0])
        else:
            return '%s %d, %s' % (months[d[1]], int(d[2]), d[0])

    def get_year_range(self):
        return '%s-%s' % (self.min_year, self.max_year)

    def get_dc_date(self):
        return self.dc.find('date').text

    def get_dc_description(self):
        return self.dc.find('description').text

    def get_dc_identifier(self):
        return self.dc.find('identifier').text

    def get_decade(self):
        return "%s0's" % self.get_year()[0:3]

    def get_year(self):
        return self.get_dc_date().split('-')[0]

    def get_dc_title(self):
        return self.dc.find('title').text

    def get_volume_number(self):
        return int(self.get_dc_identifier().split('-')[2].lstrip('0'))

    def get_publication_type(self):
        return 'student' if self.get_dc_title() in ('Cap and Gown', 'Daily Maroon') else 'university'

    def get_meta(self):
        meta = ElementTree.Element('{http://cdlib.org/xtf}meta')
        ElementTree.SubElement(meta, 'facet-sidebartitle', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'yes',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = '%s::Volume %02d' % (self.get_dc_title(), self.get_volume_number())

        ElementTree.SubElement(meta, 'facet-title', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'yes',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = '%s::Volume %02d' % (self.get_dc_title(), self.get_volume_number())

        ElementTree.SubElement(meta, 'browse-title', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'yes'
        }).text = '%s Volume %02d' % (self.get_dc_title(), self.get_volume_number())

        ElementTree.SubElement(meta, 'facet-date', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'yes',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = '%s::%s' % (self.get_decade(), self.get_year())

        ElementTree.SubElement(meta, 'browse-date', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'yes'
        }).text = '%s %s' % (self.get_decade(), self.get_year())

        ElementTree.SubElement(meta, 'range-date', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = self.get_year()

        ElementTree.SubElement(meta, 'facet-category', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'yes',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = '%s::%s' % (self.get_publication_type(), self.get_dc_title())

        ElementTree.SubElement(meta, 'browse-category', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'yes'
        }).text = self.get_publication_type()

        ElementTree.SubElement(meta, 'sort-identifier', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = self.get_dc_identifier()

        ElementTree.SubElement(meta, 'display-title', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = '%s (%s)' % (self.get_dc_title(), self.get_year_range())

        ElementTree.SubElement(meta, 'display-item', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = 'Volume %s (%s)' % (self.get_volume_number(), self.get_year())

        ElementTree.SubElement(meta, 'browse-description', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'yes'
        }).text = self.get_dc_description()

        ElementTree.SubElement(meta, 'year', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = self.get_year()

        ElementTree.SubElement(meta, 'facet-volume', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = 'Volume %d' % self.get_volume_number()

        ElementTree.SubElement(meta, 'human-readable-date', attrib={
            '{http://cdlib.org/xtf}meta': 'true',
            '{http://cdlib.org/xtf}facet': 'no',
            '{http://cdlib.org/xtf}tokenize': 'no'
        }).text = self.get_human_readable_date()

        return meta

    # End Copy-Pasted Meta Requirements

    def get_line_ocr_from_alto(self, alto):
        # Dump ALTO Data to Etree
        alto_data = ElementTree.fromstring(alto)
        # Setup our container list for the line by line OCR Data
        lines = []
        # Grab each lines data from the Alto
        for line in alto_data.findall('.//{http://www.loc.gov/standards/alto/ns-v2#}TextLine'):
            line_data = {}
            line_data['l'] = int(line.attrib["HPOS"])
            line_data['r'] = int(line.attrib["HPOS"]) + int(line.attrib['WIDTH'])
            line_data['t'] = int(line.attrib['VPOS'])
            line_data['b'] = int(line.attrib['VPOS']) + int(line.attrib['HEIGHT'])
            line_data['text'] = " ".join(
                string.attrib['CONTENT'] for string in line.findall(
                    './/{http://www.loc.gov/standards/alto/ns-v2#}String'
                )
            )

            # Spacing math
            # Uses alto "strings" within lines
            hpos_widths = []
            for string in line.findall('.//{http://www.loc.gov/standards/alto/ns-v2#}String'):
                hpos_widths.append(
                    {'hpos': int(string.attrib['HPOS']),
                     'width': int(string.attrib['WIDTH'])}
                     )
            spacing = []
            for i, x in enumerate(hpos_widths):
                # If it's the first element just grab the width
                if i == 0:
                    spacing.append(x['width'])
                # Else grab the previous space and the width
                else:
                    spacing.append(x['hpos'] - (hpos_widths[i-1]['hpos'] + hpos_widths[i-1]['width']))
                    spacing.append(x['width'])
            line_data['spacing'] = spacing

            lines.append(line_data)
        return lines

    def get_line_ocr_from_pos(pos):
        raise NotImplementedError()

    def get_leaf(self, i, d):
        leaf = ElementTree.Element("leaf")
        # Set leaf attribs
        leaf.attrib['leafNum'] = str(i)
        leaf.attrib['humanReadableLeafNum'] = str(i)
        leaf.attrib['type'] = ""
        leaf.attrib['access'] = "true"
        leaf.attrib['imgFile'] = str(i).zfill(8) + ".jpg"
        leaf.attrib['x'] = str(d['jpg_width'])
        leaf.attrib['y'] = str(d['jpg_height'])
        leaf.attrib['xtf:sectionType'] = str(i).zfill(8)
        # Cropbox Element
        cropbox = ElementTree.Element("cropBox")
        cropbox.attrib['x'] = str(d['jpg_width'])
        cropbox.attrib['y'] = str(d['jpg_height'])
        cropbox.attrib['w'] = str(d['jpg_width'])
        cropbox.attrib['h'] = str(d['jpg_height'])
        leaf.append(cropbox)
        # Line element
        x_scale = d['jpg_width'] / d['tif_width']
        y_scale = d['jpg_height'] / d['tif_height']
        if 'alto' in d:
            for line in self.get_line_ocr_from_alto(d['alto']):
                line_element = ElementTree.Element("line")
                line_element.attrib['l'] = str(round(line['l'] * x_scale))
                line_element.attrib['t'] = str(round(line['t'] * y_scale))
                line_element.attrib['r'] = str(round(line['r'] * x_scale))
                line_element.attrib['b'] = str(round(line['b'] * y_scale))
                line_element.attrib['spacing'] = " ".join(str(round(x * x_scale)) for x in line['spacing'])
                line_element.text = line['text']
                leaf.append(line_element)
        # It must be pos metadata
        else:
            for line in self.get_line_ocr_from_pos(d['pos']):
                line_element = ElementTree.Element("line")
                line_element.attrib['l'] = str(round(line['l'] * x_scale))
                line_element.attrib['t'] = str(round(line['t'] * y_scale))
                line_element.attrib['r'] = str(round(line['r'] * x_scale))
                line_element.attrib['b'] = str(round(line['b'] * y_scale))
                line_element.attrib['spacing'] = " ".join(str(round(x * x_scale)) for x in line['spacing'])
                line_element.text = line['text']
                leaf.append(line_element)
        return leaf

    def get_xtf_converted_book(self):
        root = ElementTree.Element('xtf-converted-book')
        root.append(self.get_meta())
        for i, d in enumerate(self.info_dicts):
            root.append(self.get_leaf(i+1, d))
        return ElementTree.tostring(root, encoding="UTF-8", method='xml')
