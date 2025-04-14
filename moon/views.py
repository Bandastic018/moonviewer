# moon/views.py
import os
import math
import ephem
from datetime import datetime, timezone
from django.shortcuts import render
from django.templatetags.static import static
from geopy.geocoders import Nominatim

# --- Dictionary of World Capital Cities (partial list; extend as desired) ---
world_capitals = {
     "Select Capital": None,
    "Kabul, Afghanistan": (34.5553, 69.2075),
    "Tirana, Albania": (41.3275, 19.8189),
    "Algiers, Algeria": (36.7538, 3.0588),
    "Andorra la Vella, Andorra": (42.5063, 1.5218),
    "Luanda, Angola": (-8.8383, 13.2344),
    "Buenos Aires, Argentina": (-34.6037, -58.3816),
    "Yerevan, Armenia": (40.1811, 44.5136),
    "Vienna, Austria": (48.2082, 16.3738),
    "Baku, Azerbaijan": (40.4093, 49.8671),
    "Nassau, Bahamas": (25.0343, -77.3963),
    "Manama, Bahrain": (26.2235, 50.5876),
    "Dhaka, Bangladesh": (23.8103, 90.4125),
    "Bridgetown, Barbados": (13.0975, -59.6167),
    "Minsk, Belarus": (53.9006, 27.5590),
    "Brussels, Belgium": (50.8503, 4.3517),
    "Belmopan, Belize": (17.2528, -88.7713),
    "Porto-Novo, Benin": (6.4833, 2.6167),
    "Thimphu, Bhutan": (27.4728, 89.6390),
    "La Paz, Bolivia": (-16.4897, -68.1193),  # Note: Sucre is constitutional
    "Sarajevo, Bosnia and Herzegovina": (43.8486, 18.3954),
    "Gaborone, Botswana": (-24.6282, 25.9231),
    "Brasília, Brazil": (-15.7939, -47.8828),
    "Sofia, Bulgaria": (42.6977, 23.3219),
    "Ouagadougou, Burkina Faso": (12.3714, -1.5197),
    "Gitega, Burundi": (-3.4264, 29.9227),
    "Phnom Penh, Cambodia": (11.5564, 104.9282),
    "Yaoundé, Cameroon": (3.8480, 11.5021),
    "Ottawa, Canada": (45.4215, -75.6972),
    "Bangui, Central African Republic": (4.3676, 18.5572),
    "N'Djamena, Chad": (12.1348, 15.0557),
    "Santiago, Chile": (-33.4489, -70.6693),
    "Beijing, China": (39.9042, 116.4074),
    "Bogotá, Colombia": (4.7110, -74.0721),
    "Moroni, Comoros": (-11.7172, 43.2473),
    "Brazzaville, Republic of the Congo": (-4.2634, 15.2429),
    "Kinshasa, Democratic Republic of the Congo": (-4.4419, 15.2663),
    "San José, Costa Rica": (9.9281, -84.0907),
    "Zagreb, Croatia": (45.8150, 15.9819),
    "Havana, Cuba": (23.1136, -82.3666),
    "Nicosia, Cyprus": (35.1856, 33.3823),
    "Prague, Czech Republic": (50.0755, 14.4378),
    "Copenhagen, Denmark": (55.6761, 12.5683),
    "Cairo, Egypt": (30.0444, 31.2357),
    "San Salvador, El Salvador": (13.6929, -89.2182),
    "Malabo, Equatorial Guinea": (3.7500, 8.7833),
    "Asmara, Eritrea": (15.3229, 38.9251),
    "Tallinn, Estonia": (59.4370, 24.7536),
    "Mbabane, Eswatini": (-26.3055, 31.1367),
    "Addis Ababa, Ethiopia": (8.9806, 38.7578),
    "Suva, Fiji": (-18.1248, 178.4501),
    "Helsinki, Finland": (60.1699, 24.9384),
    "Paris, France": (48.8566, 2.3522),
    "Libreville, Gabon": (0.3901, 9.4544),
    "Banjul, Gambia": (13.4549, -16.5790),
    "Tbilisi, Georgia": (41.7151, 44.8271),
    "Berlin, Germany": (52.5200, 13.4050),
    "Accra, Ghana": (5.6037, -0.1870),
    "Athens, Greece": (37.9838, 23.7275),
    "St. George's, Grenada": (12.0561, -61.7489),
    "Guatemala City, Guatemala": (14.6349, -90.5069),
    "Conakry, Guinea": (9.6412, -13.5784),
    "Bissau, Guinea-Bissau": (11.8817, -15.6170),
    "Georgetown, Guyana": (6.8013, -58.1551),
    "Port-au-Prince, Haiti": (18.5392, -72.3360),
    "Tegucigalpa, Honduras": (14.0723, -87.1921),
    "Budapest, Hungary": (47.4979, 19.0402),
    "Reykjavik, Iceland": (64.1466, -21.9426),
    "New Delhi, India": (28.6139, 77.2090),
    "Jakarta, Indonesia": (-6.2088, 106.8456),
    "Tehran, Iran": (35.6892, 51.3890),
    "Baghdad, Iraq": (33.3128, 44.3615),
    "Dublin, Ireland": (53.3498, -6.2603),
    "Jerusalem, Israel": (31.7683, 35.2137),
    "Rome, Italy": (41.9028, 12.4964),
    "Kingston, Jamaica": (18.0179, -76.8099),
    "Amman, Jordan": (31.9454, 35.9284),
    "Nur-Sultan, Kazakhstan": (51.1605, 71.4704),
    "Nairobi, Kenya": (-1.2921, 36.8219),
    "Tarawa, Kiribati": (1.4518, 173.0330),
    "Pristina, Kosovo": (42.6629, 21.1655),
    "Kuwait City, Kuwait": (29.3117, 47.4818),
    "Bishkek, Kyrgyzstan": (42.8746, 74.5698),
    "Vientiane, Laos": (17.9757, 102.6331),
    "Riga, Latvia": (56.9496, 24.1052),
    "Beirut, Lebanon": (33.8938, 35.5018),
    "Maseru, Lesotho": (-29.3634, 27.5142),
    "Monrovia, Liberia": (6.3156, -10.8070),
    "Tripoli, Libya": (32.8872, 13.1913),
    "Vaduz, Liechtenstein": (47.1410, 9.5209),
    "Vilnius, Lithuania": (54.6872, 25.2797),
    "Luxembourg, Luxembourg": (49.6116, 6.1319),
    "Skopje, North Macedonia": (41.9963, 21.4314),
    "Antananarivo, Madagascar": (-18.8792, 47.5079),
    "Lilongwe, Malawi": (-13.9626, 33.7741),
    "Kuala Lumpur, Malaysia": (3.1390, 101.6869),
    "Malé, Maldives": (4.1755, 73.5093),
    "Bamako, Mali": (12.6392, -8.0029),
    "Valletta, Malta": (35.8989, 14.5146),
    "Majuro, Marshall Islands": (7.0674, 171.2729),
    "Nouakchott, Mauritania": (18.0735, -15.9582),
    "Port Louis, Mauritius": (-20.1667, 57.5000),
    "Mexico City, Mexico": (19.4326, -99.1332),
    "Chisinau, Moldova": (47.0105, 28.8638),
    "Monaco, Monaco": (43.7384, 7.4246),
    "Ulaanbaatar, Mongolia": (47.8864, 106.9057),
    "Podgorica, Montenegro": (42.4304, 19.2594),
    "Rabat, Morocco": (34.0209, -6.8416),
    "Maputo, Mozambique": (-25.9692, 32.5732),
    "Naypyidaw, Myanmar": (19.7633, 96.0785),
    "Windhoek, Namibia": (-22.5594, 17.0831),
    "Yaren, Nauru": (-0.5477, 166.9209),
    "Kathmandu, Nepal": (27.7172, 85.3240),
    "Amsterdam, Netherlands": (52.3676, 4.9041),
    "Wellington, New Zealand": (-41.2865, 174.7762),
    "Managua, Nicaragua": (12.1140, -86.2362),
    "Niamey, Niger": (13.5116, 2.1254),
    "Abuja, Nigeria": (9.0765, 7.3986),
    "Pyongyang, North Korea": (39.0194, 125.7383),
    "Oslo, Norway": (59.9139, 10.7522),
    "Islamabad, Pakistan": (33.6844, 73.0479),
    "Ngerulmud, Palau": (7.5000, 134.6242),
    "Panama City, Panama": (8.9824, -79.5199),
    "Port Moresby, Papua New Guinea": (-9.4438, 147.1803),
    "Asunción, Paraguay": (-25.2637, -57.5759),
    "Lima, Peru": (-12.0464, -77.0428),
    "Manila, Philippines": (14.5995, 120.9842),
    "Warsaw, Poland": (52.2297, 21.0122),
    "Lisbon, Portugal": (38.7223, -9.1393),
    "Doha, Qatar": (25.2854, 51.5310),
    "Bucharest, Romania": (44.4268, 26.1025),
    "Moscow, Russia": (55.7558, 37.6173),
    "Kigali, Rwanda": (1.9441, 30.0619),
    "Basseterre, Saint Kitts and Nevis": (17.3099, -62.7170),
    "Castries, Saint Lucia": (14.0101, -60.9875),
    "Kingstown, Saint Vincent and the Grenadines": (13.1600, -61.2248),
    "Apia, Samoa": (-13.8500, -171.7500),
    "San Marino, San Marino": (43.9424, 12.4578),
    "São Tomé, São Tomé and Príncipe": (0.3365, 6.7343),
    "Riyadh, Saudi Arabia": (24.7136, 46.6753),
    "Dakar, Senegal": (14.7167, -17.4677),
    "Belgrade, Serbia": (44.7866, 20.4489),
    "Victoria, Seychelles": (-4.6191, 55.4513),
    "Freetown, Sierra Leone": (8.4844, -13.2344),
    "Singapore, Singapore": (1.3521, 103.8198),
    "Bratislava, Slovakia": (48.1486, 17.1077),
    "Ljubljana, Slovenia": (46.0569, 14.5058),
    "Caracas, Venezuela": (10.4806, -66.9036),
    "Hanoi, Vietnam": (21.0278, 105.8342),
    "Sana'a, Yemen": (15.3694, 44.1910),
    "Lusaka, Zambia": (-15.3875, 28.3228),
    "Harare, Zimbabwe": (-17.8252, 31.0335)
}


