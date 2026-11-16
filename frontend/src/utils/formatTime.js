/**
 * Convert decimal hours to hours and minutes.
 *
 * Example:
 * 46.333333333333336 -> "46h 20m"
 */
export function formatUsableHours(hours) {
  if (hours == null || !Number.isFinite(Number(hours))) {
    return "N/A";
  }

  const totalMinutes = Math.round(Number(hours) * 60);
  const wholeHours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;

  return `${wholeHours}h ${minutes}m`;
}
