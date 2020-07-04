import requests
import json
import pyttsx3
import speech_recognition as sr 
import re
api_key = "tgmPv_u_SvxQ"
project_token = "tWzFYYXqwnRF"

# response = requests.get(f'https://www.parsehub.com/api/v2/projects/{project_token}/last_ready_run/data', params={"api_key": api_key})
# data = json.loads(response.text)
# print(data['coronavirus_cases'])

class Data:
    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key": self.api_key
        }
        self.get_data()

    def get_data(self):
        '''Get updated data'''
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data', self.params)
        self.data = json.loads(response.text)

    def get_total_cases(self):
        total = self.data['coronavirus_cases']
        for info in total:
            if info['name'] == 'Coronavirus Cases:':
                return info['total_cases']

    def get_total_deaths(self):
        total = self.data['coronavirus_cases']
        for info in total:
            if info['name'] == 'Deaths:':
                return info['total_cases']
    
    def get_total_recoveries(self):
        total = self.data['coronavirus_cases']
        for info in total:
            if info['name'] == 'Recovered:':
                return info['total_cases']

    def get_country_data(self, country):
        total = self.data['country']
        for info in total:
            if info['name'].lower() == country.lower():
                # return info['total']
                if 'total' in info.keys():
                    return info['total']
                else:
                    return f"No data yet for {country}"
        return "0"


    def get_country_new_cases(self, country):
        total = self.data['country']
        for info in total:
            if info['name'].lower() == country.lower():
                # return info['new_cases']
                if 'new_cases' in info.keys():
                    return info['new_cases']
                else:
                    return f"No data yet for {country}"
        return "0"
    
    def get_country_new_deaths(self, contry):
        total = self.data['country']
        for info in total:
            if info['name'].lower() == country.lower():
                if 'new_deaths' in info.keys():
                    return info['new_deaths']
                else:
                    return f"No data yet for {country}"
        return "0"

    def get_list_of_countries(self):
        countries = [country['name'].lower() for country in self.data['country']]
        return countries


# data = Data(api_key, project_token)
# print(data.get_list_of_countries())

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# speak("Bonjour Nordyn")

def get_audio():
    r = sr.Recognizer() 
    with sr.Microphone() as source:
        audio = r.listen(source) # record the audio then pass it to recognize_google
        said = ""

        try:
            said = r.recognize_google(audio) # return the audio as text
        except Exception as e:
            print("Exception:", str(e))

    return said.lower()
# print(get_audio())

def main():
    print("Started Program")
    data = Data(api_key, project_token)
    
    end_text = "stop"
    result = None
    total_patterns = {
        re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
        re.compile("[\w\s]+ total cases"):data.get_total_cases, 
        re.compile("[\w\s]+ total [\w\s]+ deaths"): data.get_total_deaths,
        re.compile("[\w\s]+ total deaths"): data.get_total_deaths

    }

    while  True:
        print('Listening...')
        text = get_audio()
        # print(text)
        for pattern, func in total_patterns.items():
            if pattern.match(text):
                result = func()
                break
        if result:
            speak(result)

        if text.find(end_text): # stop loop
            break

# main()