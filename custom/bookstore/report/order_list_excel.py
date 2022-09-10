from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.bookstore.report_orders_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    date_report = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, order_data):
        sheet = workbook.add_worksheet('Daftar Order')
        sheet.write(0, 0, str(self.date_report))
        sheet.write(1, 0, 'No. Order')
        sheet.write(1, 1, 'Nama Pembeli')
        sheet.write(1, 2, 'Tanggal Pembelian')
        sheet.write(1, 3, 'Total Bayar')

        row = 2
        col = 0
        for obj in order_data:
            col = 0
            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.buyer)
            sheet.write(row, col + 2, str(obj.date_order))
            sheet.write(row, col + 3, obj.total)
            row += 1
