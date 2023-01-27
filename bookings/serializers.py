from django.utils import timezone
from rest_framework import serializers
from .models import Booking




class CreateRoomBookingSerializer(serializers.ModelSerializer):

    # model에서는 입력을 반드시 하지 않아도 되게 설정을 했지만 생성을 위해서는 반드시 필요하게 여기서 변경해줌. 

    check_in = serializers.DateField()
    check_out = serializers.DateField()
    
    # vaildate 커스텀.
    def validate_check_in(self,value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        else:
            return value

    def validate_check_out(self,value):
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past")
        else:
            return value
    
    def validate(self, data):
        if data["check_out"] < data["check_in"]:
            raise serializers.ValidationError("체크인 날짜는 반드시 체크아웃 전의 날짜여야 합니다.")
        # 다른 사람 체크인 날짜. >= 내가 예약 종료 날짜.
        # 다른 사람 체크 아웃 날짜 <= 내가 예약 시작 날짜.

        if Booking.objects.filter(check_in__lte=data["check_out"],check_out__gte=data["check_in"],).exists():
            raise serializers.ValidationError(
                "다른 사람이 이미 예약한 날짜가 포함되어 있습니다."
            )


        return data

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )
    






class PubilcBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )