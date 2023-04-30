from flask import Flask, render_template, request, redirect, session, Blueprint, flash
from flask_login import login_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Group, Invitation, MembershipRequest
from . import db
main = Blueprint('main', __name__)


@main.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return redirect('/login')

    return render_template('profile.html', user=user)

@main.route('/invite_members', methods=['POST'])
def invite_members():
    if request.method == 'POST':
        group_id = request.form.get('group_id')
        email = request.form.get('email')

        # Check if the user with the provided email exists
        invited_user = User.query.filter_by(email=email).first()
        if invited_user:
            group = Group.query.get(group_id)

            # Check if the invited member is already part of the group
            if invited_user in group.members:
                flash('Member is already part of the group', 'info')
            else:
                # Check if the invitation already exists
                invitation = Invitation.query.filter_by(group_id=group_id, email=email).first()
                if invitation:
                    flash('Invitation already sent', 'info')
                else:
                    # Create a new invitation
                    new_invitation = Invitation(user_id=invited_user.id, group_id=group_id)
                    db.session.add(new_invitation)
                    db.session.commit()

                    flash('Invitation sent successfully', 'success')

                    # Update the invited member's profile with the invitation
                    invited_user.invitations_received.append(new_invitation)
                    # group.invitations_sent.append(new_invitation)
                    db.session.commit()

        else:
            flash('Member does not exist', 'error')

        return redirect('/list_groups')  # Redirect to the list of groups page

@main.route('/request_membership', methods=['POST'])
def request_membership():
    if request.method == 'POST':
        group_id = request.form.get('group_id')
        user_id = request.form.get('user_id')

        group = Group.query.get(group_id)
        user = User.query.get(user_id)

        # Check if the user is already a member of the group
        if user in group.members:
            flash('You are already a member of the group', 'info')
        else:
            # Check if a membership request already exists
            membership_request = MembershipRequest.query.filter_by(group_id=group_id, user_id=user_id).first()
            if membership_request:
                flash('Membership request already sent', 'info')
            else:
                # Create a new membership request
                new_membership_request = MembershipRequest(user_id=user_id, group_id=group_id)
                db.session.add(new_membership_request)
                db.session.commit()

                flash('Membership request sent successfully', 'success')

                # Update the group's profile with the invitation
                # invited_user.invitations_received.append(new_invitation)
                group.requests_received.append(new_membership_request)
                db.session.commit()

        return redirect('/list_groups')  # Redirect to the list of groups page
@main.route('/create_group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        name = request.form['group_name']
        description = request.form['group_description']
        owner = 'current_user'  # Replace with the logic to get the current user ID

        # Create a new group instance
        new_group = Group(name=name, description=description, owner=owner)

        try:
            # Add the new group to the database
            db.session.add(new_group)
            db.session.commit()

            flash('Group created successfully', 'success')
            return redirect('/list_groups')  # Redirect to the list of groups page
        except:
            db.session.rollback()
            flash('Error creating group', 'error')
            return redirect('/create_group')  # Redirect back to the create group page

    return render_template('create_group.html')

@main.route('/process_request', methods=['POST'])
def process_request():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        group_id = request.form.get('group_id')
        action = request.form.get('action')

        membership_request = MembershipRequest.query.filter_by(user_id=user_id, group_id=group_id).first()
        if membership_request:
            if action == 'accept':
                membership_request.status = 'accepted'
                flash('Membership request accepted', 'success')
            elif action == 'reject':
                membership_request.status = 'rejected'
                flash('Membership request rejected', 'success')
            else:
                flash('Invalid action', 'error')

            db.session.commit()

            # Delete the membership request
            db.session.delete(membership_request)
            db.session.commit()

        return redirect('/list_groups')  # Redirect to the list of groups page

@main.route('/process_invitation', methods=['POST'])
def process_invitation():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        group_id = request.form.get('group_id')
        action = request.form.get('action')

        invitation = Invitation.query.filter_by(user_id=user_id, group_id=group_id).first()
        if invitation:
            if action == 'accept':
                invitation.status = 'accepted'
                flash('Invitation accepted', 'success')
            elif action == 'reject':
                invitation.status = 'rejected'
                flash('Invitation rejected', 'success')
            else:
                flash('Invalid action', 'error')

            db.session.commit()

            # Delete the invitation
            db.session.delete(invitation)
            db.session.commit()

        return redirect('/list_groups')  # Redirect to the list of groups page