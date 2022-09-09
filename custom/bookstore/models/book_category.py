from ast import Lambda
from unittest import result
from odoo import api, fields, models


class BookCategory(models.Model):
    _name = 'bookstore.bookcategory'
    _description = 'Kategori Buku'

    name = fields.Char(string='Nama Kategori')
    category_code = fields.Char(string='Kode Kategori',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')
    book_ids = fields.One2many(comodel_name='bookstore.book', inverse_name='category_id', string='Daftar Buku')
    
    
    
    @api.model
    def create(self, vals):
        if vals.get('category_code', 'New') == 'New':
            vals['category_code'] = self.env['ir.sequence'].next_by_code(
                'bookstore.bookcategory' or 'New'
            )
        
        result = super(BookCategory, self).create(vals)
        return result
    
