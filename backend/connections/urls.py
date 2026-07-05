from rest_framework.routers import DefaultRouter
from .views import UserSearchViewSet, FriendRequestViewSet, FriendViewSet
router=DefaultRouter(); router.register('search',UserSearchViewSet,basename='user-search'); router.register('requests',FriendRequestViewSet,basename='friend-requests'); router.register('',FriendViewSet,basename='friends')
urlpatterns=router.urls
