from odoo import models, fields, api


class LivreSyntetique(models.Model):
    _name = 'livre.syntetique'
    _description = 'Eparge, Dette du membre d\'une Cellule solidaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    
    cycle = fields.Char(string='Cycle', tracking=True) # Cycle de l'épargne
    Durée = fields.Char(string='Durée', tracking=True) # Durée de l'épargne
    membre_id = fields.Many2one('membre.cs', string="Membre",required=True) 
    cellule_id = fields.Many2one('cellule.solidaire', string="Cellule Solidaire",required=True) # Cellule Solidaire
    nombre_part = fields.Integer(string='Nombre des Part', required=True, tracking=True,
        help='Nombre total de parts, calculé en Franc Congolais ou en Dollar Américain.') # Nombre de Part calculé en franc Congolais ou En Dollard Américain
    

    # --- Valeurs des parts par semaines
    part_price_first_week = fields.Integer(string='Prix de la Part 1ère Semaine', required=True, tracking=True, help='Prix de la part pour la première semaine')
    part_price_second_week = fields.Integer(string='Prix de la Part 2ème Semaine', required=True, tracking=True, help='Prix de la part pour la deuxième semaine')
    part_price_third_week = fields.Integer(string='Prix de la Part 3ème Semaine', required=True, tracking=True, help='Prix de la part pour la troisième semaine')
    part_price_fourth_week = fields.Integer(string='Prix de la Part 4ème Semaine', required=True, tracking=True, help='Prix de la part pour la quatrième semaine')

    # Montant en chiffre calculé en franc Congolais ou En Dollard Américain
    # donc il viens d'épargner 2 parts cette semaine, 
    first_week = fields.Integer(string='Nombre de Part Pour La 1ère Semaine',tracking=True) # si une part_price est de 2000 FC, si le membre vient avec 4 000fc cela veut dire qu'il a 2 parts
    second_week = fields.Integer(string='Nombre de Part Pour La 2ème Semaine',tracking=True)
    third_week = fields.Integer(string='Nombre de Part Pour La 3ème Semaine',tracking=True)
    fourth_week = fields.Integer(string='Nombre de Part Pour La 4ème Semaine',tracking=True)
    
    

    first_week_amount = fields.Integer(string='Montant 1ère Semaine', compute='_compute_week_amounts', store=True)
    second_week_amount = fields.Integer(string='Montant 2ème Semaine', compute='_compute_week_amounts', store=True)
    third_week_amount = fields.Integer(string='Montant 3ème Semaine', compute='_compute_week_amounts', store=True)
    fourth_week_amount = fields.Integer(string='Montant 4ème Semaine', compute='_compute_week_amounts', store=True)

    # --- Totaux ---
    montant_chiffre = fields.Integer(string='Montant Total en chiffre', help='Montant total en chiffres, calculé comme (prix de la part U+00d7 nombre de parts).',store=True,compute='_compute_montant_chiffre')
    total_month = fields.Integer(string='Total Mensuel Des Parts', compute='_compute_totals', store=True)

    #--- Gestion social ---
    social = fields.Integer(string="Social", help="Montant social à payer par chaque semaine", default=1000) 
    social_debt = fields.Integer(string="Dette Sociale", help="Montant social à payer par le membre", default=0,readonly=True)


    #--- Signature et workflow ---
    digital_signature = fields.Binary(string='Empreinte Digitale du membre', help='Signature numérique du membre pour valider l\'épargne')
    justificatif = fields.Binary(string='Pièce Justificatif (reçu)', help='Justificatif de l\'épargne, peut être une image ou un document')
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('responsable', 'Saisi par Responsable'),
        ('validated', 'Validé par Membre'),
        ('supervised', 'Validé par le superici'),
        ('validated', 'Validé'),
        ('done', 'Terminé'),
        ('cancelled', 'Annulé'),
    ], default='draft', string='State', tracking=True)
    debt = fields.Integer(string='Dette',tracking=True) #par defaut Calculé au double de ce que le membre a épargné dans la cellule mais il peut être modifié selon ses choix
    sign_responsable = fields.Char(string='Signature du Responsable')
    sign_membre = fields.Char(string='Signature du Membre')
    date = fields.Date(string='Date', default=fields.Date.context_today) #10% de ce que le membre emprunte à la cellule
    currency = fields.Selection([
    ('fc', 'Franc Congolais'),
    ('usd', 'Dollar Américain')
    ], string='Devise', required=True)
    membre_name = fields.Char(string="Nom du Membre", related='membre_id.name', readonly=True, store=True)
    cellule_solidaire_name = fields.Char(string="Nom de la Cellule Solidaire", related='cellule_id.name', readonly=True, store=True)
    photo_passport = fields.Binary(string='Photo du Membre', related="membre_id.photo", help='Photo du membre pour identification')
    respo_name = fields.Char(string="Nom du Responsable", related='cellule_id.responsable_id.name', readonly=True, store=True)
    
    active = fields.Boolean(string='Actif', default=True)
    compte_epargne_id = fields.Many2one('compte.epargne', string="Compte Épargne", readonly=True)
    _sql_constraints = [
    ('montant_chiffre_positive', 'CHECK(montant_chiffre >= 0)', 'Le montant en chiffres doit être positif ou nul.'),
    ('debt_positive', 'CHECK(debt >= 0)', 'La dette doit être positive ou nulle.'),
    ('first_week_positive', 'CHECK(first_week >= 0)', 'La première semaine doit être positive ou nulle.'),
    ('second_week_positive', 'CHECK(second_week >= 0)', 'La deuxième semaine doit être positive ou nulle.'),
    ('third_week_positive', 'CHECK(third_week >= 0)', 'La troisième semaine doit être positive ou nulle.'),
    ('fourth_week_positive', 'CHECK(fourth_week >= 0)', 'La quatrième semaine doit être positive ou nulle.'),
    ('total_month_positive', 'CHECK(total_month >= 0)', 'Le total mensuel doit être positif ou nul.'),
]
    

     # --- Compute ---
    @api.depends('first_week', 'second_week', 'third_week', 'fourth_week',
                 'part_price_first_week', 'part_price_second_week',
                 'part_price_third_week', 'part_price_fourth_week')
    def _compute_week_amounts(self):
        for rec in self:
            rec.first_week_amount = (rec.first_week or 0) * (rec.part_price_first_week or 0)
            rec.second_week_amount = (rec.second_week or 0) * (rec.part_price_second_week or 0)
            rec.third_week_amount = (rec.third_week or 0) * (rec.part_price_third_week or 0)
            rec.fourth_week_amount = (rec.fourth_week or 0) * (rec.part_price_fourth_week or 0)

    @api.depends('first_week_amount', 'second_week_amount', 'third_week_amount', 'fourth_week_amount')
    def _compute_totals(self):
        for rec in self:
            rec.total_month = (rec.first_week or 0) + (rec.second_week or 0) + (rec.third_week or 0) + (rec.fourth_week or 0)
            rec.montant_chiffre = (rec.first_week_amount or 0) + (rec.second_week_amount or 0) + (rec.third_week_amount or 0) + (rec.fourth_week_amount or 0)

    @api.depends('first_week_amount', 'second_week_amount', 'third_week_amount', 'fourth_week_amount')
    def _compute_totals(self):
        for rec in self:
            rec.total_month = (rec.first_week or 0) + (rec.second_week or 0) + (rec.third_week or 0) + (rec.fourth_week or 0)
            rec.montant_chiffre = (rec.first_week_amount or 0) + (rec.second_week_amount or 0) + (rec.third_week_amount or 0) + (rec.fourth_week_amount or 0)

    # --- Workflow ---
    def action_responsable(self):
        self.state = "responsable"

    def action_validate_member(self):
        if not self.digital_signature:
            raise ValueError("Le membre doit valider avec son empreinte digitale.")
        self.state = "validated"

    def action_supervise(self):
        if not self.justificatif:
            raise ValueError("Le superviseur doit vérifier la pièce justificative.")
        self.state = "supervised"
    

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
    

    # @api.depends('part_price', 'nombre_part')
    # def _compute_montant_chiffre(self):
    #     """Compute the total amount in figures."""
    #     for record in self:
    #         record.montant_chiffre = record.part_price * record.nombre_part if record.part_price and record.nombre_part else 0

    # @api.depends('part_price', 'first_week', 'second_week', 'third_week', 'fourth_week')
    # def _compute_week_amounts(self):
    #     for record in self:
    #         record.first_week_amount = (record.first_week or 0) * (record.part_price or 0)
    #         record.second_week_amount = (record.second_week or 0) * (record.part_price or 0)
    #         record.third_week_amount = (record.third_week or 0) * (record.part_price or 0)
    #         record.fourth_week_amount = (record.fourth_week or 0) * (record.part_price or 0)

    @api.depends('first_week', 'second_week', 'third_week', 'fourth_week',
                 'first_week_amount', 'second_week_amount', 'third_week_amount', 'fourth_week_amount')
    def _compute_totals(self):
        for record in self:
            record.nombre_part = (record.first_week or 0) + (record.second_week or 0) + (record.third_week or 0) + (record.fourth_week or 0)
            record.total_month = record.nombre_part  # Si tu veux garder pareil
            record.montant_chiffre = (record.first_week_amount or 0) + (record.second_week_amount or 0) + (record.third_week_amount or 0) + (record.fourth_week_amount or 0)
            

    # @api.onchange('first_week', 'second_week', 'third_week', 'fourth_week')
    # def _update_social_debt(self):
    #     """Update the social debt based on the number of parts."""
    #     for record in self:
    #         if record.fir