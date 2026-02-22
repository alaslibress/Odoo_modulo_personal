# -*- coding: utf-8 -*-
from odoo import models, fields, api


# =====================================================
# MODELO 1: PELICULAS (videoclub.pelis)
# Tarea 4 - Parte 1: modelo principal con campos basicos
# =====================================================
class videoclub_pelis(models.Model):
    # Atributos del modelo
    _name = 'videoclub.pelis'
    _description = 'Pelicula'

    # ---- Campos basicos ----
    titulo = fields.Char(
        'Titulo', size=30, required=True,
        help='Nombre de la pelicula'
    )
    director = fields.Char(
        'Director', size=30, required=False,
        help='Director de la pelicula', default=''
    )
    clasificacion = fields.Selection(
        [
            ('TP', 'Todos los Publicos'),
            ('men12', 'Menores de 12 anios'),
            ('may18', 'Mayores 18 anios'),
        ],
        string='Clasificacion',
        default='TP'
    )
    presupuesto = fields.Integer()
    fechaestreno = fields.Date()

    # ---- Campo imagen ----
    foto = fields.Binary(string='Foto')

    # ---- Campos calculados ----
    # Subvencion: 30% del presupuesto (se calcula al guardar)
    subvencionado = fields.Integer(
        compute='_valor_subvencion',
        string='Subvencionado',
    )
    # Inversion: 70% del presupuesto (se calcula de forma inmediata)
    invertido = fields.Integer(
        compute='_valor_inversion',
        string='Invertido',
    )
    # Millonario: True si presupuesto > 1.000.000
    millonario = fields.Boolean(
        compute='_es_millonario',
        string='Mas de un millon de euros',
    )

    # ---- Relacion Many2one con categorias ----
    categoria_id = fields.Many2one(
        'videoclub.categorias',
        string='Categoria'
    )

    # ---- Relacion Many2one con compania cinematografica (res.partner) ----
    compania = fields.Many2one(
        'res.partner',
        string='Compania'
    )

    # ---- Metodos de campos calculados ----
    def _valor_subvencion(self):
        for record in self:
            record.subvencionado = record.presupuesto * 0.3

    @api.depends('presupuesto')
    def _valor_inversion(self):
        for record in self:
            record.invertido = record.presupuesto * 0.7

    @api.depends('presupuesto')
    def _es_millonario(self):
        for record in self:
            record.millonario = record.presupuesto > 1000000


# =====================================================
# MODELO 2: CATEGORIAS (videoclub.categorias)
# Tarea 4 - Parte 2: gestionado SOLO por el Jefe
# =====================================================
class videoclub_categorias(models.Model):
    _name = 'videoclub.categorias'
    _description = 'Categoria de Pelicula'

    name = fields.Char(
        'Nombre', size=50, required=True,
        help='Nombre de la categoria'
    )
    descripcion = fields.Text(
        string='Descripcion',
        help='Descripcion de la categoria'
    )

    # Relacion One2many inversa con peliculas
    pelis_ids = fields.One2many(
        'videoclub.pelis',
        'categoria_id',
        string='Peliculas'
    )


# =====================================================
# HERENCIA: COMPANIA CINEMATOGRAFICA (extiende res.partner)
# Tarea 4 - herencia de clase/extension
# =====================================================
class compania_cinematografica(models.Model):
    # No necesitamos _name, heredamos de res.partner
    _inherit = 'res.partner'

    # Nuevo campo: si la compania esta premiada
    premiada = fields.Boolean(default=False, string='Premiada')

    # Campo para diferenciar contactos de cine del resto
    is_cine = fields.Boolean(string='Es compania de cine')
