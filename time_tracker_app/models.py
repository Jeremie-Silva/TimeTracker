from django.db.models import Model, CASCADE, ForeignKey, ManyToManyField, PositiveSmallIntegerField, CharField, DurationField, TimeField
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime, timedelta


class Week(Model):
    user = ManyToManyField(to=User, related_name="weeks")
    week_number = PositiveSmallIntegerField()
    year = PositiveSmallIntegerField(default=2024)

    @property
    def objective(self):
        total_duration = self.days.aggregate(total=Sum('objective'))['total']
        return total_duration if total_duration is not None else "00:00:00"

    @property
    def score(self):
        total_duration = timedelta()
        for day in self.days.all():
            total_duration += day.result
        return total_duration

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
    def dataforge(self):
        return self.get_duration_by_label("Dataforge")

    @property
    def support(self):
        return self.get_duration_by_label("Support")

    @property
    def autre(self):
        return self.get_duration_by_label("Autre")

    @property
    def lundi(self):
        lundi_day = self.days.filter(name="Lundi").first()
        return lundi_day.result if lundi_day else timedelta(0)

    @property
    def mardi(self):
        lundi_day = self.days.filter(name="Mardi").first()
        return lundi_day.result if lundi_day else timedelta(0)

    @property
    def mercredi(self):
        lundi_day = self.days.filter(name="Mercredi").first()
        return lundi_day.result if lundi_day else timedelta(0)

    @property
    def jeudi(self):
        lundi_day = self.days.filter(name="Jeudi").first()
        return lundi_day.result if lundi_day else timedelta(0)

    def __str__(self):
        return f"Semaine n° {self.week_number} : {self.year}"


class Day(Model):
    week = ForeignKey(to=Week, on_delete=CASCADE, related_name="days")
    name = CharField(
        max_length=100, choices=(
            ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
            ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'),
        ))
    objective = DurationField(default="07:00:00")

    @property
    def result(self):
        total_duration = timedelta()
        for task in self.tasks.all():
            if task.start_time and task.end_time:
                duration = datetime.combine(
                    datetime.min, task.end_time
                ) - datetime.combine(datetime.min, task.start_time)
                total_duration += duration
        return total_duration


class Label(Model):
    name = CharField(max_length=100)

    def calculate_global_task_time(self):
        total_duration = timedelta()
        for task in Task.objects.all():
            if task.start_time and task.end_time:
                duration = datetime.combine(
                    datetime.min, task.end_time) - datetime.combine(datetime.min, task.start_time)
                total_duration += duration
        return total_duration

    @property
    def task_time_percentage(self):
        label_task_duration = timedelta()
        global_task_duration = self.calculate_global_task_time()
        for task in self.tasks.all():
            if task.start_time and task.end_time:
                duration = datetime.combine(datetime.min, task.end_time) - datetime.combine(datetime.min,
                                                                                            task.start_time)
                label_task_duration += duration
        if global_task_duration.total_seconds() == 0:
            return "No global tasks"
        percentage = (label_task_duration.total_seconds() / global_task_duration.total_seconds()) * 100
        return f"{percentage:.2f}%"

    def __str__(self):
        return self.name


class Task(Model):
    day = ForeignKey(to=Day, on_delete=CASCADE, related_name="tasks")
    label = ForeignKey(to=Label, on_delete=CASCADE, related_name="tasks")
    start_time = TimeField()
    end_time = TimeField(null=True, blank=True)

