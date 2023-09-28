from openpyxl import Workbook


def create_report_sheet(data):
    wb = Workbook()
    wb.remove_sheet(wb.active)

    for obj in data:
        try:
            ws = wb[obj['model']]
        except KeyError:
            ws = wb.create_sheet(obj['model'], 0)
            ws.append(['Модель', 'Версия', 'Количество за неделю'])
        ws.append([obj['model'], obj['version'], obj['count']])

    return wb
