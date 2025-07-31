from odoo import models, fields 


class MembreCs(models.Model):
    _name = 'membre.cs'
    _description = 'Identification des membres'

    name = fields.Char(string='Nom complet', required=True)
    phone_number = fields.Char(string='Téléphone', required=True)
    sexe = fields.Selection([
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),],
    string='Gender')
    birth_day = fields.Date(string='Date de Naissance')
    email = fields.Char(string='Email')
    adress = fields.Char(string="Adresse") 
    quartier = fields.Char(string="Quartier")
    avenue = fields.Char(string="Avenue") 
    cellule_id = fields.Many2one('cellule.solidaire', string="Cellule Solidaire", ondelete='cascade')