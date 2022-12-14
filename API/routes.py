from datetime import datetime
from API.models import ShortUrls
from API import app, db
from random import choice
import string
from flask import render_template, request, flash, redirect, url_for


def generate_short_id(num_of_chars: int):
    """Function to generate short_id of specified number of characters"""
    return ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))


@app.route('/apishort', methods=['POST'])
def api_short():
    if request.method == 'POST':
        url = request.args.get('url')
        short_id = request.args.get('custom_id')
        
        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            return 'Please enter different custom id!'    
        
        if not url:
            return 'The URL is required!'
        
        if not short_id:
            short_id = generate_short_id(8)
        
        new_link = ShortUrls(
            original_url=url, short_id=short_id, created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + "short/" + short_id
        return {'url':short_url}    
            
            

@app.route('/short', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        short_id = request.form['custom_id']

        if short_id and ShortUrls.query.filter_by(short_id=short_id).first() is not None:
            flash('Please enter different custom id!')
            return redirect(url_for('index'))

        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))

        if not short_id:
            short_id = generate_short_id(8)

        new_link = ShortUrls(
            original_url=url, short_id=short_id, created_at=datetime.now())
        db.session.add(new_link)
        db.session.commit()
        short_url = request.host_url + "short/" + short_id
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')


@app.route('/short/<short_id>')
def redirect_url(short_id):
    link = ShortUrls.query.filter_by(short_id=short_id).first()
    if link:
        return redirect(link.original_url)
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))