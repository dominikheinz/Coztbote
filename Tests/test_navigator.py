from unittest import TestCase
from Engines.Navigation.Navigator import Navigator


class TestNavigator(TestCase):

    def test_navigate_valid_route(self):
        # Set route
        Navigator.set_route(0, 5)

        # Navigate the route
        navigation_finished = False
        while not navigation_finished:
            navigation_finished = Navigator.navigate()

        self.assertTrue(True, navigation_finished)
