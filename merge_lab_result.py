import bisect
from typing import List, Tuple
from extract_column_data import TextPosition, separate_numbers_into_buckets

class LabResult:
    def __init__(self, label: str = '', result: float='0.0', unit: str=''):
        self.label = label
        self.result = result
        self.unit = unit


# merge text that lies in the same line basing on the y coordinate
def merge_lab_result(labels: List[TextPosition], results: List[TextPosition],units: List[TextPosition], line_word_max_deviation=10)->List[LabResult]:
    labels_results = merge_two_columns(labels, results, line_word_max_deviation)
    results_units = merge_two_columns(results, units, line_word_max_deviation)

    # now merge to the final lab result
    labelresults_idx = 0
    resultunits_idx = 0

    ret: List[LabResult] = []
    while labelresults_idx < len(labels_results):
        label, result_label = labels_results[labelresults_idx]

        while resultunits_idx < len(results_units):
            result_unit, unit = results_units[resultunits_idx]

            # if the result is common, they all are placed in the same line
            if result_label.equals(result_unit):
                ret.append(LabResult(label, result_label, unit))
                labelresults_idx += 1
                resultunits_idx += 1
                break

            # otherwise, either tuple of the other one comes first
            if result_label.y2 - result_unit.y2 < 0:
                # value from result_label comes first
                ret.append(LabResult(label, result_label, ''))
                labelresults_idx += 1
                break
            else:
                # value from result_unit comes first
                ret.append(LabResult('', result_unit, unit))
                resultunits_idx += 1
                continue




def merge_two_columns(column_before: List[TextPosition], column_after: List[TextPosition], line_word_max_deviation=10)-> List[Tuple[TextPosition, TextPosition]]:
    column_after_idx = 0
    column_before_idx = 0

    res: List[Tuple[TextPosition,TextPosition]] = []
    while column_before_idx < len(column_before):

        column_before_y = column_before[column_before_idx].y2

        while column_after_idx < len(column_after):

            column_after_y = column_after[column_after_idx].y1

            # if words are in the same line, append them together
            if abs(column_after_y - column_before_y) <= line_word_max_deviation:
                res.append((column_before[column_before_idx], column_after[column_after_idx]))
                column_before_idx += 1
                column_after_idx += 1
                break

            # if words are lying to far basing on y coordinate, they have to be added separately
            # but which one comes first?
            # y is 0 on the top of the page
            if column_after_y - column_before_y < 0:
                # value from column_after comes first
                res.append((None, column_after[column_after_idx]))
                column_after_idx += 1
                continue
            else:
                # value from column_before comes first
                res.append((column_before[column_before_idx], None))
                column_before_idx += 1
                break

    return res

