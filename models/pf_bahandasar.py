from odoo import models, fields, api
from odoo.exceptions import ValidationError as alert

class bahandasar(models.Model):
    _name = 'pondokfamily.bahandasar'
    _description = 'Database Bahan Dasar Makanan'
    

    name = fields.Char(
        string='Nama Bahan',
        required=True
    )
    
    kode_bahan = fields.Char(
        string='Kode Bahan',
        required=True
    )

    jenis_bahan = fields.Selection(
        string='Untuk',
        selection=[('makan', 'Makanan'), ('minum', 'Minuman')],
        required = True
    )

    jml_stok = fields.Float(
        string='Stok Bahan (buah)',
        default=0,
        required=True
    )

    satuan_stok = fields.Selection(
        string='Satuan',
        selection=[('kg', 'Kg'), ('renteng','Renteng') ,('pcs', 'Buah')],
        default='pcs',
        required=True
    )

    hide = fields.Boolean(
        string='Hide',
        default=True,
        compute = '_setperkg'
    )


    restok_bahan = fields.One2many(
        comodel_name='pondokfamily.restokbahan',
        inverse_name='nama_bahan'
    )

    per_kg = fields.Float(
        string='Jumlah pcs per-kg / per-renteng',
        default=0,
        required=True
    )

    catatan = fields.Char(
        string = 'Catatan'
    )

    @api.constrains('kode_bahan')
    def _is_duplicate(self):
        for rec in self:
            result = self.env['pondokfamily.bahandasar'].search([('kode_bahan','=',rec.kode_bahan)])
            if len(result)>1:
                raise alert(f'Data Gagal diinput, Bahan {rec.kode_bahan} ({rec.name}) sudah ada!')

    @api.onchange('satuan_stok')
    def _setperkg(self):
        for al in self:
            if al.satuan_stok:
                if al.satuan_stok != 'pcs':
                    al.hide = False
                    # al.no_meja = 'TA'
                else :
                    al.hide = True
