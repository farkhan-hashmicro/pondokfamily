from odoo import models, fields, api
from odoo.exceptions import ValidationError as alert

class restokbahan(models.Model):
    _name = 'pondokfamily.restokbahan'
    _description = 'History Pembelian Bahan Dasar'

    name = fields.Char(
        string = 'Kode Nota',
        required=True
    )

    nama_bahan = fields.Many2one(
        comodel_name='pondokfamily.bahandasar',
        string = 'Nama Bahan',
        delegate=True,
        required=True
    )

    restok = fields.Float(
        string = 'Banyak',
        required=True
    )

    satuan = fields.Char(
        string = 'Satuan',
        compute = '_get_satuan'
    )

    penyetok = fields.Char(
        string = 'Nama Toko Penyetok'
    )

    verif = fields.Boolean(
        string = 'Verified',
        default = False
    )

    @api.constrains('name')
    def _is_exist(self):
        for rec in self:
            result = self.env['pondokfamily.restokbahan'].search([('name','=',rec.name)])
            if len(result) > 1:
                raise alert(f'Kode Nota {rec.name} sudah ada, input data lainnya')
            if rec.verif == False:
                if rec.nama_bahan['satuan_stok'] != 'pcs':
                    result.jml_stok += rec.restok*result.per_kg
                else:
                    result.jml_stok += rec.restok

            rec.verif = True
                

    @api.onchange('restok')
    def _get_satuan(self):
        for rec in self:
            if rec.nama_bahan:
                satuan = str(rec.nama_bahan['satuan_stok'])
                # raise alert(f'log : {satuan}')
                rec.satuan = satuan
