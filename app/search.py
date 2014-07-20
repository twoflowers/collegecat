from math import sin, cos, radians, acos
import requests, json
from app import app

from models import db, Price

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


class SearchTags():

    def filter_by_radius(self, user, tutor, radius):
        """
        @TODO Assumes user and tutor has .gps parameter that is a json string
        :param user:
        :param tutor:
        :param radius:
        :return:
        """
        user_gps = user.gps.split(',')
        user_gps = {'lat': user_gps[0], 'lon': user_gps[1]}
        tutor_gps = tutor.gps.split(',')
        tutor_gps = {'lat': tutor_gps[0], 'lon': tutor_gps[1]}
        distance = calc_dist_fixed(user_gps['lat'], user_gps['long'], tutor_gps['lat'], tutor_gps['long'])
        if distance <= radius:
            return distance
        else:
            return None

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

            distance = self.filter_by_radius(user, tutor, radius)
            if not distance:
                continue

            target_tags = [tag for tag in tutor.tags if search_term in tag]
            if not target_tags:
                continue

            if max_price:
                for tag in target_tags:
                    prices = db.session.query(Price).filter((Price.tag == tag) & (Price.price <= max_price))
                    if prices:
                        break
                else:
                    continue

            # Didn't get filtered out, so add them to the list
            filtered_tutors.append(tutor)

        return filtered_tutors
