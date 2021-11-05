from odoo import models, fields, api
from random import randint
from odoo.exceptions import ValidationError as alert
from datetime import datetime as dt

class orderlist(models.Model):
    _name = 'pondokfamily.orderlist'
    _description = 'Database Penampung O2M OrderMenu'

    name = fields.Many2one(
        string = 'Pemesan',
        comodel_name='pondokfamily.ordermenu'
    )

    pesan = fields.Many2one(
        comodel_name='pondokfamily.menumakan',
        string='Nama Menu',
        delegate=True,
        required=True
    )

    qty = fields.Integer(
        string='Porsi',
        required=True
    )

    total = fields.Integer(
        string='Total (Rp)',
        compute='_get_total',
        store=True
    )

    jumlah_total = fields.Integer(
        string='Jumlah Rp'
    )

    desc = fields.Char(
        string='Catatan'
    )

    is_done = fields.Boolean(
        string='Done',
        default=False
    )

    @api.depends('is_done')
    @api.onchange('is_done')
    def _terjual(self):
        for al in self:
            menumakan = self.env['pondokfamily.menumakan'].search([('kode_menu','=',al.pesan.kode_menu)])
            ordermenu = self.env['pondokfamily.ordermenu'].search([('order_id','=',al.name.order_id)])
            listresep = menumakan.mapped('resep_ids')
            if al.is_done:
                menumakan.terjual += al.qty
                ordermenu.counter += 1
                # al.name['counter']+=1
                for x in listresep:
                    x.bahan['jml_stok'] -= x.qty * al.qty

                # raise alert(f'Log {al.name.counter}')

    @api.onchange('qty')
    @api.depends('qty')
    def _get_total(self):
        for al in self:
            if al.qty:
                al.total = al.pesan.harga * al.qty

    @api.onchange('pesan')
    def _pakai_bahan(self):
        bahanhabis = []
        for al in self:
            if al.pesan:
                for x in al.pesan['resep_ids']:
                    if (x.bahan.jml_stok - x.qty) <= 0:
                        bahanhabis.append([x.bahan.name,x.bahan.kode_bahan])      
        if len(bahanhabis) >= 1:
            raise alert(f'Stok Bahan {bahanhabis} Habis')

class ordermenu(models.Model):
    _name = 'pondokfamily.ordermenu'
    _description = 'Database penyimpan order makan/minum'

    name = fields.Char(
        string='Pesanan Atas Nama',
        required=True
    )

    order_id = fields.Char(
        string='ORDER ID',
        compute='_generate_order',
        store=True
    )

    tipe_order = fields.Selection(
        string="Tipe Pesanan",
        selection=[('dinein','Dine In'), ('takeaway','Take Away')]
    )

    no_meja = fields.Selection(
        string='Nomor Meja',
        selection=[('TA',''), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')],
        # default='TA'
    )
    
    hide = fields.Boolean(
        string='Hide',
        default=True,
        compute = '_setmeja'
    )

    orderlist = fields.One2many(
        string='Order List',
        comodel_name='pondokfamily.orderlist',
        inverse_name='name'
    )

    status = fields.Selection(
        string='Status',
        selection=[('antri', 'On Queue'), ('proses', 'On Proccess'), ('done','Done')],
        # default='antri'
    )

    counter = fields.Integer(
        string='Tersaji'
    )    

    tgl_beli = fields.Datetime(
        string = 'Tanggal Order',
        default = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    @api.onchange('tipe_order')
    def _setmeja(self):
        for al in self:
            if al.tipe_order:
                if al.tipe_order == 'takeaway':
                    al.hide = True
                    al.no_meja = 'TA'
                else :
                    al.hide = False


    @api.onchange('orderlist')
    def _seto2m(self):
        count = 0
        for al in self:
            if al.orderlist:
                for x in al.orderlist:
                    if x.is_done:
                        count+=1
            al.counter = count

    @api.onchange('counter')
    def _ubahstatus(self):
        for al in self:
            if al.counter:
                if al.counter >= len(al.orderlist)  :
                    al.status = 'done'
                elif al.counter <= 0:
                    al.status = 'antri'
                else:
                    al.status = 'proses'

    @api.onchange('no_meja')
    @api.depends('no_meja')
    def _generate_order(self):
        for al in self:
            if al.no_meja:
                while True:
                    randomid = str(f'PF{al.no_meja}-{randint(10000,99999)}')
                    check = self.env['pondokfamily.ordermenu'].search([('order_id','=',randomid)])
                    if len(check) <= 1:
                        al.order_id = randomid
                        break