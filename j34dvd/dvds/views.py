__author__ = 'carljame'

from flask import abort, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from sqlalchemy import and_

from . import dvds
from .. import db
from .forms import DVDForm
from ..models import User, Dvds, Tag, tags

@dvds.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = DVDForm()
    if form.validate_on_submit():
        title = form.title.data
        binder = form.binder.data
        page = form.page.data
        sleeve = form.sleeve.data
        imdb_page = form.imdb_page.data
        tags = form.tags.data
        dvd = Dvds(user=current_user, title=title, binder=binder,
                          page=page, sleeve=sleeve, imdb_page=imdb_page,
                          tags=tags)
        db.session.add(dvd)
        db.session.commit()
        flash('You have stored the DVD {} in binder {}, page {}, '
                         'sleeve {}.'.format(title, binder, page, sleeve))
        return redirect(url_for('main.index'))
    return render_template('dvd_form.html', form=form, title='Add a DVD')

@dvds.route('/edit/<int:dvd_id>', methods=['GET', 'POST'])
@login_required
def edit_dvd(dvd_id):
    dvd = Dvds.query.get_or_404(dvd_id)
    if current_user != dvd.user:
        abort(403)
    form = DVDForm(obj=dvd)
    if form.validate_on_submit():
        form.populate_obj(dvd)
        db.session.commit()
        flash("Stored '{}'".format(dvd.title))
        return redirect(url_for('.user', username=current_user.username))
    return render_template('dvd_form.html', form=form, title='Edit DVD')

@dvds.route('/delete/<int:dvd_id>', methods=['GET', 'POST'])
@login_required
def delete_dvd(dvd_id):
    dvd = Dvds.query.get_or_404(dvd_id)
    if current_user != dvd.user:
        abort(403)
    if request.method == "POST":
        db.session.delete(dvd)
        db.session.commit()
        flash("Deleted '{}'".format(dvd.title))
        return redirect(url_for('.user', username=current_user.username))
    else:
        flash("Please confirm deleting the bookmark.")
    return render_template('confirm_delete.html', dvd=dvd, nolinks=True)


@dvds.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user == user:
        return render_template('user.html', user=user)
    else:
        abort(403)

@dvds.route('/tag/<name>')
@login_required
def tag(name):
    tag = Tag.query.filter_by(name=name).first_or_404()
    discs = Dvds.query.join(Dvds._tags).\
        filter(Dvds.user_id == current_user.id).\
        filter(Tag.name == name).\
        order_by(Dvds.title)
    return render_template('tag.html', tag=tag, discs=discs)
