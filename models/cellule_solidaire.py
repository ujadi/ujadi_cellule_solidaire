from odoo import models, fields, api
from odoo.exceptions import ValidationError



class CelluleSolidaire(models.Model):
    _name = 'cellule.solidaire'
    _description = 'Suivis des activités de la cellule solidaire de l\'ong Ujadi'


    name = fields.Char(string='Dénomination de la CS', required=True)
    province_id = fields.Many2one('res.province', string="Province", required=True)
    entity = fields.Char(string='Entité')
    responsable_id = fields.Many2one('responsable.cs', string="Responsable")
    membre_ids = fields.One2many('membre.cs', 'cellule_id', string="Membres")
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ])
    # membre_count = fields.Integer(string="Nombre de membres", compute='_compute_membre_count')


    @api.constrains('membre_ids')  # ✅ 'constrains' avec un S, sans T
    def _check_membre_count(self):
        for rec in self:
            if len(rec.membre_ids) > 30:
                raise ValidationError("Une cellule solidaire ne peut pas avoir plus de 30 membres.")
