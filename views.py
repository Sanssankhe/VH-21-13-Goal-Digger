from django.shortcuts import render, redirect
import requests
import json

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "616a05a87fmsh08a9846f6a06cd3p193744jsn3ef06dbc9a49"
    }

response = requests.request("GET", url, headers=headers).json()


# Create your view
def covidcases(request):
  mylist = []
  noofresults = int(response['results'])

  for x in range(0,noofresults):
     mylist.append(response['response'][x]['country'])

  if request.method=="POST":
    selectedcountry= request.POST['selectedcountry']

    for x in range(0,noofresults):
      if selectedcountry == response['response'][x]['country']:
       new = response['response'][x]['cases']['new']
       active = response['response'][x]['cases']['active']
       critical= response['response'][x]['cases']['critical']
       recovered = response['response'][x]['cases']['recovered']
       total = response['response'][x]['cases']['total']
       deaths = int(total) - int(active) - int(recovered)
       context = {'selectedcountry': selectedcountry,'mylist':mylist, 'new': new, 'active': active, 'critical':critical, 'recovered': recovered, 'deaths': deaths, 'total':total}
       return render(request, 'cases.html', context)


  context = {'mylist': mylist}
  return render(request, 'cases.html', context)

