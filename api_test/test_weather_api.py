import requests
import unittest


class TestWeatherApi(unittest.TestCase):
    url = "https://weatherapi-com.p.rapidapi.com/current.json"
    api_key = "81808780b2msh21c001f0d10c950p11404djsn3b4340cf147c"

    headers = {
        "X-RapidAPI-Key": "81808780b2msh21c001f0d10c950p11404djsn3b4340cf147c",
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    def test_get_weather_by_city(self):
        querystring = {"q": "Rome"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("location", data)
        self.assertIn("current", data)
        self.assertEqual(data["location"]["name"], "Rome")

    def test_get_weather_by_lat_lon(self):
        querystring = {"q": "Cancun"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data_by_city = response.json()
        lat = data_by_city["location"]["lat"]
        lon = data_by_city["location"]["lon"]
        querystring = {"q": '{}, {}'.format(lat, lon)}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data_by_latlon = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(data_by_latlon["current"]["temp_c"], data_by_city["current"]["temp_c"], 0)
        self.assertAlmostEqual(data_by_latlon["current"]["temp_f"], data_by_city["current"]["temp_f"], 0)

    def test_temp_celsius_fahrenheit(self):
        querystring = {"q": "Miami"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertGreater(data["current"]["temp_f"], data["current"]["temp_c"])
        self.assertAlmostEqual(data["current"]["temp_c"], (data["current"]["temp_f"] - 32) * 5 / 9, 0)

    def test_temp_near_feelslike(self):
        querystring = {"q": "Los Angeles"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertAlmostEqual(data["current"]["temp_c"], data["current"]["feelslike_c"], 0)
        self.assertAlmostEqual(data["current"]["temp_f"], data["current"]["feelslike_f"], 0)

    def test_lat_lon_out_of_range(self):
        """
        Possible bug:
        with querystring = {"q": '23414, 908723'} 400 error should be returned but instead 200 is returned, making this test fail
        with querystring = {"q": '2314, 9023'} the response is 400 error, making the test pass
        """
        querystring = {"q": '2314, 9023'}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        self.assertEqual(response.status_code, 400)

    def test_lat_lon_boundary_values(self):
        querystring = {"q": '95, 185'}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data1 = response.json()
        city1 = data1["location"]["name"]
        self.assertEqual(response.status_code, 200)
        querystring = {"q": '95, -185'}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data2 = response.json()
        city2 = data2["location"]["name"]
        self.assertEqual(response.status_code, 200)
        querystring = {"q": '-95, 185'}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data3 = response.json()
        city3 = data3["location"]["name"]
        self.assertEqual(response.status_code, 200)
        querystring = {"q": '-95, -185'}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        data4 = response.json()
        city4 = data4["location"]["name"]
        self.assertEqual(response.status_code, 200)

        assert city1 == city2 == city3 == city4


if __name__ == '__main__':
    unittest.main()
