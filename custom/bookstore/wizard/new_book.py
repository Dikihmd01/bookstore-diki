from odoo import api, fields, models


class NewBook(models.Model):
    _name = 'bookstore.newbook'
    _description = 'New Book'

    book_id = fields.Many2one(comodel_name='bookstore.book',
                                string='Judul Buku',
                                required=True)
    qty = fields.Integer(string='Jumlah')

        
    def button_new_book(self):
        for line in self:
            self.env['bookstore.book'].search([('id', '=', line.book_id.id)]).write(
                {'stock': line.book_id.stock +  line.qty}
            )