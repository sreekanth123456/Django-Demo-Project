from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from .models import Form1Model, Form2Model
from .forms import Form1Form, Form2Form
from django.forms.models import model_to_dict
import uuid

class ResultView(TemplateView):
	def process_year_built(self, year_built):
		return 'It\'s been around '+str(2020-int(year_built.split('-')[0])+5)+' years that it was built.'

	def process_vehicle(self, vehicle):
		return 'There are '+str(len(vehicle.split(',')))+' types of vehicles passing through this bridge'

	def process_exposed_to(self, exposed_to):
		level = {1:'low', 2:'average', 3:'medium', 4: 'high', 5:'critical'}
		length = len(exposed_to.split(','))
		return level[length], length

	def process_color(self, color):
		colors = {'B':'Black','R': 'Red', 'G': 'Green', 'b': 'Blue', 'Y': 'Yellow', 'W': 'White'}
		return colors[color]

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		unique_id = context['unique_id']
		obj = list(Form1Model.objects.filter(unique_id=unique_id))
		result_dict = {}
		if(len(obj)>0):
			result_dict = {**result_dict, **model_to_dict(obj[0])}
		obj = list(Form2Model.objects.filter(unique_id=unique_id))
		if(len(obj)>0):
			result_dict = {**result_dict, **model_to_dict(obj[0])}
		context['inquirer_name']=result_dict['inquirer_name']
		context['unique_id']=result_dict['unique_id']
		context['year_built'] = self.process_year_built(result_dict['year_built'])
		context['expected_life'] = result_dict['expected_life']
		context['vehicle'] = self.process_vehicle(result_dict['vehicle'])
		context['color'] = self.process_color(result_dict['color'])
		context['risk_level'], context['exposing_length'] = self.process_exposed_to(result_dict['exposed_to'])
		context['comments'] = None if len(result_dict['comments'])==0 else result_dict['comments']
		return context
	template_name = 'result.html'

class QueriesView(TemplateView):
	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		items = list(Form1Model.objects.all())
		result_list = []
		colors = {'B':'Black','R': 'Red', 'G': 'Green', 'b': 'Blue', 'Y': 'Yellow', 'W': 'White'}
		for item in items:
			result_dict = {}
			result_dict = {**result_dict, **model_to_dict(item)}
			result_dict['color'] = colors[result_dict['color']]
			form2item = list(Form2Model.objects.filter(unique_id=result_dict['unique_id']))
			if(len(form2item)>0):
				result_dict = {**result_dict, **model_to_dict(form2item[0])}
			result_list.append(result_dict)
		context['result'] = result_list
		return context
	template_name = 'queries.html'


def Form_1View(request):
	if request.method == 'POST':
		print(request.POST)
		if 'year_built' in request.POST:
			return Form_2View(request, request.POST.get('unique_id'))	
		form1 = Form1Form(request.POST)
		if form1.is_valid():
			temp_1 = form1.save(commit=False)
			temp_1.unique_id = str(uuid.uuid4())
			temp_1.save()
			return Form_2View(request, temp_1.unique_id)
	else:
		form1 = Form1Form()
	args = {'form': form1}
	return render(request, 'form_1.html', args)


def Form_2View(request, unique_id):
	print(unique_id)
	if request.method == 'POST' and 'year_built' in request.POST:
		form2 = Form2Form(request.POST)
		if form2.is_valid():
			temp_2 = form2.save(commit=False)
			temp_2.unique_id = unique_id
			print(temp_2.unique_id)
			temp_2.save()
			return redirect(reverse('result', kwargs={'unique_id':unique_id}))
	else:
		form2 = Form2Form(initial={'unique_id':unique_id})
	args = {'form': form2}
	return render(request, 'form_2.html', args)