def get_moon_details(lat, lon, dt):
    """
    Calculates Moon details for the given coordinates and forecast datetime (dt).
    dt must be a timezone-aware datetime in UTC.
    Returns a dictionary with: phase (% illumination), moonrise, moonset,
    age (in days), altitude (degrees), and a viewing recommendation.
    """
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.date = dt  # use forecast datetime (UTC)
    print(f"[DEBUG] Observer: lat={lat}, lon={lon}, datetime={observer.date}")

    moon = ephem.Moon(observer)
    moon_phase = moon.phase  # percentage illumination

    # Compute moonrise and moonset (if available – catch exceptions for some regions)
    try:
        moonrise = observer.next_rising(moon).datetime().replace(tzinfo=timezone.utc)
    except Exception:
        moonrise = None
    try:
        moonset = observer.next_setting(moon).datetime().replace(tzinfo=timezone.utc)
    except Exception:
        moonset = None
# COMPUTE MOON vISIBILITY

    is_visible= False
    if moon.alt > 0:    #Check Altitude first

        if moonrise and moonset :
            is_visible= moonrise<= dt <= moonset
            
   # is_visible = False
    #if moonrise and moonset:
     #   is_visible = (moonrise <= dt <= moonset)

    #is_visible = False
    #if moonrise and moonset:
     #   is_visible = (moonrise <= dt <= moonset) and (moon.alt > 0)

    print(f"[DEBUG] Moonrise: {moonrise}, Moonset: {moonset}, Altitude: {moon.alt}")
    print(f"[DEBUG] Moon Altitude: {moon.alt} radians, {float(moon.alt) * 180 / math.pi:.2f} degrees")
 
    # Calculate Moon age in days (since the last new moon)
    current_date = ephem.Date(dt)
    last_new = ephem.previous_new_moon(current_date)
    moon_age = float(current_date - last_new)

    # Get Moon's altitude (in degrees)
    alt_deg = float(moon.alt) * 180 / math.pi

    # Viewing recommendation:
    if not is_visible:
        viewing = "Moon will not be visible at the selected time."
    else:
        if alt_deg >= 30:
            viewing = "Visible with the naked eye."
        elif alt_deg >= 10:
            viewing = "Visible with an optical lens (binoculars or small telescope recommended)."
        else:
            viewing = "Moon is very low; an advanced instrument is recommended."

    return {
        "phase": moon_phase,
        "moonrise": moonrise,
        "moonset": moonset,
        "visible": is_visible,
        "age": moon_age,
        "altitude": alt_deg,
        "viewing": viewing
    }

