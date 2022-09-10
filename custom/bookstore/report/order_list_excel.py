from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.bookstore.report_orders_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    tgl_laporan = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, order_data):
        # One sheet by partner
        sheet = workbook.add_worksheet('Daftar Order')
        # Menambahkan informasi tanggal laporan
        sheet.write(0, 0, str(self.tgl_laporan))
        sheet.write(1, 0, 'No. Order')
        sheet.write(1, 1, 'Nama Pembeli')
        sheet.write(1, 2, 'Tanggal Pembelian')
        sheet.write(1, 3, 'Total Bayar')
        
        row = 2
        col = 0
        for obj in order_data:
            col = 0
            # Text style bold, jjika tidak perlu bisa dihapus
            # bold = workbook.add_format({'bold': True})

            # write(row, col, title, style)
            # style bersifat opsional
            # sheet.write(0, 0, obj.name, bold)
            sheet.write(row, col, obj.name)
            sheet.write(row, col + 1, obj.buyer)
            sheet.write(row, col + 2, str(obj.date_order))
            sheet.write(row, col + 3, obj.total)

            # for item in obj.barang_id:
            #     sheet.write(row, col + 3, item.name)
            #     col += 1
            row += 1