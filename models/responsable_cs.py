from odoo import models, fields

class ResponsableCs(models.Model):
    _name = 'responsable.cs'
    _description = 'Responsable Cellule Solidaire'

    name = fields.Char(string="Nom du responsable", required=True)
    phone = fields.Char(string="Téléphone", required=True)
    sexe = fields.Selection([
    ('male', 'M'),
    ('female', 'F'),
    ('other', 'Other'),],
    string='Genre')
   
    email = fields.Char(string="Email")
    quartier = fields.Char(string="Quartier")  
    avenue = fields.Char(string="Avenue")  
    photo = fields.Image(string="Photo")  
    cellule_ids = fields.One2many('cellule.solidaire', 'responsable_id', string="Cellules")  # Corrected to match the new model name
    active = fields.Boolean(string='Actif', default=True)  