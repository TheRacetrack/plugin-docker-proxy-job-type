from typing import Dict, Tuple
from pathlib import Path


class Plugin:
    def fatman_job_types(self, docker_registry_prefix: str) -> Dict[str, Tuple[str, Path]]:
        """
        Job types created by this plugin
        :param docker_registry_prefix: prefix for the image names (docker registry + namespace)
        :return dict of job name -> (base image name, dockerfile template path)
        """
        return {
            'docker-http': (
                f'{docker_registry_prefix}/docker-http:{self.plugin_manifest.version}', 
                self.plugin_dir / 'fatman-template.Dockerfile',
            ),
        }
