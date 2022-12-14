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

    @api.ondelete(at_uninstall=False)
    def __ondelete_order(self):
        if self.orderdetails_ids:
            order = []
            for line in self:
                order = self.env['bookstore.orderdetails'].search(
                    [('order_id', '=', line.id)])

            for ob in order:
                ob.book_id.stock += ob.qty

    def write(self, vals):
        for line in self:
            old_data = self.env['bookstore.orderdetails'].search(
                [('order_id', '=', line.id)])
            print(old_data)

            for data in old_data:
                print(str(data.book_id.name) + " " +
                      str(data.qty) + ' ' + str(data.book_id.stock))
                data.book_id.stock += data.qty

        line = super(Orders, self).write(vals)

        for line in self:
            data_after_edit = self.env['bookstore.orderdetails'].search(
                [('order_id', '=', line.id)])
            print(old_data)
            print(data_after_edit)

            for new_data in data_after_edit:
                if new_data in old_data:
                    print(new_data.book_id.name + " " +
                          str(new_data.qty) + ' ' + str(new_data.book_id.stock))
                    new_data.book_id.stock -= new_data.qty
                else:
                    pass

        return line


class OrderDetails(models.Model):
    _name = 'bookstore.orderdetails'
    _description = 'Detail Pesanan'

    name = fields.Char(string='Nama')
    order_id = fields.Many2one(
        comodel_name='bookstore.orders',
        string='Pesanan')
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

    @api.model
    def create(self, vals):
        line = super(OrderDetails, self).create(vals)
        if line.qty:
            self.env['bookstore.book'].search(
                [('id', '=', line.book_id.id)]
            ).write({'stock': line.book_id.stock - line.qty})

        return line
