from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views import View
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.contrib.auth import get_user_model
from lambda_theme.helpers import parse_template_name, select_template

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import UserProfile
from .serializers import UserSerializer, GroupSerializer, AccountSerializer, UserProfileCreateSerializer


PROFILE_FORM = 'lambda_core.user_profile.forms.UserProfileForm'


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileAPIView(APIView):
    """
    API endpoint that allows the current user account to be viewed or edited.
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        serializer = AccountSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileCreateSerializer(data={
            'avatar': request.data['avatar'],
            'user': request.user.pk,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('user_profile.change_own_userprofile', raise_exception=True), name='dispatch')
class ProfileView(View):
    template_name = 'account/profile.html'

    @property
    def form_class(self):
        try:
            account_forms = getattr(settings, 'ACCOUNT_FORMS', {})
            account_form = account_forms['profile']
        except KeyError:
            account_form = PROFILE_FORM
        return import_string(account_form)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'avatar': request.user.profile.avatar if request.user.profile else None,
        })
        return render(request, self.template_name,  {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            avatar = form.cleaned_data['avatar']

            user = request.user
            profile, created = UserProfile.objects.get_or_create(user=user)

            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            if avatar:
                profile.avatar = avatar

            user.save()
            profile.save()

            messages.success(request, _('Update profile successfully'))

        return render(request, self.template_name,  {'form': form})
