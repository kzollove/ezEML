#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: views.py

:Synopsis:

:Author:
    costa
    servilla

:Created:
    7/23/18
"""
import daiquiri
import json
from flask import Blueprint, flash, render_template, redirect, request, url_for
from webapp.home.forms import CreateEMLForm, ResponsiblePartyForm, AbstractForm, KeywordsForm, MinimalEMLForm

from metapype.eml2_1_1 import export
from metapype.eml2_1_1 import names
from metapype.eml2_1_1 import validate
from metapype.model.node import Node

from webapp.home.metapype_client import load_eml, save_eml, log_as_xml


logger = daiquiri.getLogger('views: ' + __name__)
home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def index():
    return render_template('index.html')


@home.route('/about')
def about():
    return render_template('about.html')


@home.route('/create', methods=['GET', 'POST'])
def create():
    # Determine POST type
    if request.method == 'POST':
        if 'Validate' in request.form:
            submit_type = 'Validate'
        elif 'Next' in request.form:
            submit_type = 'Next'
        else:
            submit_type = None
    form = CreateEMLForm()
    # Process POST
    if form.validate_on_submit():
        packageid = form.packageid.data
        create_eml(packageid=packageid,
                   title=form.title.data)
        new_page = 'creator' if (submit_type == 'Next') else 'create'
        return redirect(url_for(f'home.{new_page}', packageid=packageid))
    # Process GET
    return render_template('create_eml.html', title='Create New EML', form=form)


@home.route('/creator/<packageid>', methods=['GET', 'POST'])
def creator(packageid=None):
    # Determine POST type
    if request.method == 'POST':
        if 'Validate' in request.form:
            submit_type = 'Validate'
        elif 'Next' in request.form:
            submit_type = 'Next'
        else:
            submit_type = None
    form = ResponsiblePartyForm(responsible_party="Creator", packageid=packageid)

    # Process POST
    if form.validate_on_submit():   
        salutation = form.salutation.data
        gn = form.gn.data
        sn = form.sn.data
        organization = form.organization.data
        position_name = form.position_name.data
        address_1 = form.address_1.data
        address_2 = form.address_2.data
        city = form.city.data
        state = form.state.data
        postal_code = form.postal_code.data
        country = form.country.data
        phone = form.phone.data
        fax = form.fax.data
        email = form.email.data
        online_url = form.online_url.data

        create_creator(
            packageid,   
            salutation,
            gn,
            sn,
            organization,
            position_name,
            address_1,
            address_2,
            city,
            state,
            postal_code,
            country,
            phone,
            fax,
            email,
            online_url)

        new_page = 'abstract' if (submit_type == 'Next') else 'creator'
        return redirect(url_for(f'home.{new_page}', packageid=packageid))
    # Process GET
    return render_template('responsible_party.html', title='Creator', form=form)


@home.route('/abstract/<packageid>', methods=['GET', 'POST'])
def abstract(packageid=None):
    # Determine POST type
    if request.method == 'POST':
        if 'Validate' in request.form:
            submit_type = 'Validate'
        elif 'Next' in request.form:
            submit_type = 'Next'
        else:
            submit_type = None
    # Process POST
    form = AbstractForm(packageid=packageid)
    if form.validate_on_submit():
        abstract = form.abstract.data
        create_abstract(packageid=packageid, abstract=abstract)
        new_page = 'keywords' if (submit_type == 'Next') else 'abstract'
        return redirect(url_for(f'home.{new_page}', packageid=packageid))
    # Process GET
    return render_template('abstract.html', title='Abstract', packageid=packageid, form=form)


@home.route('/keywords/<packageid>', methods=['GET', 'POST'])
def keywords(packageid=None):
    # Determine POST type
    if request.method == 'POST':
        if 'Validate' in request.form:
            submit_type = 'Validate'
        elif 'Next' in request.form:
            submit_type = 'Next'
        else:
            submit_type = None
    # Process POST
    form = KeywordsForm(packageid=packageid)
    if form.validate_on_submit():
        keywords_list = []
        append_if_non_empty(keywords_list, form.k01.data)
        append_if_non_empty(keywords_list, form.k02.data)
        append_if_non_empty(keywords_list, form.k03.data)
        append_if_non_empty(keywords_list, form.k04.data)
        append_if_non_empty(keywords_list, form.k05.data)
        append_if_non_empty(keywords_list, form.k06.data)
        append_if_non_empty(keywords_list, form.k07.data)
        append_if_non_empty(keywords_list, form.k08.data)
        create_keywords(packageid=packageid, keywords_list=keywords_list)
        new_page = 'contact' if (submit_type == 'Next') else 'keywords'
        return redirect(url_for(f'home.{new_page}', packageid=packageid))
    # Process GET
    return render_template('keywords.html', title='Keywords', packageid=packageid, form=form)


@home.route('/contact/<packageid>', methods=['GET', 'POST'])
def contact(packageid=None):
    # Determine POST type
    if request.method == 'POST':
        if 'Validate' in request.form:
            submit_type = 'Validate'
        elif 'Next' in request.form:
            submit_type = 'Next'
        else:
            submit_type = None
    form = ResponsiblePartyForm(responsible_party="Contact", packageid=packageid)

    # Process POST
    if form.validate_on_submit():   
        salutation = form.salutation.data
        gn = form.gn.data
        sn = form.sn.data
        organization = form.organization.data
        position_name = form.position_name.data
        address_1 = form.address_1.data
        address_2 = form.address_2.data
        city = form.city.data
        state = form.state.data
        postal_code = form.postal_code.data
        country = form.country.data
        phone = form.phone.data
        fax = form.fax.data
        email = form.email.data
        online_url = form.online_url.data

        create_contact(
            packageid,   
            salutation,
            gn,
            sn,
            organization,
            position_name,
            address_1,
            address_2,
            city,
            state,
            postal_code,
            country,
            phone,
            fax,
            email,
            online_url)

        new_page = 'contact' if (submit_type == 'Next') else 'contact'
        return redirect(url_for(f'home.{new_page}', packageid=packageid))
    # Process GET
    return render_template('responsible_party.html', title='Contact', form=form)


@home.route('/minimal', methods=['GET', 'POST'])
def minimal():
    # Process POST
    form = MinimalEMLForm()
    if form.validate_on_submit():
        validate_minimal(packageid=form.packageid.data,
                         title=form.title.data, 
                         creator_gn=form.creator_gn.data, 
                         creator_sn=form.creator_sn.data,
                         contact_gn=form.contact_gn.data, 
                         contact_sn=form.contact_sn.data)
    # Process GET
    return render_template('minimal_eml.html', title='Minimal EML', form=form)


def append_if_non_empty(some_list: list, value: str):
    if (value is not None and len(value) > 0):
        some_list.append(value)


def create_eml(packageid=None, title=None):
    eml_node = Node(names.EML)

    eml_node.add_attribute('packageId', packageid)
    eml_node.add_attribute('system', 'https://pasta.edirepository.org')

    dataset_node = Node(names.DATASET, parent=eml_node)
    eml_node.add_child(dataset_node)

    title_node = Node(names.TITLE)
    title_node.content = title
    dataset_node.add_child(title_node)

    validate_node(eml_node)

    try:
        save_eml(packageid=packageid, eml_node=eml_node)
    except Exception as e:
        logger.error(e)


def create_creator(packageid:str=None, 
                   salutation:str=None,
                   gn:str=None,
                   sn:str=None,
                   organization:str=None,
                   position_name:str=None,
                   address_1:str=None,
                   address_2:str=None,
                   city:str=None,
                   state:str=None,
                   postal_code:str=None,
                   country:str=None,
                   phone:str=None,
                   fax:str=None,
                   email:str=None,
                   online_url:str=None):

    try:
        eml_node = load_eml(packageid=packageid)
        logger.info(f"loaded the following package: {packageid} containing eml node: {eml_node}")
        dataset_node = eml_node.find_child('dataset')
        creator_node = Node(names.CREATOR)
        dataset_node.add_child(creator_node)

        individual_name_node = Node(names.INDIVIDUALNAME)

        if salutation is not None:
            salutation_node = Node(names.SALUTATION)
            salutation_node.content = salutation
            individual_name_node.add_child(salutation_node)

        if gn is not None:
            given_name_node = Node(names.GIVENNAME)
            given_name_node.content = gn
            individual_name_node.add_child(given_name_node)

        if sn is not None:
            surname_node = Node(names.SURNAME)
            surname_node.content = sn
            individual_name_node.add_child(surname_node)

        creator_node.add_child(individual_name_node)

        if organization is not None:
            organization_name_node = Node(names.ORGANIZATIONNAME)
            organization_name_node.content = organization
            creator_node.add_child(organization_name_node)

        if position_name is not None:
            position_name_node = Node(names.POSITIONNAME)
            position_name_node.content = position_name
            creator_node.add_child(position_name_node)

        address_node = Node(names.ADDRESS)

        if address_1 is not None:
            delivery_point_node_1 = Node(names.DELIVERYPOINT)
            delivery_point_node_1.content = address_1
            address_node.add_child(delivery_point_node_1)

        if address_2 is not None:
            delivery_point_node_2 = Node(names.DELIVERYPOINT)
            delivery_point_node_2.content = address_2
            address_node.add_child(delivery_point_node_2)

        if city is not None:
            city_node = Node(names.CITY)
            city_node.content = city
            address_node.add_child(city_node)

        if state is not None:
            administrative_area_node = Node(names.ADMINISTRATIVEAREA)
            administrative_area_node.content = state
            address_node.add_child(administrative_area_node)

        if postal_code is not None:
            postal_code_node = Node(names.POSTALCODE)
            postal_code_node.content = postal_code
            address_node.add_child(postal_code_node)

        if country is not None:
            country_node = Node(names.COUNTRY)
            country_node.content = country
            address_node.add_child(country_node)

        creator_node.add_child(address_node)

        if phone is not None:
            phone_node = Node(names.PHONE)
            phone_node.content = phone
            phone_node.add_attribute('phonetype', 'voice')
            creator_node.add_child(phone_node)

        if fax is not None:
            fax_node = Node(names.PHONE)
            fax_node.content = fax
            fax_node.add_attribute('phonetype', 'facsimile')
            creator_node.add_child(fax_node)

        if email is not None:
            email_node = Node(names.ELECTRONICMAILADDRESS)
            email_node.content = email
            creator_node.add_child(email_node)

        if online_url is not None:
            online_url_node = Node(names.ONLINEURL)
            online_url_node.content = online_url
            creator_node.add_child(online_url_node)
             
        validate_node(eml_node)
        log_as_xml(eml_node)
        save_eml(packageid=packageid, eml_node=eml_node)

    except Exception as e:
        logger.error(e)
   

def create_abstract(packageid=None, abstract=None):
    if abstract is not None:
        try:
            eml_node = load_eml(packageid=packageid)
            logger.info(f"loaded the following package: {packageid} containing eml node: {eml_node}")
            dataset_node = eml_node.find_child('dataset')
            abstract_node = Node(names.ABSTRACT)
            abstract_node.content = abstract
            abstract_node.add_attribute('xml:lang', 'en')
            dataset_node.add_child(abstract_node)
            validate_node(eml_node)
            log_as_xml(eml_node)
            save_eml(packageid=packageid, eml_node=eml_node)
        except Exception as e:
            logger.error(e)


def create_keywords(packageid:str=None, keywords_list:list=[]):
    logger.info(f"The keywords are: {keywords_list}")
    if len(keywords_list) > 0:
        try:
            eml_node = load_eml(packageid=packageid)
            logger.info(f"loaded the following package: {packageid} containing eml node: {eml_node}")
            dataset_node = eml_node.find_child('dataset')
            keywordset_node = Node(names.KEYWORDSET)
            dataset_node.add_child(keywordset_node)

            for keyword in keywords_list:
                keyword_node = Node(names.KEYWORD)
                keyword_node.content = keyword
                keywordset_node.add_child(keyword_node)

            validate_node(eml_node)
            log_as_xml(eml_node)
            save_eml(packageid=packageid, eml_node=eml_node)

        except Exception as e:
            logger.error(e)


def create_contact(packageid:str=None, 
                   salutation:str=None,
                   gn:str=None,
                   sn:str=None,
                   organization:str=None,
                   position_name:str=None,
                   address_1:str=None,
                   address_2:str=None,
                   city:str=None,
                   state:str=None,
                   postal_code:str=None,
                   country:str=None,
                   phone:str=None,
                   fax:str=None,
                   email:str=None,
                   online_url:str=None):

    try:
        eml_node = load_eml(packageid=packageid)
        logger.info(f"loaded the following package: {packageid} containing eml node: {eml_node}")
        dataset_node = eml_node.find_child('dataset')
        contact_node = Node(names.CONTACT)
        dataset_node.add_child(contact_node)

        individual_name_node = Node(names.INDIVIDUALNAME)

        if salutation is not None:
            salutation_node = Node(names.SALUTATION)
            salutation_node.content = salutation
            individual_name_node.add_child(salutation_node)

        if gn is not None:
            given_name_node = Node(names.GIVENNAME)
            given_name_node.content = gn
            individual_name_node.add_child(given_name_node)

        if sn is not None:
            surname_node = Node(names.SURNAME)
            surname_node.content = sn
            individual_name_node.add_child(surname_node)

        contact_node.add_child(individual_name_node)

        if organization is not None:
            organization_name_node = Node(names.ORGANIZATIONNAME)
            organization_name_node.content = organization
            contact_node.add_child(organization_name_node)

        if position_name is not None:
            position_name_node = Node(names.POSITIONNAME)
            position_name_node.content = position_name
            contact_node.add_child(position_name_node)

        address_node = Node(names.ADDRESS)

        if address_1 is not None:
            delivery_point_node_1 = Node(names.DELIVERYPOINT)
            delivery_point_node_1.content = address_1
            address_node.add_child(delivery_point_node_1)

        if address_2 is not None:
            delivery_point_node_2 = Node(names.DELIVERYPOINT)
            delivery_point_node_2.content = address_2
            address_node.add_child(delivery_point_node_2)

        if city is not None:
            city_node = Node(names.CITY)
            city_node.content = city
            address_node.add_child(city_node)

        if state is not None:
            administrative_area_node = Node(names.ADMINISTRATIVEAREA)
            administrative_area_node.content = state
            address_node.add_child(administrative_area_node)

        if postal_code is not None:
            postal_code_node = Node(names.POSTALCODE)
            postal_code_node.content = postal_code
            address_node.add_child(postal_code_node)

        if country is not None:
            country_node = Node(names.COUNTRY)
            country_node.content = country
            address_node.add_child(country_node)

        contact_node.add_child(address_node)

        if phone is not None:
            phone_node = Node(names.PHONE)
            phone_node.content = phone
            phone_node.add_attribute('phonetype', 'voice')
            contact_node.add_child(phone_node)

        if fax is not None:
            fax_node = Node(names.PHONE)
            fax_node.content = fax
            fax_node.add_attribute('phonetype', 'facsimile')
            contact_node.add_child(fax_node)

        if email is not None:
            email_node = Node(names.ELECTRONICMAILADDRESS)
            email_node.content = email
            contact_node.add_child(email_node)

        if online_url is not None:
            online_url_node = Node(names.ONLINEURL)
            online_url_node.content = online_url
            contact_node.add_child(online_url_node)
             
        validate_node(eml_node)
        log_as_xml(eml_node)
        save_eml(packageid=packageid, eml_node=eml_node)

    except Exception as e:
        logger.error(e)
   

def validate_minimal(packageid=None, title=None, contact_gn=None, contact_sn=None, creator_gn=None, creator_sn=None):
    eml = Node(names.EML)

    eml.add_attribute('packageId', packageid)
    eml.add_attribute('system', 'https://pasta.edirepository.org')

    dataset = Node(names.DATASET, parent=eml)
    eml.add_child(dataset)

    title_node = Node(names.TITLE)
    title_node.content = title
    dataset.add_child(title_node)
    
    creator_node = Node(names.CREATOR, parent=dataset)
    dataset.add_child(creator_node)

    individualName_creator = Node(names.INDIVIDUALNAME, parent=creator_node)
    creator_node.add_child(individualName_creator)

    givenName_creator = Node(names.GIVENNAME, parent=individualName_creator)
    givenName_creator.content = creator_gn
    individualName_creator.add_child(givenName_creator)

    surName_creator = Node(names.SURNAME, parent=individualName_creator)
    surName_creator.content = creator_sn
    individualName_creator.add_child(surName_creator)

    contact_node = Node(names.CONTACT, parent=dataset)
    dataset.add_child(contact_node)

    individualName_contact = Node(names.INDIVIDUALNAME, parent=contact_node)
    contact_node.add_child(individualName_contact)

    givenName_contact = Node(names.GIVENNAME, parent=individualName_contact)
    givenName_contact.content = contact_gn
    individualName_contact.add_child(givenName_contact)

    surName_contact = Node(names.SURNAME, parent=individualName_contact)
    surName_contact.content = contact_sn
    individualName_contact.add_child(surName_contact)

    xml_str =  export.to_xml(eml)
    print(xml_str)
    validate_node(eml)


def validate_node(node:Node):
    if (node is not None):
        try:
            validate.tree(node)
            flash(f"{node.name} node is valid")
        except Exception as e:
            flash(str(e))
