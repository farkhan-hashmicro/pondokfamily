# -*- coding: utf-8 -*-
# from odoo import http


# class Pondokfamily(http.Controller):
#     @http.route('/pondokfamily/pondokfamily/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pondokfamily/pondokfamily/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pondokfamily.listing', {
#             'root': '/pondokfamily/pondokfamily',
#             'objects': http.request.env['pondokfamily.pondokfamily'].search([]),
#         })

#     @http.route('/pondokfamily/pondokfamily/objects/<model("pondokfamily.pondokfamily"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pondokfamily.object', {
#             'object': obj
#         })
