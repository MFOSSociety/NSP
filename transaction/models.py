from django.db import models

# Create your models here.

class usr(models.Model):

    username = models.CharField(max_length=50, default="")
    password = models.CharField(max_length=20, default="")
    email_id = models.EmailField(max_length=50, default="")
    reg_id = models.CharField(max_length=10, default="")

    def __str__(self):
        return self.username + " " + self.reg_id

class book(models.Model):

    owner = models.ForeignKey(usr, on_delete=models.CASCADE)
    book_name = models.CharField(max_length=50, default="")
    book_price = models.CharField(max_length=10, default="")

    def __str__(self):
        books_price = str(self.book_price)
        return self.book_name + " " + books_price

class tool(models.Model):

    owner = models.ForeignKey(usr, on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=50, default="")
    tool_price = models.CharField(max_length=10, default=" ")

    def __str__(self):
        tools_price = str(self.tool_price)
        return self.tool_name + " " + tools_price


