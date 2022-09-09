from odoo import api, fields, models


class Book(models.Model):
    _name = 'bookstore.book'
    _description = 'Daftar Buku'

    name = fields.Char(string='Judul Buku')
    book_code = fields.Char(string='Kode Buku',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')
    category_id = fields.Many2one(comodel_name='bookstore.bookcategory', 
                                    string='Kategori',
                                    ondelete='cascade',
                                    required=True)
    total_page = fields.Integer(string='Total Halaman')
    price = fields.Integer(string='Harga',
                            required=True)
    stock = fields.Integer(string='Stok')

    @api.model
    def create(self, vals):
        if vals.get('book_code', 'New') == 'New':
            vals['book_code'] = self.env['ir.sequence'].next_by_code(
                'bookstore.book' or 'New'
            )
        
        result = super(Book, self).create(vals)
        return result
    
    
    
    
