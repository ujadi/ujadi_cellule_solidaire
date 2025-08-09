from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date



class MembreCs(models.Model):
    _name = 'membre.cs'
    _description = 'Identification des membres'

    name = fields.Char(string='Noms complets', required=True)
    phone_number = fields.Char(string='N° Téléphone', required=True)
    province_id = fields.Many2one('res.province', string="Province") 
    province_selected = fields.Boolean(string="Province choisie", compute='_compute_province_selected')
    sexe = fields.Selection([
    ('male', 'M'),
    ('female', 'F'),
    ],
    string='Sexe'
    )
    birth_day = fields.Date(string='Date de Naissance')

    age = fields.Integer(string="Âge", compute='_compute_age', store=True)
    ville = fields.Many2one(
        'res.ville.territoire',
        domain="[('province_id', '=', province_id)]",
        string="Ville/Territoire"
    )
    commune = fields.Char(string="Commune/Chefferie")
    quartier = fields.Char(string="Quartier/Groupement")
    avenue = fields.Char(string="Avenue/Village") 
    email = fields.Char(string='Email')
    cellule_id = fields.Many2one('cellule.solidaire', string="Cellule Solidaire", ondelete='restrict')
    photo = fields.Image(string="Photo passeport")
    photo_identity = fields.Image(string="Photo d'identité")
    user_id = fields.Many2one(
        'res.users', 
        string="Utilisateur lié",
        default=lambda self: self.env.user,
    )
    active = fields.Boolean(string='Actif', default=True)

    _sql_constraints = [
        ('phone_number_unique', 'unique(phone_number)', 'Le numéro de téléphone doit être unique.'),
        ('email_unique', 'unique(email)', 'L\'adresse email doit être unique.')
    ]


    @api.constrains('email')
    def _check_email_format(self):
        for rec in self:
            if rec.email and '@' not in rec.email:
                raise ValidationError("L'adresse email doit contenir un '@'.")
            
                

    @api.depends('birth_day')
    def _compute_age(self):
        for record in self:
            if record.birth_day:
                today = date.today()
                born = record.birth_day
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                record.age = age
            else:
                record.age = 0
    @api.depends('province_id')
    def _compute_province_selected(self):
        for rec in self:
            rec.province_selected = bool(rec.province_id)
   


