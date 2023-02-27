from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D


def set_point_field(validated_data):
    try:
        old_validated_data = validated_data
        pnt = GEOSGeometry(
            'POINT('+validated_data['location_lat']+' '+validated_data['location_long']+')', srid=4326)
        validated_data['point'] = pnt
        return validated_data
    except Exception as e:
        print(e)
        return old_validated_data
