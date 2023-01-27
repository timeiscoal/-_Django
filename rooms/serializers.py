from rest_framework import serializers
from rooms.models import Amenity, Room
from common.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer
from wishlists.models import Wishlist


class AmenitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


# serializer는 owner가 필요하고 그 owner는 TinyUserSerializer의 데이터 형태를
# 가지고 있어야 한다는 것만 알고 있다. 그러니 read_only를 속성으로 넣어주면 owner의 데이터는 여전히 필요하지만 request.data로부터는 오지 않는다.
# 유저 데이터로부터는 오지 않는다는 것이다.
# 그럼 유저 데이터는 어디서 받아와야 할까. 방을 생성할 때.
# request에서 받아온다.
class RoomDetailSerializer(serializers.ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitiesSerializer(many=True)
    category = CategorySerializer(read_only=True)

    photos = PhotoSerializer(many=True, read_only=True)

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    # 방 데이터를 보여줄 때 역 접근자를 포함하는 것은 좋지 못한 생각일 수 있다. 이유는 리뷰가 한 두개가 아닐때를 생각해보자. 그래서 페이지를 생성하는 방법을 고민해보자. 페이지 네이션.
    reviews = ReviewSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    def get_rating(self, room):
        return room.rating()

    def get_is_owner(self, obj):
        request = self.context['request']

        # context = {"request":request}와 같이 데이터를 직접 넣는 방식도 있다.
        # 이를 통해서 request.user가 해당 방의 주인인지 아닌지 확인 해 볼 수 있었다.
        # 이렇게 하면 이후 주인의 경우에게만 수정 버튼을 보이게 할 수 있다.
        return obj.owner == request.user

    # def get_rating(self, obj):
    #     return obj.rating()

    
    def get_is_liked(self, obj):
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, rooms__pk=obj.pk).exists()


    class Meta:
        model = Room
        fields = "__all__"
        # depth = 1

    def create(self, validated_data):
        return super().create(validated_data)


class RoomListSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    rating = serializers.SerializerMethodField()

    photos = PhotoSerializer(many=True, read_only=True)

    def get_rating(self, obj):
        return obj.rating()

    def get_is_owner(self, obj):
        request = self.context["request"]
        return obj.owner == request.user



    class Meta:
        model = Room
        fields = (
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )
