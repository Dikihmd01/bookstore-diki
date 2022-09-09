from ast import Lambda
from unittest import result
from odoo import api, fields, models


class BookCategory(models.Model):
    _name = 'bookstore.bookcategory'
    _description = 'Kategori Buku'

    name = fields.Char(string='Kode Kategori Buku',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')
    category_name = fields.Char(string='Nama Kategori')
    
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'bookstore.bookcategory' or 'New'
            )
        
        result = super(BookCategory, self).create(vals)
        return result
    
