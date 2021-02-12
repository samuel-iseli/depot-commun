from rest_framework.permissions import BasePermission


class MayReadDepot(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        requested_depot_uuid = view.kwargs['depot_uuid']
        allowed_depot_uuids = {d.uuid for d in request.user.depots.all()}

        if requested_depot_uuid in allowed_depot_uuids:
            return True

        return False


class MayReadPurchases(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        requested_user_uuid = view.kwargs['user_uuid']

        return user.uuid == requested_user_uuid

