from dataclasses import fields

from bigbytes.api.presenters.BasePresenter import BasePresenter
from bigbytes.cluster_manager.config import (
    CloudRunWorkspaceConfig,
    EcsWorkspaceConfig,
    KubernetesWorkspaceConfig,
)
from bigbytes.shared.hash import merge_dict


class WorkspacePresenter(BasePresenter):
    default_attributes = list(
        set(
            [
                'access',
                'cluster_type',
                'instance',
                'name',
                'repo_path',
                'success',
                'url',
                *[f.name for f in fields(KubernetesWorkspaceConfig)],
                *[f.name for f in fields(CloudRunWorkspaceConfig)],
                *[f.name for f in fields(EcsWorkspaceConfig)],
            ]
        )
    )

    async def present(self, **kwargs):
        workspace = self.model.pop('workspace', None)
        workspace_config = dict()
        if workspace:
            workspace_config = workspace.to_dict()
        data = merge_dict(workspace_config, self.model)

        return data
