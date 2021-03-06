from django.shortcuts import render, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView
from .models import RecipePost
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin


class RecipeListView(LoginRequiredMixin, ListView):
    """
    Displays a list of the recipes in database
    Extra context function: Gives extra context to
    be used by template
    """
    model = RecipePost
    context_object_name = 'recipes'
    template_name = 'easy_recipe/recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Recipes'
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """
    Displays detail of recipe in database
    Extra context function: Gives extra context to
    be used by template
    """
    model = RecipePost
    context_object_name = 'recipe'
    template_name = 'easy_recipe/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Recipes'
        return context


class RecipeCreateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       UserPassesTestMixin,
                       CreateView):
    """
    Displays form to create a recipe in database
    Extra context function: Gives extra context to
    be used by template
    Test func: Tests if user is_staff
    Get success func: Gets id of object created and returns
    detail view url of item
    """
    model = RecipePost
    template_name = 'easy_recipe/recipe_create_form.html'
    success_message = 'New recipe created successfully'
    fields = [
        'title',
        'author',
        'content',
        'featured_image',
        ]

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Recipes'
        return context


class RecipeUpdateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       UserPassesTestMixin,
                       UpdateView):
    """
    Displays form to update/edit a recipe in database
    Extra context function: Gives extra context to
    be used by template
    Test func: Tests if user is_staff
    Get success func: Gets id of object created and returns
    detail view url of item
    """
    model = RecipePost
    context_object_name = 'recipe'
    template_name = 'easy_recipe/recipe_update_form.html'
    success_message = 'Recipe updated successfully'
    fields = [
        'title',
        'author',
        'content',
        'featured_image',
        ]

    def get_success_url(self):
        return reverse('recipe_detail', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Recipes'
        return context


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Deletes recipe in database
    Extra context function: Gives extra context to
    be used by template
    Test func: Tests if user is_staff
    Get success func: Gets id of object created and returns
    detail view url of item
    def delete: displays message item was deleted
    """
    model = RecipePost
    template_name = 'easy_recipe/recipe_delete.html'
    success_message = 'Recipe deleted successfully!'
    success_url = reverse_lazy('recipes')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(RecipeDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Recipes'
        return context
