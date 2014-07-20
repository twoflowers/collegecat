from math import sin, cos, radians, acos
import requests, json
from app import app
import errors
from models import db, Price, User, Rating

from sqlalchemy import func

# http://en.wikipedia.org/wiki/Earth_radius
"""For Earth, the mean radius is 6,371.009 km (3,958.761 mi; 3,440.069 nmi)"""
EARTH_RADIUS_IN_MILES = 3958.761


def calc_dist_fixed(lat_a, lon_a, lat_b, lon_b):
    """
    all angles in degrees, result in miles
    found at http://stackoverflow.com/questions/4716017/django-how-can-i-find-the-distance-between-two-locations

    :param lat_a:
    :param lon_a:
    :param lat_b:
    :param lon_b:
    :return:
    """
    lat_a = float(str(lat_a))
    lon_a = float(str(lon_a))
    lat_b = float(str(lat_b))
    lon_b = float(str(lon_b))
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    delta_lon = radians(lon_a - lon_b)
    cos_x = (
        sin(lat_a) * sin(lat_b) +
        cos(lat_a) * cos(lat_b) * cos(delta_lon)
    )
    return acos(cos_x) * EARTH_RADIUS_IN_MILES


class SearchTags(object):

    def filter_by_radius(self, user_gps, tutor, radius):
        """
        @TODO Assumes user and tutor has .gps parameter that is a json string
        :param user:
        :param tutor:
        :param radius:
        :return:
        """
        for tutor_loc in tutor.loc:
            tutor_gps = tutor_loc.gps.split(',')
            tutor_gps = {'lat': tutor_gps[0], 'lon': tutor_gps[1]}
            distance = calc_dist_fixed(user_gps['lat'], user_gps['lon'], tutor_gps['lat'], tutor_gps['lon'])
            if distance <= radius:
                return distance
            else:
                return None

    def query(self, user_gps, search_term=None, radius=30, max_price=None, min_rating=0):
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

        filtered_tutors = []
        potential_tutors = db.session.query(User).filter_by(tutor=True).all()
        for tutor in potential_tutors:
            distance = self.filter_by_radius(user_gps=user_gps, tutor=tutor, radius=radius)
            if not distance:
                continue

            tags = tutor.tags.all()

            if search_term: # remove queries that don't result in terms
                target_tags = [tag for tag in tags if search_term.lower() in tag.name.lower()]
                if not target_tags:
                    continue
            else:  # no filtering via search_term so preserve all tags
                target_tags = tags

            if max_price is not None:  # remove queries that don't fit in budget
                max_price = float(max_price)
                for tag in target_tags:
                    prices = db.session.query(Price).filter_by(tag=tag.id).all()
                    prices = [price.price for price in prices if price.price <= max_price]
                    if prices:
                        break
                else:
                    continue

            # Didn't get filtered out, so add them to the list
            formatted_tutor = dict(tutor.serialize)
            ratings = db.session.query(Rating).filter_by(tutor=tutor.id).all()
            print "Ratings %r" % ratings
            formatted_tutor.update(rating=sum([float(rating.rating) for rating in ratings])/len(ratings) if ratings else 0)
            if formatted_tutor['rating'] >= min_rating:
                formatted_tutor.update(distance=distance)
                filtered_tutors.append(formatted_tutor)
        return filtered_tutors
