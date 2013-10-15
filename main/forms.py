from django.forms import ModelForm
from toilet.models import Toilet

class AddRestroomForm (ModelForm):
	class Meta:
		model = Toilet
		fields = ['date', 'creator']

form = AddRestroomForm()

#toilet = Toilet.objects.get(pk=1)
#form = AddRestroomForm(instance = toilet) 
