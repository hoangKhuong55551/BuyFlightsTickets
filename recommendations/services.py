def price_score(price, min_price, max_price):

    if max_price == min_price:
        return 100

    score = (
        (max_price - price)
        / (max_price - min_price)
    ) * 100

    return max(0, min(100, score))
def duration_score(duration_minutes):

    max_duration = 600

    score = (
        (max_duration - duration_minutes)
        / max_duration
    ) * 100

    return max(
        0,
        min(100, score)
    )
def fatigue_score(flight):

    score = 100

    hour = flight.departure_time.hour

    if hour < 6:
        score -= 25

    if hour >= 22:
        score -= 25

    return max(score, 0)
def weather_score(weather_condition):

    if weather_condition == "clear":
        return 100

    if weather_condition == "cloudy":
        return 80

    if weather_condition == "rain":
        return 60

    if weather_condition == "storm":
        return 30

    return 70
def recommendation_score(
    price,
    duration,
    weather,
    fatigue
):

    return (
        price * 0.4
        + duration * 0.2
        + weather * 0.2
        + fatigue * 0.2
    )