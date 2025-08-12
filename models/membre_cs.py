from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re



class MembreCs(models.Model):
    _name = 'membre.cs'
    _description = 'Identification des membres'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Noms complets', required=True, tracking=True)
    phone_number = fields.Char(string='N° Téléphone', required=True, tracking=True)
    province_id = fields.Many2one('res.province', string="Province") 
    ville = fields.Many2one(
        'res.ville.territoire',
        domain="[('province_id', '=', province_id)]",
        string="Ville/Territoire"
    )
    province_selected = fields.Boolean(string="Province choisie", compute='_compute_province_selected')
    sexe = fields.Selection([
    ('male', 'M'),
    ('female', 'F'),
    ],
    string='Sexe'
    )
    birth_day = fields.Date(string='Date de Naissance')

    age = fields.Integer(string="Âge", compute='_compute_age', store=True)
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
        readonly=True,
    )
    active = fields.Boolean(string='Actif', default=True)
    livre_ids = fields.One2many('livre.syntetique', 'membre_id', string="Livres Synthétiques")

    _sql_constraints = [
        ('phone_number_unique', 'unique(phone_number)', 'Le numéro de téléphone doit être unique.'),
        ('email_unique', 'unique(email)', 'L\'adresse email doit être unique.')
    ]

   

    @api.constrains('email')
    def _check_email_format(self):
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        for rec in self:
            if rec.email and not re.match(email_regex, rec.email):
                raise ValidationError("L'adresse email n'est pas valide.")

               

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

    @api.onchange('province_id')
    def _onchange_province_id(self):
        self.ville = False


    @api.model_create_multi
    def create(self, vals_list):
        user = self.env.user
        if user.has_group('cellule_solidaire_ujadi.group_responsable_ujadi'):
            cellule = self.env['cellule.solidaire'].search([('responsable_id.user_id', '=', user.id)], limit=1)
            if not cellule:
                raise ValidationError("Vous devez être responsable d'une cellule pour créer un membre.")
            membres_count = self.env['membre.cs'].search_count([('cellule_id', '=', cellule.id)])
            if membres_count + len(vals_list) > 30:
                raise ValidationError("Vous ne pouvez pas avoir plus de 30 membres dans votre cellule.")
            for vals in vals_list:
                vals['cellule_id'] = cellule.id
        return super(MembreCs, self).create(vals_list)


    
    def action_open_livre_syntetique(self):
        self.ensure_one()
        livre = self.env['livre.syntetique'].search([('membre_id', '=', self.id)], limit=1)
        if not livre:
            livre = self.env['livre.syntetique'].create({
                'membre_id': self.id,
                'cellule_id': self.cellule_id.id if self.cellule_id else False,
                'part_price': 2000,
                'currency': 'fc',
            })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Livre Synthétique',
            'res_model': 'livre.syntetique',
            'view_mode': 'form',
            'res_id': livre.id,
            'target': 'new',
        }
  
   


