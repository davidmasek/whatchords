from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from . import triads

# Create your views here.
def home(request):
	if request.method == 'POST' and 'prog' in request.POST:
		prog = request.POST['prog']
		generator = triads.ProgressionGenerator()
		try:
			progressions = generator.get_progressions(prog)
		except triads.GeneratorError:
			return HttpResponse('Incorrect input.', content_type="text/plain", status=400)
		return render(request, 'chords/progressions_table.html', {
			'progressions': progressions,
			})
	return render(request, 'chords/home.html')