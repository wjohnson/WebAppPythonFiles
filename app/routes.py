from flask import render_template, redirect, url_for, flash, request, jsonify
from app import appvar
from .forms import SearchForm

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

from util import search
from util import graph as jsgraph

import os
from urllib.parse import quote_plus, quote
import requests


@appvar.route('/')
@appvar.route('/index')
def index():
    form = SearchForm()
    return render_template('index.html', title='Home', form=form)


@appvar.route('/search', methods=['GET','POST'])
def search_page():
    form = SearchForm()
    query = None
    results = []

    if form.validate_on_submit():
        query = form.search.data
        query_string = {'search':quote_plus(query.strip()), "highlight":"content"}
        results = search.query_index(query_string)

    return render_template('search.html', title="Search a Topic", form=form, results = results, query = query)

@appvar.route('/graph/<query>', methods=["POST","GET"])
def graph(query):
    form = SearchForm()
    results = []

    query_string = {'search':quote_plus(query.strip()), "$select":"keyphrases"}
    results = search.query_index(query_string)

    list_of_entities_lists = [doc["keyphrases"] for doc in results]

    nodes, edges = jsgraph.node_edge_creation(list_of_entities_lists, query)

    graph_dict = [{"id":i, "label":value} for i, value in nodes]

    return render_template('graph.html', 
        title='Relationship Mapping', 
        form = form ,
        query = query, 
        graph_dict= graph_dict,
        edge_list = edges,
        results = results
    )

