# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from pkg_resources import load_entry_point

import click

from .utils import list_interfaces
from ..miner import Miner

ROOT_PACKAGE = __package__.split('.')[0]


@click.command()
@click.option(
  '-r', '--render', type=click.Choice(list_interfaces()), default='tabular')
@click.option('--human', is_flag=True, help='Make output more human readable')
@click.option(
  '-p', '--panel',
  type=click.File('r', encoding='utf-8'),
  help='Gene panel file with (superblock) IDs')
@click.pass_context
def report(context, render, human, panel):
  """Generate reports from Chanjo SQL output."""
  # get uri + dialect of Chanjo database
  uri, dialect = context.obj.get('db'), context.obj.get('dialect')

  # set the custom option
  context.obj.set('report.human', human)
  context.obj.set('report.panel', panel)

  if uri is None:
    # chanjo executed without "--db" set, prompt user input
    click.prompt('Please enter path to database', type=click.Path(exists=True))

  # create instance of Chanjo API "Miner"
  api = Miner(uri, dialect=dialect)

  # determine which render method to use and initialize it
  render_method = load_entry_point(
    ROOT_PACKAGE, 'chanjo_report.interfaces', render
  )

  # run the render_method and print the result to STDOUT
  click.echo(render_method(api, options=context.obj))