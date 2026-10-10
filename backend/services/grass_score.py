from typing import Dict, Any, Optional

# Piecewise interpolation knots for World / Screen Ratio to base score [0, 100]
# Each tuple is (ratio_value, base_points)
RATIO_KNOTS = [
    (0.0, 10.0),
    (1.0, 25.0),
    (2.0, 40.0),
    (3.0, 55.0),
    (4.0, 63.0),
    (5.0, 70.0),
    (7.0, 79.0),
    (10.0, 90.0),
    (20.0, 100.0)
]

# Knots for Phone-Free Field Time in seconds to points [0, 10]
FIELD_TIME_KNOTS = [
    (0, 0.0),
    (30, 3.0),
    (60, 5.0),
    (120, 7.0),
    (300, 8.5),
    (600, 10.0)
]

def format_duration(seconds: int) -> str:
    """Format seconds into human readable time (e.g., '4m 21s' or '38s')."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    rem = seconds % 60
    if rem > 0:
        return f"{minutes}m {rem}s"
    return f"{minutes}m"

def interpolate_piecewise(val: float, knots: list) -> float:
    """Smooth piecewise linear interpolation across monotonically increasing knots."""
    if val <= knots[0][0]:
        return knots[0][1]
    if val >= knots[-1][0]:
        return knots[-1][1]

    for i in range(len(knots) - 1):
        x0, y0 = knots[i]
        x1, y1 = knots[i + 1]
        if x0 <= val <= x1:
            if x1 == x0:
                return y0
            return y0 + (val - x0) / (x1 - x0) * (y1 - y0)
    return knots[-1][1]

def calculate_ratio_score(
    ratio_or_world: float,
    screen_time_seconds: Optional[int] = None
) -> float:
    """
    Calculates the 70% World/Screen Ratio component.
    Max points: 70.
    Can be called with either (ratio: float) or (world_time_seconds, screen_time_seconds).
    Uses bounded piecewise mapping to prevent high ratios from immediately yielding 100.
    """
    if screen_time_seconds is not None:
        safe_screen = max(screen_time_seconds, 1)
        ratio = max(0.0, float(ratio_or_world) / safe_screen)
    else:
        ratio = max(0.0, float(ratio_or_world))

    ratio = round(ratio, 2)
    base_points = interpolate_piecewise(ratio, RATIO_KNOTS)
    return round((base_points / 100.0) * 70.0, 2)

def calculate_mission_score(
    is_completed: bool = True,
    mission_completed: Optional[bool] = None
) -> float:
    """
    Calculates the 15% Mission Completion component.
    15 points if completed, 0 if abandoned.
    """
    completed = mission_completed if mission_completed is not None else is_completed
    return 15.0 if completed else 0.0

def calculate_field_time_score(field_time_seconds: int) -> float:
    """
    Calculates the 10% Phone-Free Field Time component.
    Max points: 10.
    Bounded between 0 and 10 based on duration spent away from screens.
    """
    safe_time = max(0, field_time_seconds)
    return round(interpolate_piecewise(safe_time, FIELD_TIME_KNOTS), 2)

def calculate_reflection_score(
    user_observation: Optional[str] = None,
    has_observation: Optional[bool] = None
) -> float:
    """
    Calculates the 5% Reflection component.
    Max points: 5.
    - 0: Empty / no reflection
    - 2: Very short (< 15 chars or under 3 words)
    - 4: Meaningful observation (>= 15 chars)
    - 5: Meaningful observation + curiosity reflection
    """
    clean_obs = user_observation.strip() if user_observation else ""

    if not clean_obs:
        return 4.0 if has_observation else 0.0

    words = clean_obs.split()
    if len(clean_obs) < 15 or len(words) < 3:
        return 2.0

    # Meaningful observation + curiosity investigation (contains '?' or curiosity marker words)
    curiosity_markers = ["?", "wonder", "curious", "why", "how", "notice", "what"]
    has_curiosity = any(marker in clean_obs.lower() for marker in curiosity_markers)

    if has_curiosity:
        return 5.0

    return 4.0

def calculate_grass_score(
    screen_time_seconds: int,
    field_time_seconds: int,
    user_observation: Optional[str] = None,
    has_observation: Optional[bool] = None,
    is_completed: bool = True,
    mission_completed: Optional[bool] = None,
    phone_free_seconds: Optional[int] = None
) -> Dict[str, Any]:
    """
    Computes an explainable, reproducible, evidence-based Grass Score (0-100).
    Weighted components:
      - 70% World / Screen Ratio (0 to 70 points)
      - 15% Mission Completion (0 or 15 points)
      - 10% Phone-Free Field Time (0 to 10 points)
      -  5% Reflection (0 to 5 points)
    """
    completed = mission_completed if mission_completed is not None else is_completed
    actual_phone_free = phone_free_seconds if phone_free_seconds is not None else field_time_seconds

    # 1. Independent component calculations
    safe_screen = max(screen_time_seconds, 1)
    raw_ratio = max(0.0, field_time_seconds / safe_screen)
    ratio_val = round(raw_ratio, 2)

    ratio_score_raw = calculate_ratio_score(ratio_val)
    mission_score_raw = calculate_mission_score(completed)
    field_time_score_raw = calculate_field_time_score(actual_phone_free)
    reflection_score_raw = calculate_reflection_score(user_observation, has_observation)

    ratio_points = round(ratio_score_raw)
    mission_points = round(mission_score_raw)
    field_time_points = round(field_time_score_raw)
    reflection_points = round(reflection_score_raw)

    # 2. Total score calculation and bounding
    raw_total = (
        ratio_score_raw +
        mission_score_raw +
        field_time_score_raw +
        reflection_score_raw
    )
    final_score = round(max(0.0, min(100.0, raw_total)))

    ratio_formatted = f"{ratio_val:.1f}×" if ratio_val < 10 else f"{round(ratio_val)}×"

    # 3. Qualitative Naturalist Verdict
    if final_score >= 85:
        verdict = "True Field Naturalist 🌿"
    elif final_score >= 70:
        verdict = "Dedicated Observer 🍃"
    elif final_score >= 50:
        verdict = "Ground Explorer 🌲"
    else:
        verdict = "Screen Leaning 📱"

    explanation = f"You spent {ratio_formatted} more time exploring than looking at your screen."

    return {
        "score": final_score,
        "grass_score": final_score,  # Backward compatibility
        "breakdown": {
            "ratio_points": ratio_points,
            "mission_points": mission_points,
            "field_time_points": field_time_points,
            "reflection_points": reflection_points,
            "max_ratio_points": 70,
            "max_mission_points": 15,
            "max_field_time_points": 10,
            "max_reflection_points": 5,
            "raw_ratio_points": ratio_score_raw,
            "raw_field_time_points": field_time_score_raw
        },
        "metrics": {
            "world_time_seconds": field_time_seconds,
            "screen_time_seconds": screen_time_seconds,
            "world_screen_ratio": ratio_val,
            "mission_completed": completed,
            "phone_free_seconds": actual_phone_free,
            "reflection_completed": bool(user_observation or has_observation)
        },
        # Backward-compatible fields
        "screen_time_seconds": screen_time_seconds,
        "field_time_seconds": field_time_seconds,
        "screen_time_formatted": format_duration(screen_time_seconds),
        "field_time_formatted": format_duration(field_time_seconds),
        "ratio": ratio_val,
        "ratio_formatted": ratio_formatted,
        "verdict": verdict,
        "explanation": explanation
    }
