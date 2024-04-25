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
        "lundi", "mardi", "mercredi", "jeudi", "formatted_score", "formatted_result",
        "dataforge", "autre", "support")
    fields = ("user", "week_number", "year")

    @display(description='Result')
    def formatted_result(self, obj):
        color = "green" if obj.result.startswith("+") else "coral"
        return format_html('<span style="color: {};">{}</span>', color, obj.result)

    def formatted_objective(self, obj):
        try:
            hours = int(obj.objective.total_seconds() // 3600)
            minutes = int((obj.objective.total_seconds() % 3600) // 60)
        except AttributeError:
            return ""
        return format_html('<span style="color: cornflowerblue;">{}h {}m</span>', hours, minutes)

    def formatted_score(self, obj):
        try:
            hours = int(obj.score.total_seconds() // 3600)
            minutes = int((obj.score.total_seconds() % 3600) // 60)
        except AttributeError:
            return ""
        return format_html('<span style="color: cornflowerblue;">{}h {}m</span>', hours, minutes)

    formatted_objective.short_description = "objective"
    formatted_score.short_description = "score"
    formatted_result.short_description = "result"


@register(Label)
class LabelAdmin(NestedModelAdmin):
    list_display = ("name", "task_time_percentage")
    fields = ("name",)
