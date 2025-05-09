from rest_framework import serializers, response
from .models import Profile, Skill, Follow

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only = True)
    class Meta:
        model = Profile
        exclude = ('date_joined',)
        extra_kwargs = {'password':{'write_only': True}}
       

    def validate(self, data):
            if data['password2'] != data['password']:
                raise ValueError("Your password does not match")
            return data
        
    def create(self,request, validated_data):
            validated_data.pop('password2')
            user = Profile.objects.create_user(**validated_data)
            return user

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
          model = Profile
          fields = ['pfp', 'username', 'full_name', 'email', 'phone_number' , 'bio','birthday', 'gender',  ]
          extra_kwargs = {'password':{'write_only':True }}

    
    

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['skill']

    def create(self, validated_data):
         request = self.context.get('request')
         validated_data['profile'] = request.user
         return super().create(validated_data)
    
class FollowSerializer(serializers.ModelSerializer):

    class Meta:
          model = Follow
          fields = ['profile',  'follower', 'following'] 

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['profile'] = request.user
        return super().create(validated_data)