from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResponsableCs(models.Model):
    _name = 'responsable.cs'
    _description = 'Responsable Cellule Solidaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Nom du responsable",
        required=True
        
        )
    phone = fields.Char(string="Téléphone", required=True)
    sexe = fields.Selection([
    ('male', 'M'),
    ('female', 'F'),
    ],
    string='Sexe')
    
    province_id = fields.Many2one('res.province', string="Province",tracking=True)
    cellule_ids = fields.One2many('cellule.solidaire', 'responsable_id', string="Cellules",tracking=True)  # Corrected to match the new model name
    user_id = fields.Many2one('res.users', string='Responsable', required=True, tracking=True)
    email = fields.Char(string="Email")
    quartier = fields.Char(string="Quartier")  
    avenue = fields.Char(string="Avenue")  
    photo = fields.Image(string="Photo Passeport")  
    photo_identity = fields.Image(string="Photo d'identité")
    active = fields.Boolean(string='Actif', default=True)  


  
    # Add a one-to-many relationship to CelluleSolidaire
    # This assumes that the 'cellule.solidaire' model has a field 'responsable_id'
    # that links back to this model.
    # If the field name in 'cellule.solidaire' is different, adjust accordingly.
    # Note: The field 'cellule_ids' is used to link multiple cellules to a responsable.
    # If a responsable can only be linked to one cellule, use Many2one instead.
    # If you want to restrict deletion of a responsable if they are linked to cellules,
    # you can set ondelete='restrict' in the Many2one field in 'cellule.solidaire'.
    # If you want to allow deletion, you can set ondelete='set null' or ondelete='cascade'.
    # Here, we assume that a responsable can be linked to multiple cellules.
    # If you want to restrict deletion of a responsable if they are linked to cellules,
    # you can set ondelete='restrict' in the Many2one field in 'cellule.solidaire'.
    # If you want to allow deletion, you can set ondelete='set null' or ondelete='cascade'.
    # Here, we assume that a responsable can be linked to multiple cellules.        