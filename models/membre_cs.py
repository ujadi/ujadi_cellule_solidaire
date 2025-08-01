from odoo import models, fields 


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
    province = fields.Selection([
        ('nord-kivu', 'Nord Kivu'),
        ('sud-kivu', 'Sud Kivu'),
        ('maniema', 'Maniema'),
        ('kinshasa', 'Kinshasa'),
        ('haut-katanga', 'Haut-Katanga'),
        ('lualaba', 'Lualaba'),
        ('sud-kivu', 'Sud-Kivu'),
        ('tshopo', 'Tshopo'),
        ('haut-lomami', 'Haut-Lomami'),
        ('kasai', 'Kasaï'),
        ('kasai-central', 'Kasaï Central'),
        ('kasai-oriental', 'Kasaï Oriental'),
        ('kwango', 'Kwango'),
        ('kwilu', 'Kwilu'),
        ('maindombe', 'Maï-Ndombe'),
        ('mongala', 'Mongala'),
        ('nord-ubangi', 'Nord-Ubangi'),
        ('sud-ubangi', 'Sud-Ubangi'),
        ('tshuapa', 'Tshuapa'),
        ('haut-lomami', 'Haut-Lomami'),
        ('lualaba', 'Lualaba'),
        ('maniema', 'Maniema'),
        ('sankuru', 'Sankuru'),
        ('ituri', 'Ituri'),
        ('haut-katanga', 'Haut-Katanga'),
    ], string='Province')   
    ville = fields.Char(string="Ville/Territoire")
    commune = fields.Char(string="Commune/Chefferie")
    quartier = fields.Char(string="Quartier/Groupement")
    avenue = fields.Char(string="Avenue/Village") 
    email = fields.Char(string='Email')
    cellule_id = fields.Many2one('cellule.solidaire', string="Cellule Solidaire", ondelete='cascade')
    photo = fields.Image(string="Photo")
