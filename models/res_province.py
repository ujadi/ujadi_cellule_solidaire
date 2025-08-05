from odoo import models, fields

class ResProvince(models.Model):
    _name = 'res.province'
    _description = 'Les Province et de la RDC'
    _order = 'name'

    name = fields.Char(string='Nom de la Province', required=True, unique=True)
