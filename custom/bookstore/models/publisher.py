from odoo import api, fields, models


class Publisher(models.Model):
    _name = 'bookstore.publisher'
    _description = 'Daftar Penerbit'

    name = fields.Char(string='Nama Penerbit')
    publisher_code = fields.Char(string='Kode Penerbit',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')

    @api.model
    def create(self, vals):
        if vals.get('publisher_code', 'New') == 'New':
            vals['publisher_code'] = self.env['ir.sequence'].next_by_code(
                'bookstore.publisher' or 'New'
            )
        
        result = super(Publisher, self).create(vals)
        return result
    
