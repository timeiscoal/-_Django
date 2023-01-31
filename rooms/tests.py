# testcase는 자동으로 장고 제공
from django.test import TestCase
# restframework에서 제공하는 테스트 코드
from rest_framework.test import APITestCase
from user.models import User
from . import models

# Create your tests here.

class TestAmenities(APITestCase):


    NAME = "Amenity Test"
    DESC = "Amenity Description"
    URL = "/rooms/amenites/"

    #테스트를 매번 진행할 때 마다 임시 데이터베이스가 생성되고 삭제가 되는데 , 그로 인해서 데이터베이스에 어떤 데이터도 없다. 이를 설정해주는 메소드

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
            
        )


    # 반드시 test_가 들어가야함.
    def test_all_ameities(self):

    # self.client은 좋은 도구임 이걸 통해서 API로 get put delete 등을 보낼 수 있음.
    # test는 test데이터베이스를 임의로 생성해서 진행함. 그래서 []빈 리스트가 나오는 것은 데이터베이스에 데이터가 없기 때문이다. 그리고 테스트가 바로 끝나면 삭제됨.
        response =self.client.get(self.URL)
        data = response.json()

        # 우선 해당 url로 접근을 했을 때 잘 접속되는지 확인.
        # 그리고 아니라면 에러메시지 출력.
        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200."
        )
        # 지금 받고 있는 데이터의 형태가 리스트인 것을 확인해볼 수 있었다.
        # str로 변경해보면 str이 아니라고 알려줌.
        # 들어오는 데이터가 리스트인가?
        self.assertIsInstance(data, list)
        # 데이터의 길이는 1인가?
        self.assertEqual(len(data),1)
        # 데이터가 들어오는 0번째 인덱스에서 name의 값과 위에서 선언한 NAME의 값이 같은 값으로 들어오는가.
        self.assertEqual(data[0]["name"], self.NAME,)
        self.assertEqual(data[0]['description'], self.DESC,)

    # 생성 테스트
    def test_create_ameity(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity Description"
        
        
        # post요청을 보내는데, 해당 url로 보내고 데이터는 다음과 같이 보낼게.
        response = self.client.post(self.URL, 
        data={"name":new_amenity_name, "description":new_amenity_description},
        )

        data = response.json()

        # 마지막에 메세지를 항상 작성하는 이유는 아닐 경우의 메세지를 볼 수 있게 작성해야함.
        
        # 데이터가 잘 저장되고 있는가.
        self.assertEqual(response.status_code,201,"NOT 200 status Code ")
        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_description)


        # 잘못된 데이터를 보냈을 때. 예외처리일 경우.
        # 필수 데이터인데 없을 경우.
        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code,400)
        self.assertIn("name", data )
    

# detail test

class TestAmenity(APITestCase):

    NAME = "Test Amenity"
    DESC = "Test Des"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_found(self):
       response = self.client.get("/rooms/amenites/2/")
       self.assertEqual(response.status_code,404)


    def test_get_amenity(self):
       response = self.client.get("/rooms/amenites/1/")
       self.assertEqual(response.status_code,200)


    # 수정이 되는 경우에 어떻게 처리하면 좋을까. 음응 예를 들면 글자 개수를 초과할 경우.
    def test_update_amenity(self):
        put_url="/rooms/amenites/1/"

        response = self.client.put(put_url, 
        data={"name":"test_Put","description":"test_description"},
        )
        data = response.json()
        self.assertEqual(response.status_code,200, "can not fix amenity")


        response1 = self.client.put(put_url,
        data={"name":"test_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Puttest_Put","description":"test_wrong"},)
        self.assertEqual(response1.status_code,400)


    
    def test_delete_amenity(self):
        
        response = self.client.delete("/rooms/amenites/1/")
        self.assertEqual(response.status_code,204)


class TestRooms(APITestCase):

         # 아이디 생성
    def setUp(self):
        user = User.objects.create(
            username="test"
            
        )
        user.set_password("123")
        user.save()

        # 아이디를 생성한 후에, class 내부에 저장을 해서 method에서 접근이 가능하게 만들어준 것이다.
        self.user = user

    def test_create_room(self):

        response=self.client.post("/rooms/")
        self.assertEqual(response.status_code , 403)

        # 로그인
        # 일반 login일 경우 username과 password가 필요하지만 force_login은 필요없음.
        self.client.force_login(
            self.user
        )
        # 다시 게시글 생성
        response = self.client.post("/rooms/")
        print(response.json())
