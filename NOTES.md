In Django, forms are broadly categorized into two types: `Form` and `ModelForm`. The distinction between these two types of forms is crucial for understanding when and how you can use the `save()` method. Here's what each type represents and why the `save()` method behaves differently between them:

### Form
A `Form` in Django is a simple form class that handles basic form-related tasks such as displaying a form and validating user input. It is independent of the database layer, meaning it isn't tied directly to a model. Therefore, a `Form` does not inherently know anything about database operations. Its primary purpose is to validate data.

Since a `Form` is not linked to any Django model, it does not have a `save()` method. If you're using a regular `Form`, you must manually handle what to do with the data upon validation in your view. For instance, you might retrieve data from the form manually and perform any necessary actions, such as saving data to a model or sending an email.

```python
# Example using Django's Form
from django import forms
from django.http import HttpResponseRedirect
from some_app.models import SomeModel

class MyForm(forms.Form):
    my_field = forms.CharField()

def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            # Manually handle the data
            data = form.cleaned_data['my_field']
            instance = SomeModel(field_name=data)
            instance.save()
            return HttpResponseRedirect('/success/')
    else:
        form = MyForm()
    return render(request, 'template_name.html', {'form': form})
```

### ModelForm
A `ModelForm` is specifically designed to handle Django models. It is a subclass of `Form` that knows about a particular model and can perform operations directly related to that model. When you create a `ModelForm`, you link it to a model class, and Django introspects the model to automatically build form fields corresponding to the model fields.

Because a `ModelForm` is tied to a model, it comes with a `save()` method. This method allows you to save the form's data directly to the database. After validating a `ModelForm`, calling `save()` will create or update a model instance with the form's input.

```python
# Example using Django's ModelForm
from django.forms import ModelForm
from some_app.models import SomeModel

class MyModelForm(ModelForm):
    class Meta:
        model = SomeModel
        fields = ['field_name']

def model_form_view(request):
    if request.method == 'POST':
        form = MyModelForm(request.POST)
        if form.is_valid():
            # Automatically save the data to the database
            form.save()
            return HttpResponseRedirect('/success/')
    else:
        form = MyModelForm()
    return render(request, 'template_name.html', {'form': form})
```

### Summary
In summary, the presence of the `save()` method in `ModelForm` and its absence in `Form` reflect their intended use cases. `Form` is for when you need a form that is not directly linked to a database model, while `ModelForm` is used when you want to easily create and process forms based on your models, leveraging Django's ORM capabilities to handle database interactions directly.