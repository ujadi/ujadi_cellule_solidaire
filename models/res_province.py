from odoo import models, fields

class ResProvince(models.Model):
    _name = 'res.province'
    _description = 'Les Province et de la RDC'
    _order = 'name'

    name = fields.Char(string='Nom de la Province', required=False)

    _sql_constraints = [
    ('province_name_unique', 'unique(name)', 'Le nom de la province doit être unique.')
]
