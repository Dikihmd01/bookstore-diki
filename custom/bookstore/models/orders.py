from odoo import api, fields, models


class Orders(models.Model):
    _name = 'bookstore.orders'
    _description = 'Pesanan'

    name = fields.Char(String='No. Pemesanan',
                        readonly=True,
                        copy=False,
                        required=True,
                        default='New')
    buyer = fields.Char(string='Nama Pembeli',
                        required=True)
    employee_id = fields.Many2one(comodel_name='res.users',
                                    String='Pegawai',
                                    required=True)
    date_order = fields.Datetime(string='Tanggal Penjualan',
                                default=fields.Datetime.now())
    total = fields.Integer(string='Total Bayar',
                            compute='_compute_total')
    orderdetails_ids = fields.One2many(comodel_name='bookstore.orderdetails',
                                        inverse_name='order_id',
                                        string='Detail Order')
    

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'bookstore.orders' or 'New'
            )
        
        result = super(Orders, self).create(vals)
        return result

    @api.depends('orderdetails_ids')
    def _compute_total(self):
        for line in self:
            result = sum(self.env['bookstore.orderdetails'].search(
                [('order_id', '=', line.id)]).mapped('subtotal'))
            line.total = result

    
    
class OrderDetails(models.Model):
    _name = 'bookstore.orderdetails'
    _description = 'Detail Pesanan'

    name = fields.Char(string='Nama')
    order_id = fields.Many2one(comodel_name='bookstore.orders', string='Pesanan')
    book_id = fields.Many2one(comodel_name='bookstore.book', string='Buku')
    price_per_book = fields.Integer(string='Harga Satuan',
                                    onchange='_onchange_book_id')
    qty = fields.Integer(string='Jumlah Beli')
    subtotal = fields.Integer(string='Subtotal',
                                compute='_compute_subtotal')
    
    @api.depends('price_per_book', 'qty')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.price_per_book

    @api.onchange('book_id')
    def _onchange_book_id(self):
        if self.book_id.price:
            self.price_per_book = self.book_id.price
    
    
    
    