from django.shortcuts import render

from django.views import View
# Create your views here.


class HomeView(View):

    template = 'home.html'

    def get(self,request,*args,**kwargs):

        return render(request,self.template)

class AboutView(View):

    template = 'lms/about.html'

    def get(self,request,*args,**kwargs):

        return render(request,self.template)

