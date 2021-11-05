from odoo import models, fields, api
from odoo.exceptions import ValidationError as alert

class resepmakan(models.Model):
    _name = 'pondokfamily.resep'
    _description = 'Daftar Bahan Terpakai Untuk Resep'

    name = fields.Many2one(
        string='Nama Menu',
        comodel_name='pondokfamily.menumakan',
        delegate=True,
        required=True
    )

    bahan = fields.Many2one(
        string='Nama Bahan',
        comodel_name='pondokfamily.bahandasar',
        delegate=True,
        required=True
    )

    satuan = fields.Selection(
        string='Satuan',
        selection=[('gr', 'Gram'), ('buah', 'Buah')]
    )

    qty = fields.Float(
        string='Jumlah',
        required=True
    )

    @api.constrains('bahan')
    def _set_stock(self):
        for rec in self:
            if rec.bahan:
                check = self.env['pondokfamily.resep'].search([('bahan.kode_bahan','=',rec.bahan['kode_bahan'])])
                if len(check) > 1:
                    raise alert(f'Tidak Boleh Ada Bahan Yang Sama')


class menumakan(models.Model):
    _name = 'pondokfamily.menumakan'
    _description = 'Daftar Menu Makanan / Minuman'

    name = fields.Char(
        string='Nama Menu',
        required = True
    )

    kode_menu = fields.Char(
        string='Kode Menu',
        required=True
    )
    
    jenis_menu = fields.Selection(
        string='Jenis Menu',
        selection=[('makan', 'Makanan'), ('minum', 'Minuman')],
        required=True
    )

    harga = fields.Integer(
        string='Harga (Rp)',
        required=True,
        default=0
    )

    star = fields.Boolean(
        string='Favorit',
        default=False
    )

    terjual = fields.Integer(
        string='Terjual',
        default=0
    )

    catatan = fields.Char(
        string='Catatan'
    )

    resep_ids = fields.One2many(
        string='Resep',
        comodel_name='pondokfamily.resep',
        inverse_name='name'
    )
    
    @api.constrains('kode_menu')
    def _unique_kode(self):
        for al in self:
            check = self.env['pondokfamily.menumakan'].search([('kode_menu','=',al.kode_menu)])
            if len(check) > 1:
                raise alert(f'Kode Menu {al.kode_menu} Sudah Ada, Masukkan Kode Lain!')

    @api.depends('terjual')
    @api.onchange('terjual')
    def _favorite(self):
        for al in self:
            if al.terjual >= 50:
                al.star = True
