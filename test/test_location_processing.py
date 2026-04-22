import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add project root and lib to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "lib"))

from lib.location import location_processing, NOT_FOUND_LOCATION

class TestLocationProcessing(unittest.TestCase):

    def setUp(self):
        self.patch_location = patch('lib.location._get_location')
        self.patch_geolocator = patch('lib.location._geolocator')
        self.patch_gethost = patch('lib.location.socket.gethostbyname')
        self.patch_hemisphere = patch('lib.location._get_hemisphere')
        
        self.mock_get_location = self.patch_location.start()
        self.mock_geolocator = self.patch_geolocator.start()
        self.mock_gethost = self.patch_gethost.start()
        self.mock_hemisphere = self.patch_hemisphere.start()

        self.mock_get_location.return_value = ("DefaultCity", "DefaultRegion", "DefaultCountry")
        self.mock_geolocator.return_value = {"latitude": "10.0", "longitude": "20.0", "address": "Full Address"}
        self.mock_gethost.return_value = "1.2.3.4"
        self.mock_hemisphere.return_value = True

    def tearDown(self):
        self.patch_location.stop()
        self.patch_geolocator.stop()
        self.patch_gethost.stop()
        self.patch_hemisphere.stop()

    def test_tc1_automatic_detection(self):
        # TC1: This test case is to test help for automatic location detection
        res = location_processing("~", "8.8.8.8")
        self.assertEqual(res[0], "~DefaultCity, DefaultCountry", "TC1 failed: Expected city name string starting with '~'")

    def test_tc2_domain_name(self):
        # TC2: This test case is to test location detection using a domain name
        res = location_processing("@example.com", "8.8.8.8")
        self.assertEqual(res[0], "~DefaultCity, DefaultCountry", "TC2 failed: Expected city name string starting with '~'")

    def test_tc3_domain_search_no_name(self):
        # TC3: This test case is to test a domain search with no name
        res = location_processing("@", "8.8.8.8")
        self.assertEqual(res[0], NOT_FOUND_LOCATION)

    def test_tc4_search_for_moon(self):
        # TC4: This test case is to test a search for the moon
        res = location_processing("moon", "8.8.8.8")
        self.mock_hemisphere.assert_called()

    def test_tc5_mylocation_keyword(self):
        # TC5: This test case is to test the MyLocation shortcut keyword
        res = location_processing("MyLocation", "1.2.3.4")
        self.assertEqual(res[0], "~DefaultCity, DefaultCountry", "TC5 failed: Expected city name string starting with '~'")

    def test_tc6_no_location_given(self):
        # TC6: This test case is to test when no location is given at all
        res = location_processing(None, "1.2.3.4")
        self.assertEqual(res[0], "~DefaultCity, DefaultCountry", "TC6 failed: Expected city name string starting with '~'")

    def test_tc7_ip_address_search(self):
        # TC7: This test case is to test search using an IP address instead of a name
        res = location_processing("1.1.1.1", "8.8.8.8")
        self.assertEqual(res[0], "~DefaultCity, DefaultCountry", "TC7 failed: Expected city name string starting with '~'")

    def test_tc8_normal_city_search(self):
        # TC8: This test case is to test a normal city name search
        res = location_processing("London", "8.8.8.8")
        self.assertEqual(res[0], "10.0,20.0")

    def test_tc9_search_starting_with_tilde(self):
        # TC9: This test case is to test a name search starting with a tilde
        res = location_processing("~Paris", "8.8.8.8")
        self.assertEqual(res[0], "10.0,20.0")

    def test_tc10_invalid_location(self):
        # TC10: This test case is to test what happens when a name cannot be found
        self.mock_geolocator.return_value = None
        res = location_processing("invalid_loc_999", "8.8.8.8")
        self.assertEqual(res[0], NOT_FOUND_LOCATION)

    def test_tc11_bypass_prefix(self):
        # TC11: This test case is to test a special bypass prefix that skips geocoding
        self.mock_geolocator.reset_mock()
        res = location_processing("~-,bad", "8.8.8.8")
        self.mock_geolocator.assert_not_called()

if __name__ == '__main__':
    unittest.main()
