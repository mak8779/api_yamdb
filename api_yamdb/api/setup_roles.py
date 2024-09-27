""" from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from reviews.models import Review, Comment


def setup_roles():
    user_group, created = Group.objects.get_or_create(name='User')
    moderator_group, created = Group.objects.get_or_create(name='Moderator')
    admin_group, created = Group.objects.get_or_create(name='Admin')

    review_ct = ContentType.objects.get_for_model(Review)
    comment_ct = ContentType.objects.get_for_model(Comment)

    user_permissions = Permission.objects.filter(
        content_type__in=[review_ct, comment_ct],
        codename__in=[
            'add_review', 'change_review', 'delete_review',
            'add_comment', 'change_comment', 'delete_comment'
        ])
    user_group.permissions.add(*user_permissions)

    moderator_permissions = Permission.objects.filter(
        content_type__in=[review_ct, comment_ct],
        codename__in=[
            'change_review', 'delete_review',
            'change_comment', 'delete_comment'
        ])
    moderator_group.permissions.add(*moderator_permissions)

    admin_permissions = Permission.objects.all()
    admin_group.permissions.add(*admin_permissions)
 """
