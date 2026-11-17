"""Configuration values for the recommendation engine."""

# Australian National Minimum Wage (AUD/hour).
# Reference period: 2026–2027.
NATIONAL_MINIMUM_HOURLY_WAGE = 26.44

# Assumed proportion of hourly wage used to value leisure time.
# This is a modelling assumption, not an official VTTS rate.
DEFAULT_TIME_VALUE_RATIO = 0.40

DEFAULT_VALUE_OF_TIME = round(
    NATIONAL_MINIMUM_HOURLY_WAGE * DEFAULT_TIME_VALUE_RATIO,
    2,
)