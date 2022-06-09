from django.shortcuts import render
from .models import TimeSlot, Closed
from datetime import datetime

def booking_day(request):
    return render(request, 'booking/booking_day.html', {})

def booking_detail(request):
    
    if request.method == 'POST':
        date = request.POST.get('date')
        bookings = TimeSlot.objects.filter(date=date)
        days = Closed.objects.all()
        closed_days = []
        for day in days:
            closed_days.append(day.day.strftime("%Y-%m-%d"))
        if len(bookings) > 0:
            # my_list1 = []
            # new_list = []
            # for time in bookings.time:
            #     print(time)
            #     new_list.append(arr.count(i))
            # for num in new_list:
            #     if num > 2:
            #         index_of = new_list.index(num)
            #         my_list1.append(my_list[index_of])

            # my_list1 = list(dict.fromkeys(my_list1))
            # return my_list1
            # pass
        else:
            times = ['12:00', '13:00','14:00',
                    '15:00', '16:00', '17:00',
                    '18:00', '19:00', '20:00']

    return render(request, 'booking/booking_detail.html', 
                  {'bookings': bookings,
                   'date': date,
                   'times': times,
                   'closed_days': closed_days
                   })