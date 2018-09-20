from unittest import TestCase
from Engines.RobotController.TrackLoader import TrackLoader
from Engines.RobotController.Navigator import Navigator
from Utils.InstanceManager import InstanceManager


class TestNavigator(TestCase):

    def test_navigate_valid_route(self):
        # Set route
        Navigator.set_route(0, 5)

        # Navigate the route
        navigation_finished = False
        while not navigation_finished:
            navigation_finished = Navigator.navigate()

        self.assertTrue(True, navigation_finished)
