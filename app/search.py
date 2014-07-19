from math import sin, cos, radians, acos
import requests, json
from app import app

# http://en.wikipedia.org/wiki/Earth_radius
"""For Earth, the mean radius is 6,371.009 km (˜3,958.761 mi; ˜3,440.069 nmi)"""
EARTH_RADIUS_IN_MILES = 3958.761


def calc_dist_fixed(lat_a, long_a, lat_b, long_b):
    """
    all angles in degrees, result in miles
    found at http://stackoverflow.com/questions/4716017/django-how-can-i-find-the-distance-between-two-locations

    :param lat_a:
    :param long_a:
    :param lat_b:
    :param long_b:
    :return:
    """
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_long = radians(long_a - long_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_long)
    )
    return acos(cos_x) * EARTH_RADIUS_IN_MILES


class search_tutors():
    class TUTOR_OUT_OF_RADIUS(Exception):
        pass

    def __init__(self):
        pass

    def filter_by_radius(self, user, tutor, radius):
        """
        @TODO Assumes user and tutor has .gps parameter that is a json string
        :param user:
        :param tutor:
        :param radius:
        :return:
        """
        user_gps  = json.loads(user.gps)
        tutor_gps = json.loads(tutor.gps)
        distance = calc_dist_fixed(user_gps['lat'], user_gps['long'], tutor_gps['lat'], tutor_gps['long'])
        if distance > radius:
            raise self.TUTOR_OUT_OF_RADIUS
        else:
            return distance

    def search(self, user, search_term=None, radius=30, max_price=None):
        """
        filter_by using subject
        loop through results
            - calc distance between user's location and tutor's location(s)
                - filter out > radius
            - filter out > max_price

        :param search_term:
        :param user:
        :param radius:
        :param max_price:
        :return:
        """
        potential_tutors = []
        filtered_tutors = []
        # @TODO: Search mysql
        for tutor in potential_tutors:
            try:
                tutor['distance'] = self.filter_by_radius(user, tutor, radius)
            except self.TUTOR_OUT_OF_RADIUS:
                # Tutor too far away, yo
                continue

            if not search_term in tutor.subjects:
                continue

            if max_price and tutor.price >= max_price:
                continue

            # Didn't get filtered out, so add them to the list
            filtered_tutors.append(tutor)

        return filtered_tutors
