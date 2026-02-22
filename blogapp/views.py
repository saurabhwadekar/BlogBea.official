from django.shortcuts import render,redirect,get_object_or_404
from .models import Blog ,  Comment , Savedblog
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required   #its basic use is that to login to auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages




# Create your views here.



@login_required
def addblog(request):

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('blog_image')

        # Basic validation
        if not title or not description:
            messages.error(request, "Title and description are required.")
            return redirect('addblog')

        # Create blog safely
        blog = Blog(
            title=title,
            description=description,
            blog_image=image,
            user=request.user
        )

        blog.save()

        messages.success(request, "Blog created successfully.")

        return redirect('home')

    return render(request, 'addblog.html')


        

# changes
@login_required
def viewBg(request, bg_id):
    blog = get_object_or_404(Blog, id=bg_id)
    # comments=blog.comments.all()
    # print("FOUND COMMENTS:",comments)
    # print(f'foundedblog{blog}')
    return render(request, "vb.html",{"blog": blog,})





#-----------------------------------------------------------------------------------
@login_required
def myblog(request):
    blogs = Blog.objects.filter(user=request.user)
    return render(request, "myblog.html", {"blogs": blogs})



    
    
@login_required
def delete_blog(request, bg_id):
    blog = get_object_or_404(Blog, id=bg_id)
    blog.delete()
    return redirect('myblog')

@login_required
def edit_blog(request, bg_id):
    blog = get_object_or_404(Blog, id=bg_id)

    if request.method == 'POST':
        title = request.POST.get("title")
        description = request.POST.get("description")
        blog_image = request.FILES.get("blog_image")  # Use .get() to avoid error

        blog.title = title
        blog.description = description
        
        if blog_image:
            blog.blog_image = blog_image  #blog img

        blog.save()
        return redirect('myblog')

    return render(request, "editblog.html", {"blog": blog})
    
#-------------------------------------------------------------------------


    
def is_reccuring(request,blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    return render(request,"is_recc.html",{'blog':blog})




def Userprofile(request):
    blogs=Blog.objects.filter(user=request.user).order_by("created_at")
    return render(request, 'profile.html',{"blogs":blogs})


@login_required
def editpf(request):
    user = request.user
    if request.method == 'POST':
       
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        first_name = user.first_name
        user.save()   # To save the changes/update
        
        return redirect('profile')
    return render(request, 'editpf.html',{'user':user} )
    
# COMMENT FROM NEW_FEATURE BRANCH
from django.views import View





    
from django.http import JsonResponse
from .models import Blog




@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    liked = False

    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        liked = False
    else:
        blog.likes.add(request.user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': blog.likes.count()
    })


