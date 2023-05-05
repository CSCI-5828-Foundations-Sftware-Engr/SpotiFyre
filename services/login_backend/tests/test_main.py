# REQ: pip install Flask-Testing

import unittest
from flask import url_for
from flask_testing import TestCase

from app import create_app
from app.models import db, User, Group, Invitation, MembershipRequest, Member

app = create_app()

class TestMainRoutes(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        # Create a test user
        test_user = User(email='test@example.com', name='Test User', password='test_password')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_profile_redirect(self):
        response = self.client.get(url_for('main.profile'))
        self.assertRedirects(response, url_for('auth.login'))

    def test_invite_members(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a test group
            test_group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            db.session.add(test_group)
            db.session.commit()

            # Create a user to invite
            invited_user = User(email='invitee@example.com', name='Invitee', password='invitee_password')
            db.session.add(invited_user)
            db.session.commit()

            # Test sending an invitation to an existing user
            response = self.client.post(
                url_for('main.invite_members'),
                data=dict(group_id=test_group.id, email=invited_user.email),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertEqual(json_data['message'], 'Invitation sent successfully')

            # Test sending an invitation to a non-existent user
            response = self.client.post(
                url_for('main.invite_members'),
                data=dict(group_id=test_group.id, email='nonexistent@example.com'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertFalse(json_data['success'])
            self.assertEqual(json_data['message'], 'Member does not exist')

            # Test sending an invitation to the same user again (duplicate)
            response = self.client.post(
                url_for('main.invite_members'),
                data=dict(group_id=test_group.id, email=invited_user.email),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertFalse(json_data['success'])
            self.assertEqual(json_data['message'], 'Invitation already sent')

    def test_request_membership(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a test group
            test_group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            db.session.add(test_group)
            db.session.commit()

            # Create a user to request membership
            requesting_user = User(email='requester@example.com', name='Requester', password='requester_password')
            db.session.add(requesting_user)
            db.session.commit()

            # Log in the requesting user
            self.client.post(
                url_for('auth.login'),
                data=dict(email=requesting_user.email, password='requester_password'),
                follow_redirects=True
            )

            # Test sending a membership request to an existing group
            response = self.client.post(
                url_for('main.request_membership'),
                data=dict(group_id=test_group.id),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertEqual(json_data['message'], 'Membership request sent successfully')

            # Test sending a membership request to the same group again (duplicate)
            response = self.client.post(
                url_for('main.request_membership'),
                data=dict(group_id=test_group.id),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertFalse(json_data['success'])
            self.assertEqual(json_data['message'], 'Membership request already sent')
    
    def test_get_all_invitations(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a test group
            test_group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            db.session.add(test_group)
            db.session.commit()

            # Create a user to be invited
            invited_user = User(email='invitee@example.com', name='Invitee', password='invitee_password')
            db.session.add(invited_user)
            db.session.commit()

            # Send an invitation to the user
            invitation = Invitation(user_id=invited_user.id, group_id=test_group.id)
            db.session.add(invitation)
            db.session.commit()

            # Log in the invited user
            self.client.post(
                url_for('auth.login'),
                data=dict(email=invited_user.email, password='invitee_password'),
                follow_redirects=True
            )

            # Test getting all invitations for the invited user
            response = self.client.post(
                url_for('main.get_all_invitations'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertEqual(json_data['message'], 'Invites fetched.')
            self.assertEqual(len(json_data['data']), 1)
            self.assertEqual(json_data['data'][0]['id'], invitation.id)
            self.assertEqual(json_data['data'][0]['user_id'], invited_user.id)
            self.assertEqual(json_data['data'][0]['group_id'], test_group.id)
            self.assertEqual(json_data['data'][0]['status'], 'pending')

    def test_get_all_membership_requests(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a test group
            test_group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            db.session.add(test_group)
            db.session.commit()

            # Create a user to request membership
            requesting_user = User(email='requester@example.com', name='Requester', password='requester_password')
            db.session.add(requesting_user)
            db.session.commit()

            # Request membership for the test group
            membership_request = MembershipRequest(user_id=requesting_user.id, group_id=test_group.id)
            db.session.add(membership_request)
            db.session.commit()

            # Test getting all membership requests for the test user's groups
            response = self.client.post(
                url_for('main.get_all_membership_requests'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertEqual(json_data['message'], 'Membership Requests fetched.')
            self.assertEqual(len(json_data['data']), 1)
            self.assertEqual(json_data['data'][0]['id'], membership_request.id)
            self.assertEqual(json_data['data'][0]['user_id'], requesting_user.id)
            self.assertEqual(json_data['data'][0]['group_id'], test_group.id)
            self.assertEqual(json_data['data'][0]['status'], 'pending')

    def test_create_group(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Test creating a new group
            response = self.client.post(
                url_for('main.create_group'),
                data=dict(group_name='Test Group', group_description='Test Group Description'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertIn('Group created successfully.', json_data['message'])

            # Check if the group was created in the database
            new_group = Group.query.filter_by(name='Test Group').first()
            self.assertIsNotNone(new_group)
            self.assertEqual(new_group.description, 'Test Group Description')
            self.assertEqual(new_group.owner_id, 1)

            # Check if the new member was added
            new_member = Member.query.filter_by(user_id=1, group_id=new_group.id).first()
            self.assertIsNotNone(new_member)

    def test_list_groups(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a group for testing
            group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            self.db.session.add(group)
            self.db.session.commit()

            # Add a member to the group
            member = Member(user_id=1, group_id=group.id)
            self.db.session.add(member)
            self.db.session.commit()

            # Test listing all groups
            response = self.client.post(
                url_for('main.list_groups'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertIn('Group list sent successfully.', json_data['message'])

            # Check if the test group is in the list of groups
            found_test_group = False
            for group_data in json_data['data']:
                if group_data['id'] == group.id:
                    found_test_group = True
                    self.assertEqual(group_data['name'], 'Test Group')
                    self.assertEqual(group_data['description'], 'Test Group Description')
                    self.assertEqual(group_data['owner']['id'], 1)
                    self.assertEqual(group_data['owner']['username'], 'Test User')
                    self.assertTrue(group_data['isMember'])

            self.assertTrue(found_test_group)

    def test_process_membership_request(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a group for testing
            group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            self.db.session.add(group)
            self.db.session.commit()

            # Create a new user for testing
            new_user = User(email='new@example.com', password=generate_password_hash('new_password', method='sha256'))
            self.db.session.add(new_user)
            self.db.session.commit()

            # Create a membership request for the new user
            membership_request = MembershipRequest(user_id=new_user.id, group_id=group.id, status='pending')
            self.db.session.add(membership_request)
            self.db.session.commit()

            # Test processing the membership request - accept
            response = self.client.post(
                url_for('main.process_membership_request'),
                data=dict(user_id=new_user.id, group_id=group.id, action='accept'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertIn('Membership request processed - accepted', json_data['message'])

            # Test processing the membership request - reject
            membership_request = MembershipRequest(user_id=new_user.id, group_id=group.id, status='pending')
            self.db.session.add(membership_request)
            self.db.session.commit()

            response = self.client.post(
                url_for('main.process_membership_request'),
                data=dict(user_id=new_user.id, group_id=group.id, action='reject'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertIn('Membership request processed - rejected', json_data['message'])

    def test_process_invitation(self):
        with self.client:
            # Log in the test user
            self.client.post(
                url_for('auth.login'),
                data=dict(email='test@example.com', password='test_password'),
                follow_redirects=True
            )

            # Create a group for testing
            group = Group(name='Test Group', description='Test Group Description', owner_id=1)
            self.db.session.add(group)
            self.db.session.commit()

            # Create a new user for testing
            new_user = User(email='new@example.com', password=generate_password_hash('new_password', method='sha256'))
            self.db.session.add(new_user)
            self.db.session.commit()

            # Create an invitation for the new user
            invitation = Invitation(user_id=new_user.id, group_id=group.id, status='pending')
            self.db.session.add(invitation)
            self.db.session.commit()

            # Test processing the invitation - accept
            response = self.client.post(
                url_for('main.process_invitation'),
                data=dict(group_id=group.id, action='accept'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertIn('Invitation processed - accepted', json_data['message'])

            # Test processing the invitation - reject
            invitation = Invitation(user_id=new_user.id, group_id=group.id, status='pending')
            self.db.session.add(invitation)
            self.db.session.commit()

            response = self.client.post(
                url_for('main.process_invitation'),
                data=dict(group_id=group.id, action='reject'),
                follow_redirects=True
            )
            json_data = response.get_json()
            self.assertTrue(json_data['success'])
            self.assertIn('Invitation processed - rejected', json_data['message'])

# if __name__ == '__main__':
#     unittest.main()
