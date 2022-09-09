from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BookCategory(models.Model):
    _name = 'bookstore.bookcategory'
    _description = 'Kategori Buku'

    CHOICES = [
        ('antropologi', 'Antropologi'),
        ('astronomi', 'Astronomi'),
        ('biografi', 'Biografi'),
        ('bisnis', 'Bisnis'),
        ('ekonomi', 'Ekonomi'),
        ('etika', 'Etika'),
        ('fiksi', 'Fiksi'),
        ('komputer', 'Komputer'),
        ('masak', 'Masak'),
        ('medis', 'Medis'),
        ('musik', 'Musik'),
        ('pemasaran', 'Pemasaran'),
        ('pengembangan_diri', 'Pengembangan Diri'),
        ('psikologi', 'Psikologi'),
        ('sasrtra', 'Sastra'),
        ('sejarah', 'Sejarah'),
        ('sosiologi', 'Sosiologi'),
        ('dongeng', 'Dongeng'),
        ('fotografi', 'Fotografi'),
        ('nonfiksi', 'Nonfiksi'),
    ]

    name = fields.Selection(string='Nama Kategori',
                            selection=CHOICES,
                            required=True)
    category_code = fields.Char(string='Kode Kategori',
                                readonly=True,
                                copy=False,
                                required=True,
                                default='New')
    book_ids = fields.One2many(comodel_name='bookstore.book',
                               inverse_name='category_id',
                               string='Daftar Buku',
                               required=True)

    @api.constrains('name')
    def check_unique_name(self):
        count = self.search_count(
            [('name', '=', self.name), ('id', '!=', self.id)])
        if count > 0:
            raise ValidationError(
                'Kategori {} sudah ada di Database!'.format(
                    self.name))

    @api.model
    def create(self, vals):
        if vals.get('category_code', 'New') == 'New':
            vals['category_code'] = self.env['ir.sequence'].next_by_code(
                'bookstore.bookcategory' or 'New'
            )

        result = super(BookCategory, self).create(vals)
        return result
