from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.dateformat import DateFormat
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Blog, BlogLike, Comment
from .forms import AddBlogForm, DeleteBlogForm


@login_required
def browse(request):
    blogs = Blog.objects.all()
    return render(
        request,
        "BlogApp/browse.html",
        {
            "blogs": blogs,
        },
    )


@login_required
def add_blog(request):
    if request.method == "GET":
        form = AddBlogForm()
        return render(
            request,
            "BlogApp/add.html",
            {
                "form": form,
            },
        )
    elif request.method == "POST":
        form = AddBlogForm(request.POST)
        if form.is_valid():
            title, content = form.cleaned_data.get("title"), form.cleaned_data.get(
                "content"
            )
            author = request.user
            new_blog = Blog.objects.create(title=title, author=author, content=content)
            new_blog.save()
            return redirect(reverse("BlogApp:browse"))
        else:
            messages.error(request, "Invalid Form.")
            return redirect(reverse("BlogApp:add_blog"))


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        messages.error(request, "You are not authorised to edit this blog.")
        return redirect(reverse("BlogApp:browse"))
    if request.method == "GET":
        form = AddBlogForm(instance=blog)
    elif request.method == "POST":
        form = AddBlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{blog.title}' by {blog.author} was edited!")
            return redirect(reverse("BlogApp:browse"))
    return render(
        request,
        "BlogApp/edit.html",
        {
            "form": form,
            "blog": blog,
        },
    )


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if blog.author != request.user:
        messages.error(request, "You are not authorised to delete this blog.")
        return redirect(reverse("BlogApp:browse"))
    if request.method == "POST":
        form = DeleteBlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog.delete()
            messages.success(request, f"Blog '{blog.title}' was deleted.")
            return redirect(reverse("BlogApp:browse"))
    elif request.method == "GET":
        return render(
            request,
            "BlogApp/delete.html",
            {
                "blog": blog,
            },
        )


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    user = request.user

    try:
        BlogLike.objects.create(blog=blog, user=user)
        blog.likes.add(user)
        blog.save()
    except IntegrityError:
        return JsonResponse(
            {"error": "You have already liked this blog post."}, status=400
        )

    return JsonResponse({"likes": blog.likes.count()})


@login_required
def add_comment(request, blog_id):
    if request.method == "POST":
        blog = get_object_or_404(Blog, id=blog_id)
        content = request.POST.get("content")
        if content:
            comment = Comment.objects.create(
                blog=blog, user=request.user, content=content
            )
            created_at = DateFormat(comment.created_at).format('F j, Y, H:i')
            return JsonResponse(
                {
                    "user": comment.user.username,
                    "content": comment.content,
                    "created_at": created_at,
                }
            )
    return JsonResponse({"error": "Invalid comment data."}, status=400)