def get_moon_phase_name(phase):
    """Return the common name for the Moon phase based on illumination percentage."""
    if phase < 10:
        return "New Moon"
    elif phase < 40:
        return "Waxing Crescent"
    elif phase < 50:
        return "First Quarter"
    elif phase < 60:
        return "Waxing Gibbous"
    elif phase < 80:
        return "Full Moon"
    elif phase < 90:
        return "Waning Gibbous"
    elif phase < 97:
        return "Last Quarter"
    else:
        return "Waning Crescent"

def get_moon_image_path(phase):
    """
    Returns the relative path (under the static folder) to the image file
    corresponding to the Moon phase.
    """
    if phase < 10:
        return os.path.join("images", "new_moon.png")
    elif phase < 40:
        return os.path.join("images", "waxing_crescent.png")
    elif phase < 50:
        return os.path.join("images", "first_quarter.png")
    elif phase < 60:
        return os.path.join("images", "waxing_gibbous.png")
    elif phase < 80:
        return os.path.join("images", "full_moon.png")
    elif phase < 90:
        return os.path.join("images", "waning_gibbous.png")
    elif phase < 97:
        return os.path.join("images", "last_quarter.png")
    else:
        return os.path.join("images", "waning_crescent.png")

def index(request):
    result = None
    error = None
    if request.method == "POST":
        # Determine coordinates
        try:
            capital = request.POST.get("capital")
            loc_query = request.POST.get("location_query")
            if capital and capital != "Select Capital" and capital in world_capitals:
                lat, lon = world_capitals[capital]
            elif loc_query:
                geolocator = Nominatim(user_agent="moon_viewer_app")
                location = geolocator.geocode(loc_query)
                if location:
                    lat, lon = location.latitude, location.longitude
                else:
                    error = "Location not found."
            else:
                lat = float(request.POST.get("latitude"))
                lon = float(request.POST.get("longitude"))
        except Exception as e:
            error = "Error obtaining coordinates: " + str(e)

        # Parse forecast datetime
        dt_str = request.POST.get("datetime")
        try:
            if dt_str.strip():
                dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = datetime.now(timezone.utc)
        except Exception as e:
            error = "Error parsing datetime. Use YYYY-MM-DD HH:MM format."

        if not error:
            details = get_moon_details(lat, lon, dt)
            phase_name = get_moon_phase_name(details["phase"])
            # Get desired moon age unit and convert
            age_unit = request.POST.get("age_unit")
            if age_unit == "Days":
                age_display = details["age"]
            elif age_unit == "Hours":
                age_display = details["age"] * 24
            elif age_unit == "Minutes":
                age_display = details["age"] * 1440
            elif age_unit == "Seconds":
                age_display = details["age"] * 86400
            else:
                age_display = details["age"]

            result = {
                "phase_percent": f"{details['phase']:.2f}",
                "phase_name": phase_name,
                "moon_age": f"{age_display:.2f} {age_unit}",
                "moonrise": details["moonrise"],
                "moonset": details["moonset"],
                "viewing": details["viewing"],
                "altitude": f"{details['altitude']:.2f}",
                "visible": details["visible"]
            }
            
            img_rel_path = get_moon_image_path(details["phase"])
            result["img_url"] = static(img_rel_path)

            
    return render(request, "moon/index.html", {"result": result, "error": error, "capitals": world_capitals})

   