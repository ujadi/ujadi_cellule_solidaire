from odoo import models, fields, api


class LivreSyntetique(models.Model):
    _name = 'livre.syntetique'
    _description = 'Eparge, Dette du membre d\'une Cellule solidaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    part_price = fields.Integer(
        string='Valeur d\'Une Part', 
        required=True,
        help='Prix unitaire d’une part, en Franc Congolais ou en Dollar Américain.'
        ) # Prix de Part calculé en franc Congolais ou En Dollard Américain
    cycle = fields.Char(string='Cycle', tracking=True) # Cycle de l'épargne
    Durée = fields.Char(string='Durée', tracking=True) # Durée de l'épargne
    membre_id = fields.Many2one('membre.cs', string="Membre",
                                #  required=True
                                 ) # Membre de la cellule solidaire
    cellule_id = fields.Many2one('cellule.solidaire', string="Cellule Solidaire",
                                #   required=True
                                  ) # Cellule Solidaire
    nombre_part = fields.Integer(string='Nombre des Part',
        # required=True,
        tracking=True,
        help='Nombre total de parts, calculé en Franc Congolais ou en Dollar Américain.') # Nombre de Part calculé en franc Congolais ou En Dollard Américain
    montant_chiffre = fields.Integer(
        string='Montant Total en chiffre', 
        help='Montant total en chiffres, calculé comme (prix de la part U+00d7 nombre de parts).',
        store=True,
        compute='_compute_montant_chiffre'        
        )
    
    # Montant en chiffre calculé en franc Congolais ou En Dollard Américain
    # donc il viens d'épargner 2 parts cette semaine, 
    first_week = fields.Integer(string='Nombre de Part Pour La 1ère Semaine',tracking=True) # si une part_price est de 2000 FC, si le membre vient avec 4 000fc cela veut dire qu'il a 2 parts
    second_week = fields.Integer(string='Nombre de Part Pour La 2ème Semaine',tracking=True)
    third_week = fields.Integer(string='Nombre de Part Pour La 3ème Semaine',tracking=True)
    fourth_week = fields.Integer(string='Nombre de Part Pour La 4ème Semaine',tracking=True)
    total_month = fields.Integer(string='Total Mensuel Des Parts', compute='_compute_totals', store=True)
    

    first_week_amount = fields.Integer(string='Montant 1ère Semaine', compute='_compute_week_amounts', store=True)
    second_week_amount = fields.Integer(string='Montant 2ème Semaine', compute='_compute_week_amounts', store=True)
    third_week_amount = fields.Integer(string='Montant 3ème Semaine', compute='_compute_week_amounts', store=True)
    fourth_week_amount = fields.Integer(string='Montant 4ème Semaine', compute='_compute_week_amounts', store=True)

    # Total Mensuel calculé en franc Congolais ou En Dollard Américain 
    #en fonction du nombre de part ajouté chaque semaine
    debt = fields.Integer(string='Dette',tracking=True) #par defaut Calculé au double de ce que le membre a épargné dans la cellule mais il peut être modifié selon ses choix
    sign_responsable = fields.Char(string='Signature du Responsable')
    sign_membre = fields.Char(string='Signature du Membre')
    date = fields.Date(string='Date', default=fields.Date.context_today) #10% de ce que le membre emprunte à la cellule
    currency = fields.Selection([
    ('fc', 'Franc Congolais'),
    ('usd', 'Dollar Américain')
    ], string='Devise', required=True)
    membre_name = fields.Char(string="Nom du Membre", related='membre_id.name', readonly=True, store=True)

    active = fields.Boolean(string='Actif', default=True) # pour savoir si le livre est actif ou pas

    _sql_constraints = [
    ('part_price_positive', 'CHECK(part_price > 0)', 'Le prix de la part doit être strictement positif.'),
    ('nombre_part_positive', 'CHECK(nombre_part >= 0)', 'Le nombre de parts doit être positif ou nul.'),
    ('montant_chiffre_positive', 'CHECK(montant_chiffre >= 0)', 'Le montant en chiffres doit être positif ou nul.'),
    ('debt_positive', 'CHECK(debt >= 0)', 'La dette doit être positive ou nulle.'),
    ('first_week_positive', 'CHECK(first_week >= 0)', 'La première semaine doit être positive ou nulle.'),
    ('second_week_positive', 'CHECK(second_week >= 0)', 'La deuxième semaine doit être positive ou nulle.'),
    ('third_week_positive', 'CHECK(third_week >= 0)', 'La troisième semaine doit être positive ou nulle.'),
    ('fourth_week_positive', 'CHECK(fourth_week >= 0)', 'La quatrième semaine doit être positive ou nulle.'),
    ('total_month_positive', 'CHECK(total_month >= 0)', 'Le total mensuel doit être positif ou nul.'),
]
    
    state = fields.Selection([
    ('draft', 'Brouillon'),
    ('confirmed', 'Confirmé'),
    ], default='draft', string='État', tracking=True)

    def action_confirm(self):
        """Change the state to confirmed."""
        self.state = 'confirmed'

    def action_draft(self):
        """Change the state back to draft."""
        self.state = 'draft'    
    
    def action_view_membre(self):
        """Open the form view of the related member."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Membre',
            'res_model': 'membre.cs',
            'view_mode': 'form',
            'res_id': self.membre_id.id,
            'target': 'new',
        }   
    

    @api.depends('part_price', 'nombre_part')
    def _compute_montant_chiffre(self):
        """Compute the total amount in figures."""
        for record in self:
            record.montant_chiffre = record.part_price * record.nombre_part if record.part_price and record.nombre_part else 0

    @api.depends('part_price', 'first_week', 'second_week', 'third_week', 'fourth_week')
    def _compute_week_amounts(self):
        for record in self:
            record.first_week_amount = (record.first_week or 0) * (record.part_price or 0)
            record.second_week_amount = (record.second_week or 0) * (record.part_price or 0)
            record.third_week_amount = (record.third_week or 0) * (record.part_price or 0)
            record.fourth_week_amount = (record.fourth_week or 0) * (record.part_price or 0)

    @api.depends('first_week', 'second_week', 'third_week', 'fourth_week',
                 'first_week_amount', 'second_week_amount', 'third_week_amount', 'fourth_week_amount')
    def _compute_totals(self):
        for record in self:
            record.nombre_part = (record.first_week or 0) + (record.second_week or 0) + (record.third_week or 0) + (record.fourth_week or 0)
            record.total_month = record.nombre_part  # Si tu veux garder pareil
            record.montant_chiffre = (record.first_week_amount or 0) + (record.second_week_amount or 0) + (record.third_week_amount or 0) + (record.fourth_week_amount or 0)
            