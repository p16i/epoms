#!/usr/local/bin/python

import click
import os
import uuid
from epoms.named_entity_indexer import NamedEntityIndexer
from epoms.entity_extract import EntityExtract

# @click.command()
#               help='The person to greet.')
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('Hello %s!' % name)


@click.group()
# @click.option('--help', default=0, help='[index_named_entity]')
def cli():
    pass


@click.command()
@click.option('--text', default="", help='Text to be indexed')
@click.option('--dry-run', default=0, help='Dry Run')
def index_named_entity( text, dry_run ):
    if( dry_run ):
        print 'NOTE: You`re in dry-run mode.'

    indexer = NamedEntityIndexer()
    if( not dry_run ):
        doc_id = uuid.uuid4().hex
        print "Indexing doc_id : "+ doc_id
        indexer.index_doc( text, doc_id  )

@click.command()
@click.option('--text', default="", help='Text..')
def list_named_entity( text ):

    ee = EntityExtract()
    names = ee.extract_name( text )
    for n in names:
        print "-> "+n


@click.command()
@click.option('--term', default="", help='Search by term')
@click.option('--doc-id', default="", help='Search by doc id')
def search(term, doc_id):
    indexer = NamedEntityIndexer()
    if term:
        click.echo('Searching term : ' + term)
        docs = indexer.search_by_term( term )
        print "There are %d documents having %s." % ( len(docs), term )
        for d in docs:
            print d

    elif doc_id:
        click.echo('Searching document id' + doc_id)
        entities = indexer.search_by_docID( doc_id )
        print "Document %s having %d entities." % ( doc_id, len(entities) )
        for e in entities:
            print '-> ' + e

# cli.add_command(initdb)
cli.add_command(index_named_entity)
cli.add_command(search)
cli.add_command(list_named_entity)

if __name__ == '__main__':
    cli()

