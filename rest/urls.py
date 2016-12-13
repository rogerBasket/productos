from django.conf.urls import url, include

from . import views
from .constantes import REGEX_IMAGES

urlpatterns = [
	#url(r'^(index(\.html){0,1}){0,1}$', views.index)
	url(r'^index$', views.index),
	url(r'^uploadImage$', views.SingleImage.as_view()),
	url(r'^deleteImage/(?P<filename>' + REGEX_IMAGES + ')$', views.DeleteImage.as_view(), name = 'delete-image'),
	url(r'^classificationImage/(?P<filename>' + REGEX_IMAGES + ')$', views.ClassificationImage.as_view()),
	url(r'^multipleClassification$', views.MultipleClassification.as_view()),
	url(r'^learningImage/(?P<filename>' + REGEX_IMAGES + ')$', views.LearningImage.as_view())
]
