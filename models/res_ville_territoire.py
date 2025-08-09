from odoo import models, fields

class ResVilleTerritoire(models.Model):
    _name = 'res.ville.territoire'
    _description = 'Villes et Territoires de la RDC'
    _order = 'name'

    name = fields.Char(string='Nom de la Ville/Territoire', required=True)
    province_id = fields.Many2one('res.province', string="Province", required=True)

    _sql_constraints = [
        ('ville_territoire_name_unique', 'unique(name, province_id)', 'Le nom de la ville/territoire doit être unique par province.')
    ]

    