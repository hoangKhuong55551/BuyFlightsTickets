from django import template

register = template.Library()


@register.filter
def flight_duration(departure, arrival):
    """
    Returns compact duration string like "1h 20m" given two datetime objects.
    Usage: {{ booking.flight.departure_time|flight_duration:booking.flight.arrival_time }}
    """
    if not departure or not arrival:
        return ""
    delta = arrival - departure
    total_minutes = int(delta.total_seconds() // 60)
    if total_minutes <= 0:
        return ""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if hours and minutes:
        return f"{hours}h {minutes}m"
    elif hours:
        return f"{hours}h"
    else:
        return f"{minutes}m"
@register.filter
def vnd_format(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except (ValueError, TypeError):
        return value
