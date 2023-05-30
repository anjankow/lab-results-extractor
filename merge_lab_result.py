import numpy as np
import sys
from typing import List
from extract_column_data import TextPosition

class LabResult:
    ref_value_min = ''
    ref_value_max = ''

    def __init__(self, label: TextPosition, result: TextPosition, unit: TextPosition):
        if label is None:
            self.label = ''
        else:
            self.label = label.text

        if result is None:
            self.result = None
        else:
            self.result = result.text

        if unit is None:
            self.unit = ''
        else:
            self.unit = unit.text

    def set_ref_value(self, text: str):
        if text is not None:
            if text.lstrip().startswith('<'):
                self.ref_value_max = text.split('<')[1]
            elif text.lstrip().startswith('>'):
                self.ref_value_min = text.split('>')[1]
            splitted = text.split('-', 1)
            if len(splitted) == 2:
                min, max = splitted
                self.ref_value_min = min
                self.ref_value_max = max

# a = LabResult(None, None, None)
# a.set_ref_value(' >234  ')
# print(a.ref_value_min)
# print(a.ref_value_max)

class _ColumnData:
    def __init__(self, column_data: List[TextPosition]):
        self.idx = -1
        self.column_data = column_data
        self.increment()

    def increment(self):
        if self.idx + 1 < len(self.column_data):
            self.idx += 1
        else:
            self.idx = -1

    def get(self) -> TextPosition:
        if self.idx != -1:
            return self.column_data[self.idx]
        else:
            return None

# merge text that lies in the same line basing on the y coordinate
def merge_lab_result(labels: List[TextPosition], results: List[TextPosition], units: List[TextPosition], references: List[TextPosition], max_line_deviation=10.)->List[LabResult]:
    data = [_ColumnData(labels), _ColumnData(results), _ColumnData(units)]
    if references is not None:
        data.append(_ColumnData(references))
    data_merged = merge_text_positions(data, max_line_deviation)
    res: List[LabResult] = []
    for line in data_merged:
        lab_result = LabResult(line[0], line[1], line[2])
        if len(line) > 3 and line[3] is not None:
            lab_result.set_ref_value(line[3].text)
        res.append(lab_result)

    return res

def merge_text_positions(data: List[_ColumnData], max_line_deviation: float = 10.):
    res = []

    while True:
        # get data currently pointed by indexes of each column
        current_idx_data: List[TextPosition] = []
        current_min_y = sys.maxsize

        for column in data:
            current_idx_data.append(column.get())

            if column.get() is not None:
                # check which y is the lowest -> which comes first
                current_min_y = min(current_min_y, column.get().y1)


        # break the loop is there is no data to process (all column.get() returned None)
        if current_min_y == sys.maxsize:
            break

        # start comparing, checking which data is coming first in the column or lying in the same line
        line_data = []
        previous_y = current_min_y
        for i in range(len(current_idx_data)):
            column_line = current_idx_data[i]

            # is None only if no more elements left in this column
            if column_line is None:
                line_data.append(None)
                continue

            if abs(column_line.y1 - previous_y) <= max_line_deviation:
                # lies in the same line with the previous element
                line_data.append(column_line)

                # set new previous_y
                previous_y = column_line.y1
                # data used, increment the index
                data[i].increment()
                continue
            else:
                # this column has no element in this line, append None
                line_data.append(None)
                continue

        res.append(line_data)

    return res
