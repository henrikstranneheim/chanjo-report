# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask import Blueprint, render_template, request, url_for
from flask_weasyprint import render_pdf

report = Blueprint('report', __name__, template_folder='templates')


@report.route('/hello')
@report.route('/hello/<name>')
def hello_html(name='World'):
  return render_template('hello.html', name=name)


@report.route('/hello_<name>.pdf')
def hello_pdf(name):
  # make a PDF from another view
  response = render_pdf(url_for('report.hello_html', name=name))

  # check if the request is to download the file right away
  if 'dl' in request.args:
    fname = "hello_%s.pdf" % name
    response.headers['Content-Disposition'] = 'attachment; filename=' + fname

  return response
