from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserForm
from django.views.generic import View

def home(request):
    return render(request, 'Homepage.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'Homepage.html')
    context = {
        "form": form,
    }
    return render(request, 'Homepage.html', context)



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                # redirect the user when he is logged in
                return render(request, 'account/Login.html', {'albums': albums})
            else:
                return render(request, 'account/Login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'account/Login.html', {'error_message': 'Invalid login'})
    return render(request, 'account/Login.html')



class UserFormView(View):
    form_class = UserForm
    template_name = 'account/registration.html'

    #display a blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request, self.template_name)

    #process form data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # normalize the data (data formatted properly)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #authenticate
            user = authenticate(user=username,password=password)
            if user is not None:
                login(request,user)
                # return to something should be dashboard
                return redirect('#')
        # If wrong info we redirect here
        return redirect('#')



