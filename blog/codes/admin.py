from django.contrib import admin
from .models import Author, Category,Post,Signup,Comments,PostView


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Signup)
admin.site.register(PostView)


