from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MembreCs(models.Model):
    _name = 'membre.cs'
    _description = 'Identification des membres'

    name = fields.Char(string='Noms complets', required=True)
    phone_number = fields.Char(string='N° Téléphone', required=True)
    sexe = fields.Selection([
    ('male', 'M'),
    ('female', 'F'),
    ],
    string='Sexe')
    birth_day = fields.Date(string='Date de Naissance')
    province_id = fields.Many2one('res.province', string="Province", required=True)  
    ville = fields.Char(string="Ville/Territoire")
    commune = fields.Char(string="Commune/Chefferie")
    quartier = fields.Char(string="Quartier/Groupement")
    avenue = fields.Char(string="Avenue/Village") 
    email = fields.Char(string='Email')
    cellule_id = fields.Many2one('cellule.solidaire', string="Cellule Solidaire", ondelete='restrict')
    photo = fields.Image(string="Photo")



    @api.constrains('phone_number')
    def _check_phone_number(self):
        for rec in self:
            if len(rec.phone_number) < 9 or len(rec.phone_number) > 12:
                raise ValidationError("Le numéro de téléphone doit comporter entre 9 et 15 chiffres.")
            
    @api.constrains('email')
    def _check_email_format(self):
        for rec in self:
            if rec.email and '@' not in rec.email:
                raise ValidationError("L'adresse email doit contenir un '@'.")

    @api.constrains('name')
    def _check_name_length(self):
        for rec in self:
            if len(rec.name) < 3:
                raise ValidationError("Le nom complet doit comporter au moins 3 caractères.")
            
    @api.constrains('birth_day')
    def _check_birth_day(self):
        for rec in self:
            if rec.birth_day and rec.birth_day > fields.Date.today():
                raise ValidationError("La date de naissance ne peut pas être dans le futur.")
            
    @api.constrains('cellule_id')
    def _check_cellule_membership(self):
        for membre in self:
            if membre.cellule_id:
                existing = self.search([
                    ('id', '!=', membre.id),
                    ('cellule_id', '=', membre.cellule_id.id)
                    ])
                if existing:
                    raise ValidationError("Ce membre est déjà assigné à une cellule.")
