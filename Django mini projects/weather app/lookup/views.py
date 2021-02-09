import json
import requests
from django.shortcuts import render


# Create your views here.
def home(request):

    def renderScreen(zipcode='20002'):
        api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + zipcode + "&distance=2&API_KEY=73EC8BCC-2960-472C-AB96-25889CA7BCAD")
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = 'Error occoured with {}...'.format(e)
        if api[0]['Category']['Name'] == 'Good':
            category_color = 'good'
            category_description = 'The current air quality is good.'
        elif api[0]['Category']['Name'] == 'Moderate':
            category_color = 'moderate'
            category_description = 'The current air quality is Moderate.'
        elif api[0]['Category']['Name'] == 'Unhealthy for Sensitive Groups':
            category_color = 'usg'
            category_description = 'The current air quality is Unhealthy for Sensitive Groups.'
        elif api[0]['Category']['Name'] == 'Unhealthy':
            category_color = 'unhealthy'
            category_description = 'The current air quality is Unhealthy.'
        elif api[0]['Category']['Name'] == 'Very Unhealthy':
            category_color = 'veryunhealthy'
            category_description = 'The current air quality is Very Unhealthy.'
        elif api[0]['Category']['Name'] == 'Hazardous':
            category_color = 'hazardous'
            category_description = 'The current air quality is Hazardous.'
        return render(request, 'home.html', {'api': api, 'category_description': category_description, 'category_color': category_color})

    if request.method == 'POST':
        # POST method.
        zipcode = request.POST['zipcode_searchbar']
        return renderScreen(zipcode)
    elif request.method == 'GET':
        # GET method.
        # https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=20002&distance=2&API_KEY=73EC8BCC-2960-472C-AB96-25889CA7BCAD
        return renderScreen()


def about(request):
    return render(request, 'about.html', {})
