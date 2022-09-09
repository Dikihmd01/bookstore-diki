from odoo import api, fields, models


class Author(models.Model):
    _name = 'bookstore.author'
    _description = 'Penulis'

    name = fields.Char(string='Nama Penulis')
    author_code = fields.Char(tring='Kode Author',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')
    
    @api.model
    def create(self, vals):
        if vals.get('author_code', 'New') == 'New':
            vals['author_code'] = self.env['ir.sequence'].next_by_code(
                'bookstore.author' or 'New'
            )
        
        result = super(Author, self).create(vals)
        return result
