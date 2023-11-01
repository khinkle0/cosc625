from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

@login_required
def create_post(request):
    if request.method == 'GET':
        context = {'form': PostForm()}
        return render(request, 'blog/post_form.html', context)
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('posts')
        else:
            return render(request, 'blog/post_form.html', {'form': form})

@login_required
def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/home.html', context)

@login_required
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.name = request.user
            new_comment.save()
            return redirect('post_detail', id)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'GET':
        context = {'post': post, 'form': PostForm(instance=post), 'id': id}
        return render(request, 'blog/post_edit.html',context)

    elif request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts')
        else:
            return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    context = {'post': post}

    if request.method == 'GET':
        return render(request, 'blog/post_confirm_delete.html', context)
    elif request.method == 'POST':
        post.delete()
        return redirect('posts')

@login_required
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    pk = comment.post.id
    context = {'comment': comment}

    if request.method == 'GET':
        return render(request, 'blog/comment_confirm_delete.html', context)
    elif request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk)

@login_required
def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    comments = comment.post.comments.filter(active=True)
    pk = comment.post.id
    if request.method == 'POST':
        comment_form = CommentForm(request.POST, instance=comment)
        if comment_form.is_valid():
            comment.save()
            return redirect('post_detail', pk)
    else:
        comment_form = CommentForm(instance=comment)
    return render(request, 'blog/comment_edit.html', {'post': comment.post, 'comments': comments, 'comment': comment, 'comment_form': comment_form})
