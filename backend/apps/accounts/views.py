from django.shortcuts import render

# Create your views here.
class UserListView(APIView):
    def get(self, request, *args, **kwargs):
        if request.version == 'v1':
            print('v1')
        elif request.version == 'v2' :
            print('v2')