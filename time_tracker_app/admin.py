from django.contrib.admin import register
from nested_admin import NestedTabularInline, NestedModelAdmin
from django.contrib.admin import display
from django.utils.html import format_html
from .models import Week, Day, Task, Label


class TaskInline(NestedTabularInline):
    model = Task
    extra = 0


class DayInline(NestedTabularInline):
    model = Day
    extra = 0
    inlines = [TaskInline]


@register(Week)
class WeekAdmin(NestedModelAdmin):
    inlines = [DayInline]
    list_display = ("start_date", "end_date", "week_number", "formatted_objective",
        "lundi", "mardi", "mercredi", "jeudi", "vendredi", "formatted_score", "formatted_result",)
    fields = ("user", "week_number", "year")

    @display(description='Result')
    def formatted_result(self, obj):
        total_seconds = obj.score.total_seconds() - obj.objective.total_seconds()

        color = "green" if total_seconds >= 0 else "orange"
        hours, remainder = divmod(abs(total_seconds), 3600)
        minutes = int(remainder // 60)
        sign = "+" if total_seconds >= 0 else "-"
        return format_html('<span style="color: {};">{}h {}min</span>', color, sign + str(int(hours)), minutes)

    def formatted_objective(self, obj):
        total_seconds = obj.objective.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes = int(remainder // 60)
        return format_html('<span style="color: cornflowerblue;">{}h {}min</span>', int(hours), minutes)

    def formatted_score(self, obj):
        total_seconds = obj.score.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes = int(remainder // 60)
        return format_html('<span style="color: cornflowerblue;">{}h {}min</span>', int(hours), minutes)

    @display(description='Lundi')
    def lundi(self, obj):
        lundi_day = obj.days.filter(name="Lundi").first()
        if lundi_day:
            total_seconds = lundi_day.result.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes = int(remainder // 60)
            # Récupérer l'objectif journalier en secondes
            objective_seconds = lundi_day.objective
            # Comparer avec le résultat et choisir la couleur
            color = "green" if total_seconds >= objective_seconds else "orange"
            return format_html('<span style="color: {};">{}h {}min</span>', color, int(hours), minutes)
        return "0h 0min"

    @display(description='Mardi')
    def mardi(self, obj):
        mardi_day = obj.days.filter(name="Mardi").first()
        if mardi_day:
            total_seconds = mardi_day.result.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes = int(remainder // 60)
            # Récupérer l'objectif journalier en secondes
            objective_seconds = mardi_day.objective
            # Comparer avec le résultat et choisir la couleur
            color = "green" if total_seconds >= objective_seconds else "orange"
            return format_html('<span style="color: {};">{}h {}min</span>', color, int(hours), minutes)
        return "0h 0min"

    @display(description='Mercredi')
    def mercredi(self, obj):
        mercredi_day = obj.days.filter(name="Mercredi").first()
        if mercredi_day:
            total_seconds = mercredi_day.result.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes = int(remainder // 60)
            # Récupérer l'objectif journalier en secondes
            objective_seconds = mercredi_day.objective
            # Comparer avec le résultat et choisir la couleur
            color = "green" if total_seconds >= objective_seconds else "orange"
            return format_html('<span style="color: {};">{}h {}min</span>', color, int(hours), minutes)
        return "0h 0min"

    @display(description='Jeudi')
    def jeudi(self, obj):
        jeudi_day = obj.days.filter(name="Jeudi").first()
        if jeudi_day:
            total_seconds = jeudi_day.result.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes = int(remainder // 60)
            # Récupérer l'objectif journalier en secondes
            objective_seconds = jeudi_day.objective
            # Comparer avec le résultat et choisir la couleur
            color = "green" if total_seconds >= objective_seconds else "orange"
            return format_html('<span style="color: {};">{}h {}min</span>', color, int(hours), minutes)
        return "0h 0min"

    @display(description='Vendredi')
    def vendredi(self, obj):
        vendredi_day = obj.days.filter(name="Vendredi").first()
        if vendredi_day:
            total_seconds = vendredi_day.result.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes = int(remainder // 60)
            # Récupérer l'objectif journalier en secondes
            objective_seconds = vendredi_day.objective
            # Comparer avec le résultat et choisir la couleur
            color = "green" if total_seconds >= objective_seconds else "orange"
            return format_html('<span style="color: {};">{}h {}min</span>', color, int(hours), minutes)
        return "0h 0min"


    formatted_objective.short_description = "objective"
    formatted_score.short_description = "score"
    formatted_result.short_description = "result"


@register(Label)
class LabelAdmin(NestedModelAdmin):
    list_display = ("name", "total_balance")
    fields = ("name",)

