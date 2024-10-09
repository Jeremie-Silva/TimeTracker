from django.db.models import Model, CASCADE, ForeignKey, ManyToManyField, PositiveSmallIntegerField, CharField, TimeField, IntegerField
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta


class Week(Model):
    user = ManyToManyField(to=User, related_name="weeks")
    week_number = PositiveSmallIntegerField()
    year = PositiveSmallIntegerField(default=2024)

    @property
    def objective(self):
        total_seconds = self.days.aggregate(total=Sum('objective'))['total']
        return timedelta(seconds=total_seconds) if total_seconds is not None else timedelta()

    @property
    def score(self):
        total_seconds = 0
        for day in self.days.all():
            total_seconds += day.result.total_seconds()
        return timedelta(seconds=total_seconds)

    @property
    def result(self):
        difference = self.score - self.objective
        difference_in_minutes = int(difference.total_seconds() / 60)
        return f"+{difference_in_minutes}mins" if difference_in_minutes >= 0 else f"{difference_in_minutes}mins"

    @property
    def start_date(self):
        first_day_of_year = datetime(self.year, 1, 1)
        year, week_num, weekday = first_day_of_year.isocalendar()
        week_difference = self.week_number - week_num
        first_day_of_week = first_day_of_year + timedelta(weeks=week_difference, days=-(weekday - 1))
        return first_day_of_week.strftime("%d %B %Y")

    @property
    def end_date(self):
        first_day_of_year = datetime(self.year, 1, 1)
        year, week_num, weekday = first_day_of_year.isocalendar()
        week_difference = self.week_number - week_num
        first_day_of_week = first_day_of_year + timedelta(weeks=week_difference, days=-(weekday - 1))
        last_day_of_week = first_day_of_week + timedelta(days=6)
        return last_day_of_week.strftime("%d %B %Y")

    def get_duration_by_label(self, label_name: str) -> str :
        label_duration = timedelta()
        total_duration = self.score  # Assuming score is the total duration of all tasks in the week
        if total_duration.total_seconds() == 0:
            return "0%"  # No tasks in the week
        for day in self.days.all():
            for task in day.tasks.filter(label__name=label_name):
                if task.start_time and task.end_time:
                    duration = datetime.combine(
                        datetime.min, task.end_time) - datetime.combine(datetime.min, task.start_time)
                    label_duration += duration

        percentage = (label_duration.total_seconds() / total_duration.total_seconds()) * 100
        return f"{percentage:.2f}%"

    @property
    def lundi(self):
        day = self.days.filter(name="Lundi").first()
        return day.result if day else timedelta(0)

    @property
    def mardi(self):
        day = self.days.filter(name="Mardi").first()
        return day.result if day else timedelta(0)

    @property
    def mercredi(self):
        day = self.days.filter(name="Mercredi").first()
        return day.result if day else timedelta(0)

    @property
    def jeudi(self):
        day = self.days.filter(name="Jeudi").first()
        return day.result if day else timedelta(0)

    @property
    def vendredi(self):
        day = self.days.filter(name="vendredi").first()
        return day.result if day else timedelta(0)

    def __str__(self):
        return f"Semaine n° {self.week_number} : {self.year}"


class Day(Model):
    week = ForeignKey(to=Week, on_delete=CASCADE, related_name="days")
    name = CharField(
        max_length=100, choices=(
            ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
            ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'),
        ))
    objective = IntegerField(default=26280)

    @property
    def result(self):
        total_seconds = 0
        for task in self.tasks.all():
            if task.start_time and task.end_time:
                duration = datetime.combine(
                    datetime.min, task.end_time
                ) - datetime.combine(datetime.min, task.start_time)
                total_seconds += duration.total_seconds()
        return timedelta(seconds=total_seconds)


class Label(Model):
    name = CharField(max_length=100)

    def calculate_global_task_time(self):
        total_seconds = 0
        for task in Task.objects.all():
            if task.start_time and task.end_time:
                duration = datetime.combine(
                    datetime.min, task.end_time) - datetime.combine(datetime.min, task.start_time)
                total_seconds += duration.total_seconds()
        return timedelta(seconds=total_seconds)

    @property
    def total_balance(self):
        total_balance_seconds = 0
        for week in Week.objects.all():
            for day in week.days.all():
                day_seconds = 0
                for task in day.tasks.filter(label=self):
                    if task.start_time and task.end_time:
                        duration = datetime.combine(datetime.min, task.end_time) - datetime.combine(datetime.min, task.start_time)
                        day_seconds += duration.total_seconds()
                day_balance_seconds = day_seconds - day.objective
                total_balance_seconds += day_balance_seconds
        hours, remainder = divmod(abs(total_balance_seconds), 3600)
        minutes = int(remainder // 60)

        # Ajouter le signe "+" ou "-" en fonction de la balance
        sign = "+" if total_balance_seconds >= 0 else "-"
        return f"{sign}{int(hours)}h {minutes}min"

    def __str__(self):
        return self.name


class Task(Model):
    day = ForeignKey(to=Day, on_delete=CASCADE, related_name="tasks")
    label = ForeignKey(to=Label, on_delete=CASCADE, related_name="tasks")
    start_time = TimeField()
    end_time = TimeField(null=True, blank=True)
