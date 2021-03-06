from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import TimeSlot, Closed
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def booking_day(request):
    """
    Function to render booking day page. Additional context page_title
    to display name in title and bookings - gets all bookings of user
    """
    current_user = request.user
    page_title = 'Booking'
    user = User.objects.get(id=current_user.id)
    bookings = TimeSlot.objects.filter(user=user)
    return render(request,
                  'booking/booking_day.html',
                  {'bookings': bookings,
                   'page_title': page_title})


@login_required
def booking_detail(request):
    """
    Function to render Booking detail page. Gets date from booking_day
    page.Checks if date is a Closed day if true displays message. If not
    closed day get all booking on that day. Counts all bookings at times.
    If time displays 5 times it removes the time choice and only displays
    available times. Final check to see if time is still available and if
    user did not alter time before posting
    """
    page_title = 'Booking'
    date = request.GET.get('date')
    bookings = TimeSlot.objects.filter(date=date)
    days = Closed.objects.all()
    closed_days = []
    days = Closed.objects.all()
    for day in days:
        closed_days.append(day.day.strftime("%Y-%m-%d"))
    if len(bookings) > 0:
            times = ['12:00', '13:00', '14:00',
                     '15:00', '16:00', '17:00',
                     '18:00', '19:00', '20:00']
        # get times that is booked for date add them to list
            booked_times = []
            for booking in bookings:
                booked_times.append(booking.time)
        # count how many times ,time is in list and add to new list
            count_times = []
            for time in booked_times:
                count_times.append(booked_times.count(time))
            # see if item greater then predetermined amount
            # and add to list
            time = []
            counter = 0
            for num in count_times:
                counter += 1
                if num >= 5:
                    index_of = (counter-1)
                    time.append(str(booked_times[index_of]))
            time = list(dict.fromkeys(time))
        # removes times that is not available
            for slot in time:
                if slot in times:
                    times.remove(slot)
    else:
        times = ['12:00', '13:00', '14:00',
                 '15:00', '16:00', '17:00',
                 '18:00', '19:00', '20:00']

    if request.method == 'POST':
        current_user = request.user
        date = request.POST.get('date')
        time = request.POST.get('time')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        user = User.objects.get(id=current_user.id)
        number_of_people = request.POST.get('number_of_people')
        form = TimeSlot(date=date,
                        first_name=first_name,
                        last_name=last_name,
                        time=time,
                        user=user,
                        phone=phone,
                        number_of_people=number_of_people
                        )
        final_check = TimeSlot.objects.filter(date=date, time=time)
        if len(final_check) < 5 and time in times:
            form.save()
            messages.success(request, 'Booking created successfully!')
            return redirect(reverse('customer_booking_detail',
                                    kwargs={'pk': form.id}))
        else:
            pass

    return render(request, 'booking/booking_detail.html',
                  {'bookings': bookings,
                   'date': date,
                   'times': times,
                   'closed_days': closed_days,
                   'page_title': page_title
                   })


@staff_member_required
def booking_date(request):
    """
    Function to render booking_date page. Addition context page_title
    to display in title
    """
    page_title = 'Booking'
    return render(request,
                  'booking/booking_date.html',
                  {'page_title': page_title})


@staff_member_required
def booking_date_list(request):
    """
    Function to render booking_date_list for staff
    """
    page_title = 'Booking'
    date = request.GET.get('date')
    bookings = TimeSlot.objects.filter(date=date)

    return render(request,
                  'booking/booking_date_list.html',
                  {'bookings': bookings,
                   'date': date,
                   'page_title': page_title})


class ClosedListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    Displays a list of the closed days
    Test_fun: tests if user is a staff member
    Get extra context: Passes extra context to the class based view to use
    """
    model = Closed
    context_object_name = 'dates'
    template_name = 'booking/closed_list.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context


class ClosedDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Displays the detail of the selected closed day
    Test_fun: tests if user is a staff member
    Get extra context: Passes extra context to the class based view to use
    """
    model = Closed
    context_object_name = 'dates'
    template_name = 'booking/closed_detail.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context


class ClosedCreateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       UserPassesTestMixin,
                       CreateView):
    """
    Displays form to create new closed day
    Test_fun: tests if user is a staff member
    Get extra context: Passes extra context to the class based view to use
    Get Success url: gets primary key of closed day created and turns success
    url, detail view of item just created
    """
    model = Closed
    template_name = 'booking/closed_create_form.html'
    success_message = 'Date added successfully'
    fields = [
        'day',
        'reason',
        'user',
        ]

    def get_success_url(self):
        return reverse('closed_detail', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context


class ClosedUpdateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       UserPassesTestMixin,
                       UpdateView):
    """
    Displays form to edit closed day chosed
    Test_fun: tests if user is a staff member
    Get extra context: Passes extra context to the class based view to use
    Get Success url: gets primary key of closed day created and turns success
    url, detail view of item just created
    """
    model = Closed
    context_object_name = 'dates'
    template_name = 'booking/closed_update_form.html'
    success_message = 'Date updated successfully'
    fields = [
        'day',
        'reason',
        'user',
        ]

    def get_success_url(self):
        return reverse('closed_detail', args=[self.object.pk])

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context


class ClosedDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Deletes closed day chosen
    Test_fun: tests if user is a staff member
    Get extra context: Passes extra context to the class based view to use
    Def delete: displays message item was deleted
    """
    model = Closed
    template_name = 'booking/closed_delete.html'
    success_message = 'Date deleted successfully!'
    success_url = reverse_lazy('closed_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ClosedDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context


class CustomerBookingListView(LoginRequiredMixin, ListView):
    """
    Displays a list of the customer bookings
    Get extra context: Passes extra context to the class based view to use
    """
    model = TimeSlot
    template_name = 'booking/customer_booking_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        context['timeslots'] = TimeSlot.objects.filter(user=self.request.user)
        return context


class CustomerBookingDetailView(LoginRequiredMixin, DetailView):
    """
    Displays details of the customer booking
    Get extra context: Passes extra context to the class based view to use
    """
    model = TimeSlot
    context_object_name = 'timeslots'
    template_name = 'booking/customer_booking_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context


class BookingDeleteView(LoginRequiredMixin, DeleteView):
    """
    Deletes booking chosen
    Get extra context: Passes extra context to the class based view to use
    Def delete: displays message item was deleted
    """
    model = TimeSlot
    template_name = 'booking/customer_booking_delete.html'
    success_message = 'Date deleted successfully!'
    success_url = reverse_lazy('customer_booking_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(BookingDeleteView, self).delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Booking'
        return context
