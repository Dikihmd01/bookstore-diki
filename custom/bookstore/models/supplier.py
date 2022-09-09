from odoo import api, fields, models


class Supplier(models.Model):
    _name = 'bookstore.supplier'
    _description = 'Supplier'

    name = fields.Char(string='Nama Supplier',
                       required=True)
    supplier_code = fields.Char(String='Kode Supplier',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')
    address = fields.Char(string='Alamat')
    book_ids = fields.One2many(
        comodel_name='bookstore.book',
        inverse_name='supplier_id',
        string='Buku')

    @api.model
    def create(self, vals):
        if vals.get('supplier_code', 'New') == 'New':
            vals['supplier_code'] = self.env['ir.sequence'].next_by_code(
                'bookstore.supplier' or 'New'
            )

        result = super(Supplier, self).create(vals)
        return result
