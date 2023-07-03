from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import User, Post, Like, Comment, Follow

import json

def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')

    # Pagination
    paginator = Paginator(all_posts, 2)
    page_number = request.GET.get("page")
    posts_for_page = paginator.get_page(page_number)

    user_liked_posts = []
    if request.user.is_authenticated:
        user_liked_posts = Post.objects.filter(post_likes__owner=request.user)
    return render(request, "network/index.html", {
        "all_posts": posts_for_page,
        "user_liked_posts": user_liked_posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def new_post(request):
    if request.method == "POST":
        user = request.user
        content = request.POST["content"]
        
        new_post = Post(
            author=user,
            content=content
        )

        new_post.save()
        return HttpResponseRedirect(reverse("index"))

def profile_page(request, username):
    print(username)
    # Get profile posts
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(author=user).order_by('-timestamp')

    # Pagination
    paginator = Paginator(user_posts, 2)
    page_number = request.GET.get("page")
    posts_for_page = paginator.get_page(page_number)

    # Follow section
    followers = user.user_follower.all()
    followings = user.user_following.all()

    # Is current user follow profile
    is_following = False
    if followers.filter(follower=request.user):
        is_following = True

    return render(request, "network/profile.html", {
        "all_posts": posts_for_page,
        "profile": user,
        "follower": followers,
        "following": followings,
        "is_following": is_following
    })

def follow(request):
    target_user = request.POST["target_user"]
    new_following = Follow(
        follower = request.user,
        followed = User.objects.get(username=target_user)
    )
    new_following.save()
    return HttpResponseRedirect(reverse("profile_page", kwargs={"username":target_user}))

def unfollow(request):
    target_user = request.POST["target_user"]
    old_following = Follow.objects.filter(
        follower = request.user,
        followed = User.objects.get(username=target_user))
    old_following.first().delete()
    return HttpResponseRedirect(reverse("profile_page", kwargs={"username":target_user}))

def following_page(request):
    current_user = request.user
    following_users_id = current_user.user_following.values_list("followed_id", flat=True)
    all_posts = Post.objects.filter(author_id__in=following_users_id).order_by('-timestamp')

    # Pagination
    paginator = Paginator(all_posts, 2)
    page_number = request.GET.get("page")
    posts_for_page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "all_posts": posts_for_page
    })

def edit_post(request, post_id):
    if request.method == "POST":
        try:
            current_post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        data = json.loads(request.body)
        current_post.content = data["new_content"]
        current_post.save()
        return JsonResponse({"message": "Post has been changed succesfully."}, status=204)

def like_post(request, post_id):
    current_post = Post.objects.get(pk=post_id)
    new_like = Like(
        owner=request.user,
        post=current_post
    )
    new_like.save()
    return JsonResponse({"message": "Liked!"})

def unlike_post(request, post_id):
    current_post = Post.objects.get(pk=post_id)
    old_like = Like.objects.filter(
        owner=request.user,
        post=current_post)
    old_like.delete()
    return JsonResponse({"message": "Unliked!"})