@login_required
def add_comment(request, blog_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        blog = Blog.objects.get(id=blog_id)
        Comment.objects.create(blog=blog, content=content, user=request.user)
        return redirect(request.META.get('HTTP_REFERER', '/'))

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Checks if the current user has already liked the blog
    user_has_liked = blog.likes.filter(user=request.user).exists()

    return render(request, 'blogdetails.html', {
        'blog': blog,
        'user_has_liked': user_has_liked,
    })


def savedblog(request, blog_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Unauthorized Access')

    blog = get_object_or_404(Blog, id=blog_id)
    Savedblog.objects.create(blog=blog, user=request.user)
    return redirect('home')    
 
@login_required
def saved_blogs_view(request):
    
    saved_blogs = Savedblog.objects.filter(user=request.user).order_by('-timestamp')  # ✅ Correct
    return render(request, 'savebg.html', {'saved_blogs': saved_blogs})

@login_required
def remove_saved_blog(request, blog_id):
    blog = get_object_or_404(Savedblog, id=blog_id, user=request.user)
    blog.delete()
    return redirect('saved_blogs')        


# views.py
import openai
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt





# blog/views.py
from django.http import JsonResponse
import random

# Simple demo title generator (you can integrate GPT or your own logic here)
def generate_title(request):
    titles = [
       "The Future of AI in 2025",
    "Mastering Productivity in Daily Life",
    "Exploring Mental Health in Your Career",
    "The Art of Digital Marketing in a Digital Era",
    "Secrets of Startups in 2025",
    "Beginner's Guide to Technology in the Modern World",
    "How to Excel in Web Development in Your Career",
    "The Future of Freelancing in a Digital Era",
    "Exploring Personal Growth in Daily Life",
    "Mastering Entrepreneurship in 2025",
    "The Art of Creativity in the Modern World",
    "Secrets of Design Thinking in Your Career",
    "Beginner's Guide to Remote Work in 2025",
    "How to Excel in Blockchain in the Modern World",
    "The Future of Cybersecurity in a Digital Era",
    "Mastering Life Hacks in Your Career",
    "Exploring Finance in the Modern World",
    "The Art of Data Science in 2025",
    "Secrets of Education in a Digital Era",
    "Beginner's Guide to Social Media in Your Career",
    "Mastering AI in the Modern World",
    "Exploring Productivity in 2025",
    "The Future of Mental Health in Daily Life",
    "The Art of Startups in a Digital Era",
    "Secrets of Freelancing in Your Career",
    "Beginner's Guide to Digital Marketing in the Modern World",
    "How to Excel in Technology in a Digital Era",
    "The Future of Web Development in Your Career",
    "Mastering Personal Growth in 2025",
    "Exploring Entrepreneurship in the Modern World",
    "The Art of Remote Work in Daily Life",
    "Secrets of Blockchain in a Digital Era",
    "Beginner's Guide to Cybersecurity in the Modern World",
    "How to Excel in Life Hacks in Your Career",
    "The Future of Finance in 2025",
    "Mastering Data Science in a Digital Era",
    "Exploring Education in Daily Life",
    "The Art of Social Media in the Modern World",
    "Secrets of AI in Your Career",
    "Beginner's Guide to Productivity in 2025",
    "How to Excel in Mental Health in a Digital Era",
    "The Future of Startups in the Modern World",
    "Mastering Freelancing in Daily Life",
    "Exploring Digital Marketing in Your Career",
    "The Art of Technology in 2025",
    "Secrets of Web Development in a Digital Era",
    "Beginner's Guide to Personal Growth in Your Career",
    "How to Excel in Entrepreneurship in the Modern World",
    "The Future of Remote Work in Daily Life",
    "Mastering Blockchain in Your Career",
    "Exploring Cybersecurity in the Modern World"
    ]
    return JsonResponse({"title": random.choice(titles)})

# Simple demo description generator
def generate_description(request):
    descriptions = [
        "Dive deep into the evolving world of artificial intelligence and discover how it shapes our lives.",
        "This blog explores the hidden potential of forming simple habits for long-term success.",
        "Minimalism isn't just aesthetics — it's a mindset for intentional living.",
        "Explore the complexity and beauty of human psychology and emotional intelligence.",
        "A practical, step-by-step guide to help you take control of your time and energy.",
           "This blog post uncovers practical insights to improve your understanding of AI and how it shapes future innovation.",
    "This blog post uncovers expert advice to improve your understanding of productivity and how it shapes your success.",
    "This blog post uncovers modern trends to improve your understanding of mental health and how it shapes digital transformation.",
    "This blog post uncovers hidden strategies to improve your understanding of digital marketing and how it shapes the industry.",
    "This blog post uncovers creative approaches to improve your understanding of startups and how it shapes your success.",
    "This blog post uncovers expert advice to improve your understanding of technology and how it shapes future innovation.",
    "This blog post uncovers practical insights to improve your understanding of web development and how it shapes your success.",
    "This blog post uncovers modern trends to improve your understanding of freelancing and how it shapes digital transformation.",
    "This blog post uncovers creative approaches to improve your understanding of personal growth and how it shapes the industry.",
    "This blog post uncovers hidden strategies to improve your understanding of entrepreneurship and how it shapes your success.",
    "This blog post uncovers expert advice to improve your understanding of creativity and how it shapes your success.",
    "This blog post uncovers practical insights to improve your understanding of design thinking and how it shapes the industry.",
    "This blog post uncovers creative approaches to improve your understanding of remote work and how it shapes daily habits.",
    "This blog post uncovers hidden strategies to improve your understanding of blockchain and how it shapes future innovation.",
    "This blog post uncovers expert advice to improve your understanding of cybersecurity and how it shapes the industry.",
    "This blog post uncovers practical insights to improve your understanding of life hacks and how it shapes your success.",
    "This blog post uncovers modern trends to improve your understanding of finance and how it shapes digital transformation.",
    "This blog post uncovers hidden strategies to improve your understanding of data science and how it shapes your success.",
    "This blog post uncovers expert advice to improve your understanding of education and how it shapes the industry.",
    "This blog post uncovers creative approaches to improve your understanding of social media and how it shapes digital transformation.",
    "This blog post uncovers expert advice to improve your understanding of AI and how it shapes the industry.",
    "This blog post uncovers modern trends to improve your understanding of productivity and how it shapes future innovation.",
    "This blog post uncovers practical insights to improve your understanding of mental health and how it shapes your success.",
    "This blog post uncovers creative approaches to improve your understanding of startups and how it shapes daily habits.",
    "This blog post uncovers hidden strategies to improve your understanding of freelancing and how it shapes digital transformation.",
    "This blog post uncovers expert advice to improve your understanding of digital marketing and how it shapes your success.",
    "This blog post uncovers practical insights to improve your understanding of technology and how it shapes future innovation.",
    "This blog post uncovers modern trends to improve your understanding of web development and how it shapes the industry.",
    "This blog post uncovers creative approaches to improve your understanding of personal growth and how it shapes your success.",
    "This blog post uncovers expert advice to improve your understanding of entrepreneurship and how it shapes future innovation.",
    "This blog post uncovers hidden strategies to improve your understanding of remote work and how it shapes daily habits.",
    "This blog post uncovers modern trends to improve your understanding of blockchain and how it shapes the industry.",
    "This blog post uncovers creative approaches to improve your understanding of cybersecurity and how it shapes your success.",
    "This blog post uncovers expert advice to improve your understanding of life hacks and how it shapes digital transformation.",
    "This blog post uncovers practical insights to improve your understanding of finance and how it shapes your success.",
    "This blog post uncovers hidden strategies to improve your understanding of data science and how it shapes the industry.",
    "This blog post uncovers expert advice to improve your understanding of education and how it shapes future innovation.",
    "This blog post uncovers creative approaches to improve your understanding of social media and how it shapes the industry.",
    "This blog post uncovers practical insights to improve your understanding of AI and how it shapes digital transformation.",
    "This blog post uncovers expert advice to improve your understanding of productivity and how it shapes your success.",
    "This blog post uncovers hidden strategies to improve your understanding of mental health and how it shapes the industry.",
    "This blog post uncovers modern trends to improve your understanding of startups and how it shapes your success.",
    "This blog post uncovers creative approaches to improve your understanding of freelancing and how it shapes future innovation.",
    "This blog post uncovers expert advice to improve your understanding of digital marketing and how it shapes the industry.",
    "This blog post uncovers practical insights to improve your understanding of technology and how it shapes your success.",
    "This blog post uncovers modern trends to improve your understanding of web development and how it shapes future innovation.",
    "This blog post uncovers creative approaches to improve your understanding of personal growth and how it shapes digital transformation.",
    "This blog post uncovers expert advice to improve your understanding of entrepreneurship and how it shapes your success.",
    "This blog post uncovers practical insights to improve your understanding of remote work and how it shapes the industry.",
    "This blog post uncovers hidden strategies to improve your understanding of blockchain and how it shapes your success.",
    "This blog post uncovers expert advice to improve your understanding of cybersecurity and how it shapes future innovation."
]
    
    return JsonResponse({"description": random.choice(descriptions)})
