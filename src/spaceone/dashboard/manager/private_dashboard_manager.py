import logging
from typing import Tuple
from mongoengine import QuerySet

from spaceone.core.manager import BaseManager
from spaceone.dashboard.model.private_dashboard.database import PrivateDashboard

_LOGGER = logging.getLogger(__name__)


class PrivateDashboardManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboard_model = PrivateDashboard

    def create_private_dashboard(self, params: dict) -> PrivateDashboard:
        def _rollback(vo: PrivateDashboard) -> None:
            _LOGGER.info(
                f"[create_private_dashboard._rollback] "
                f"Delete vo : {vo.name} "
                f"({vo.private_dashboard_id})"
            )
            vo.delete()

        dashboard_vo: PrivateDashboard = self.dashboard_model.create(params)
        self.transaction.add_rollback(_rollback, dashboard_vo)

        return dashboard_vo

    def update_private_dashboard_by_vo(
        self, params: dict, dashboard_vo: PrivateDashboard
    ) -> PrivateDashboard:
        def _rollback(old_data: dict) -> None:
            _LOGGER.info(
                f"[update_private_dashboard_by_vo._rollback] Revert Data : "
                f'{old_data["private_dashboard_id"]}'
            )
            dashboard_vo.update(old_data)

        self.transaction.add_rollback(_rollback, dashboard_vo.to_dict())
        return dashboard_vo.update(params)

    @staticmethod
    def delete_private_dashboard_by_vo(dashboard_vo: PrivateDashboard) -> None:
        dashboard_vo.delete()

    def get_private_dashboard(
        self,
        private_dashboard_id: str,
        domain_id: str,
        user_id: str,
    ) -> PrivateDashboard:
        return self.dashboard_model.get(
            private_dashboard_id=private_dashboard_id,
            domain_id=domain_id,
            user_id=user_id
        )

    def filter_private_dashboards(self, **conditions) -> QuerySet:
        return self.dashboard_model.filter(**conditions)

    def list_private_dashboards(self, query: dict) -> Tuple[QuerySet, int]:
        return self.dashboard_model.query(**query)

    def stat_private_dashboards(self, query: dict) -> dict:
        return self.dashboard_model.stat(**query)
