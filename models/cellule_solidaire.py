from odoo import models, fields



class CelluleSolidaire(models.Model):
    _name = 'cellule.solidaire'
    _description = 'Suivis des activités de la cellule solidaire de l\'ong Ujadi'


    name = fields.Char(string='Dénomination de la CS', required=True)
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


