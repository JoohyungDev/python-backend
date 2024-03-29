from django.shortcuts import render
from .models import Post, Comment, Tag
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def tube_list(request):
    posts = Post.objects.all()
    return render(request, "tube/tube_list.html", {"posts": posts})


def tube_detail(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            message = form.cleaned_data["message"]
            c = Comment.objects.create(author=author, message=message, post=post)
            c.save()
    return render(request, "tube/tube_detail.html", {"post": post, "form": form})


def tube_tag(request, tag):
    posts = Post.objects.filter(tags__name__iexact=tag)
    return render(request, "tube/tube_list.html", {"posts": posts})


@login_required
def tube_create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        p = Post.objects.create(title=title, content=content)
        p.save()
    return render(request, "tube/tube_create.html")


@login_required
def tube_update(request, pk):
    post = Post.objects.get(pk=pk)
    # 내가 쓴 게시물만 업데이트 가능
    if post.author != request.user:
        return redirect("tube_list")
    if request.method == "GET":
        return render(request, "tube/tube_update.html", {"post": post})
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        post.title = title
        post.content = content
        post.save()
    return redirect("tube_detail", pk)


@login_required
def tube_delete(request, pk):
    post = Post.objects.get(pk=pk)
    # 내가 쓴 게시물만 삭제 가능
    if post.author != request.user:
        return redirect("tube_list")
    if request.method == "POST":
        post.delete()
    return redirect("tube_list")
