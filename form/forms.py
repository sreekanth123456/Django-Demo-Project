from django import forms

from .models import Form1Model, Form2Model

COLORS= (
	('B', 'Black'),
	('R', 'Red'),
	('G', 'Green'),
	('b', 'Blue'),
	('Y', 'Yellow'),
	('W', 'White'),
)
VEHICLES_DICT= {'car': 'Car', 'bus':'Bus', 'tram':'Tramcar', 'metro':'Metro', 'Trucks':'Trucks', 'rail':'Rail'}
VEHICLES= (
	('car', 'Car'),
	('bus','Bus'),
	('tram','Tramcar'),
	('metro','Metro'),
	('Trucks','Trucks'),
	('rail','Rail')
)

YEAR_BUILT=(
	('1971-1980', '1971-1980'),
	('1981-1990', '1981-1990'),
	('1991-2000', '1991-2000'),
	('2001-2010', '2001-2010'),
	('2011-2020', '2011-2020')
)

EXPOSED_TO_DICT = {'water':'Water', 'smoke':'Smoke', 'fire':'Fire', 'rain':'Rain', 'sun':'Sun', 'heavy_traffic':'Heavy Traffic', 'animals':'Animals'}
EXPOSED_TO = (
	('water','Water'),
	('smoke','Smoke'),
	('fire','Fire'),
	('rain','Rain'),
	('sun','Sun'),
	('heavy_traffic','Heavy Traffic'),
	('animals','Animals')
)

class Form1Form(forms.ModelForm):
	inquirer_name = forms.CharField(widget=forms.TextInput(), label='Inquirer Name')
	expected_life = forms.DecimalField(widget=forms.NumberInput(), label='Expected Life')
	color = forms.ChoiceField(widget = forms.RadioSelect(), choices = COLORS, label='Bridge Color')
	class Meta:
		model = Form1Model
		fields = ['inquirer_name','expected_life','color']

class Form2Form(forms.ModelForm):
	unique_id = forms.CharField(widget=forms.HiddenInput())
	exposed_to = forms.MultipleChoiceField(widget = forms.SelectMultiple(), choices = EXPOSED_TO, label='Exposed to', help_text='Select a max of 3 items')
	vehicle = forms.MultipleChoiceField(widget = forms.CheckboxSelectMultiple(), choices = VEHICLES, label='Vehicles')
	year_built = forms.ChoiceField(widget = forms.Select(), choices = YEAR_BUILT, label='Year Built')
	comments = forms.CharField(widget=forms.Textarea(attrs={'rows': 10}), required=False)
	
	class Meta:
		model = Form2Model
		fields = ['unique_id','exposed_to','vehicle','year_built','comments']
	
	def clean_exposed_to(self):
		exposed_to = self.cleaned_data['exposed_to']
		if not exposed_to:
			raise forms.ValidationError("Select atleast 1 option")

		if len(exposed_to) > 3:
			raise forms.ValidationError("Do not select more than 3 options")

		for i in range(len(exposed_to)):
			exposed_to[i] = EXPOSED_TO_DICT[exposed_to[i]]
		exposed_to = ', '.join(exposed_to)
		return exposed_to

	def clean_vehicle(self):
		vehicle= self.cleaned_data['vehicle']
		for i in range(len(vehicle)):
			vehicle[i] = VEHICLES_DICT[vehicle[i]]
		vehicle = ', '.join(vehicle)
		return vehicle