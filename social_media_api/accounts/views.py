# Profile View (Authenticated)
class ProfileView(generics.GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# List All Users (Authenticated)
class ListUsersView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        data = [{"id": u.id, "username": u.username} for u in users]
        return Response(data)


# Follow / Unfollow (Authenticated)
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def post(self, request, user_id):
        target_user = User.objects.filter(id=user_id).first()
        if not target_user:
            return Response({"error": "User not found"}, status=404)
        if request.user == target_user:
            return Response({"error": "You cannot follow yourself"}, status=400)
        target_user.followers.add(request.user)
        return Response({"message": f"You are now following {target_user.username}"})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users

    def post(self, request, user_id):
        target_user = User.objects.filter(id=user_id).first()
        if not target_user:
            return Response({"error": "User not found"}, status=404)
        target_user.followers.remove(request.user)
        return Response({"message": f"You have unfollowed {target_user.username}"})
