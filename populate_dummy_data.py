from django.contrib.auth.models import User
from app.models import Profile, Tag, Post, Comments, Subscribe, WebsiteMeta
from django.utils.text import slugify
from django.core.files.base import ContentFile
import base64
import random

def create_dummy_data():
    # First clear existing data
    User.objects.all().delete()
    Profile.objects.all().delete()
    Tag.objects.all().delete()
    Post.objects.all().delete()
    Comments.objects.all().delete()
    Subscribe.objects.all().delete()
    WebsiteMeta.objects.all().delete()

    # Create a simple 1x1 pixel base64 encoded image
    dummy_image = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==')

    # Create Users with Profiles
    users = []
    for i in range(5):
        username = f'testuser{i}'
        while User.objects.filter(username=username).exists():
            i += 1
            username = f'testuser{i}'
            
        user = User.objects.create_user(
            username=username,
            email=f'testuser{i}@example.com',
            password='password123',
            first_name=f'First{i}',
            last_name=f'Last{i}'
        )
        users.append(user)
        
        # Create Profile with image for each user
        profile = Profile.objects.create(
            user=user,
            bio=f'This is the bio for {username}',
            slug=slugify(username)
        )
        
        # Add profile image
        profile.profile_image.save(
            f'profile_{i}.png',
            ContentFile(dummy_image),
            save=True
        )

    # Create Tags
    tags = []
    tag_names = ['Technology', 'Travel', 'Food', 'Lifestyle', 'Sports']
    for name in tag_names:
        tag = Tag.objects.create(
            name=name,
            description=f'Posts about {name.lower()}',
            slug=slugify(name)
        )
        tags.append(tag)

    # Create Posts
    posts = []
    for i in range(10):
        post = Post.objects.create(
            title=f'Sample Post {i}',
            content=f'This is the content for sample post {i}. Lorem ipsum dolor sit amet...',
            slug=slugify(f'sample-post-{i}'),
            view_count=random.randint(0, 100),
            is_featured=random.choice([True, False]),
            author=random.choice(users)
        )
        
        # Add post image
        post.image.save(
            f'post_{i}.png',
            ContentFile(dummy_image),
            save=True
        )
        
        # Add random tags to post
        post.tags.add(*random.sample(tags, random.randint(1, 3)))
        # Add random likes
        post.likes.add(*random.sample(users, random.randint(0, 5)))
        posts.append(post)

    # Create Website Meta
    WebsiteMeta.objects.create(
        title='My Amazing Blog',
        description='A blog about everything interesting in technology and lifestyle',
        about='Welcome to my blog! This is a space where I share my thoughts and experiences...'
    )